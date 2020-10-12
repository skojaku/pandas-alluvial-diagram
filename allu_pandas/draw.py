import numpy as np
import matplotlib.pyplot as plt
from . import utils
import matplotlib.patheffects as PathEffects


def draw(
    df,
    columns,
    color_by=None,
    palette=None,
    ax=None,
    margin=0.2,
    label_pad=0.05,
    show_count=False,
    row_order=[],
):
    """
    Draw alluvial diagram from pandas. 
    This function draws an alluvial diagram, with flows between groups specified by columns of `df`.
    Specifically, each group is a set of records with the same column (say `col`) and value in the column (say `v`).
    The groups are orderd horizontally based on `col` and vertically based on `v`.
    The height of a group represents the number of records that the group contains.

    Params
    ------
    df: pandas.DataFrame
    columns: list of str
        Name of columns
    color: str or func
        Name of color of a function for each flow across multiple groups.
        A flow starts from the left-most group, go through middle groups and end at the right-most group. 
        If a function is given, the function will receive a list of (`col`, `v`) pairs in order of 
        the groups along the path. For example, if a flow goes along a path of groups, ('col1', 'a'), ('col2', 'x'), ('col3', 'W'), 
        then the function will receive list [('col1', 'a'), ('col2', 'x'), ('col3', 'W')].
    palette: str
        Palette of colors. Flow will be colored based on the left-most group.
    ax: matplotlib.pyplo.gca
    margin: vertical margin between groups
    label_pad: int
        margin between the flow and labels 
    row_order: list of tuples
        Each tuple is (`col`, `v`), where `col` is the column name and `v` is the value of the group. 
        Force a group with row_order[i] to be placed above row_order[i+1]
    """
    if ax is None:
        ax = plt.gca()

    #
    # Compute the size of groups
    #
    dg = df[columns].groupby(columns).size().reset_index().sort_values(by=columns)
    sum_all = dg[0].sum()

    #
    # Set the colors
    #
    dg["_color"] = utils.make_color_column(dg, columns, color_by, palette)

    #
    # Order group vertically
    #
    dg = dg.sort_values(
        by="_color"
    )  # utils.order_groups_by_rows(dg, columns, row_order)

    #
    # Compute the top left coner of groups
    #
    offset = {}
    group_position_type = {}
    for col_id, col in enumerate(columns):
        keys = dg[col].drop_duplicates().values
        offset_key = 0.0

        col_row_order = [r[1] for r in row_order if r[0] == col]
        ordered_keys = [r for r in col_row_order if r in keys]
        keys = np.concatenate([ordered_keys, keys[~np.isin(keys, col_row_order)]])

        for i, key in enumerate(keys):
            offset[(col, key)] = -offset_key

            v = np.sum(dg.loc[dg[col] == key, 0]) / sum_all
            offset_key += v + margin

            if col_id == 0:
                group_position_type[(col, key)] = "left"
            elif col_id == len(columns) - 1:
                group_position_type[(col, key)] = "right"
            else:
                group_position_type[(col, key)] = "middle"

        if (col_id != 0) and (col_id != len(columns) - 1):
            group_position_type[(col, keys[0])] = "top"
            group_position_type[(col, keys[-1])] = "bottom"
    #
    # Compute the coordinate of flows
    #
    flows = []
    flows_bundled_by_group = {}
    for _, row in dg.iterrows():
        height = row[0] / sum_all
        # make a list of (x,y) going through the top left corner of the group
        xys = []
        for i, col in enumerate(columns):
            xys += [(i / (len(columns) - 1), offset[(col, row[col])])]
            offset[(col, row[col])] = offset[(col, row[col])] - height
        flow = {
            "xys": xys,
            "height": height,
            "groups": [(c, row[c]) for c in columns],
            "color": row["_color"],
            "sz": row[0],
        }
        flows += [flow]

        for i, col in enumerate(columns):
            flows_bundled_by_group[(col, row[col])] = flows_bundled_by_group.get(
                (col, row[col]), []
            ) + [flow]

    #
    # Draw flows
    #
    for flow in flows:
        height = flow["height"]
        xys = flow["xys"]
        c = flow["color"]

        # Draw bezier curve
        utils.plot_curves(xys, height, ax, color=c)

    #
    # Draw labels
    #
    for (col, v), flows_in_group in flows_bundled_by_group.items():
        # compute the corner
        cid = np.where(np.isin(columns, col))[0][0]
        x = np.min([flow["xys"][cid][0] for flow in flows_in_group])
        y = np.max([flow["xys"][cid][1] for flow in flows_in_group])
        height = np.sum([flow["height"] for flow in flows_in_group])
        sz = np.sum([flow["sz"] for flow in flows_in_group])

        group_pos = group_position_type[(col, v)]

        label_x = x + label_pad
        label_y = y - height / 2
        label_ha = "left"
        label_va = "center"
        if group_pos == "left":
            label_ha = "right"
            label_x = -label_pad
        elif group_pos == "right":
            label_ha = "left"
            label_x = 1 + label_pad
        elif group_pos == "top":
            label_va = "bottom"
            label_ha = "center"
            label_x = x
            label_y = y + 2 * label_pad
        elif group_pos == "bottom":
            label_va = "top"
            label_ha = "center"
            label_x = x
            label_y = y - height - 2 * label_pad

        if show_count:
            v = v + "\n(%d)" % sz
        txt = ax.annotate(
            v, xy=(label_x, label_y), xycoords="data", ha=label_ha, va=label_va
        )
        txt.set_path_effects([PathEffects.withStroke(linewidth=5, foreground="w")])
        plt.draw()

    #
    # Prettify
    #
    ax.axis("off")

    return ax
