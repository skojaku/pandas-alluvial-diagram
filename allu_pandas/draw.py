import numpy as np
import matplotlib.pyplot as plt
from . import utils


def draw(df, columns, color=None, ax=None, margin=0.05, row_order=[]):
    if ax is None:
        ax = plt.gca()

    dg = df[columns].groupby(columns).size().reset_index().sort_values(by=columns)
    sum_all = dg[0].sum()
    offset = {}
    for col in columns:
        keys = dg[col].drop_duplicates().values
        offset_key = 0.0

        ordered_keys = [r for r in row_order if r in keys]
        keys = np.concatenate([ordered_keys, keys[~np.isin(keys, row_order)]])

        for i, key in enumerate(keys):
            offset[(col, key)] = -offset_key
            v = np.sum(dg.loc[dg[col] == key, 0]) / sum_all
            offset_key += v + margin

    def calc_order(row, columns, row_order):
        s = 0
        for i, col in enumerate(columns):
            rank = np.where(np.isin(row_order, row[col]))[0][0]
            if rank is None:
                rank = len(row_order) + 1
            s += rank * np.power(len(columns) - i - 1, 10)
        return s

    if len(row_order) > 0:
        dg["_order"] = dg.apply(lambda x: calc_order(x, columns, row_order), axis=1)
        dg = dg.sort_values(by="_order")
    for _, row in dg.iterrows():
        height = row[0]
        xys = []
        for i, col in enumerate(columns):
            xys += [(i / (len(columns) - 1), offset[(col, row[col])])]
            offset[(col, row[col])] = offset[(col, row[col])] - height / sum_all

        if callable(color):
            c = color(row)
        else:
            c = color
        utils.plot_curves(
            xys, height / sum_all, ax, color=c if c is not None else "#444444"
        )
    ax.axis("off")
    return ax
