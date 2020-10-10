import numpy as np
import matplotlib.pyplot as plt
from . import utils


def draw(df, columns, color=None, palette=None, ax=None, margin=0.05, row_order=[]):
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
    # Compute the top left coner of groups
    #
    offset = {}
    for col in columns:
        keys = dg[col].drop_duplicates().values
        offset_key = 0.0

        col_row_order = [r[1] for r in row_order if r[0] == col]
        ordered_keys = [r for r in col_row_order if r in keys]
        keys = np.concatenate([ordered_keys, keys[~np.isin(keys, col_row_order)]])

        for i, key in enumerate(keys):
            offset[(col, key)] = -offset_key
            v = np.sum(dg.loc[dg[col] == key, 0]) / sum_all
            offset_key += v + margin

    #
    # Order group vertically
    #
    dg = utils.order_groups_by_rows(dg, columns, row_order)

    #
    # Set the colors
    #
    palette = utils.make_color_palette(dg, columns, color, palette)

    #
    # Draw
    #
    for _, row in dg.iterrows():
        height = row[0]
        # make a list of (x,y) going through the top left corner of the group
        xys = []
        for i, col in enumerate(columns):
            xys += [(i / (len(columns) - 1), offset[(col, row[col])])]
            offset[(col, row[col])] = offset[(col, row[col])] - height / sum_all

        # generate color
        if callable(palette):
            c = palette([(col, row[col]) for col in columns])
        else:
            c = palette

        # Draw bezier curve
        utils.plot_curves(xys, height / sum_all, ax, color=c)

    #
    # Prettify
    #
    ax.axis("off")

    return ax
