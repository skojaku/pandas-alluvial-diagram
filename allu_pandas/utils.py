import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.special import comb


def bernstein_poly(i, n, t):
    """
     The Bernstein polynomial of n, i as a function of t
    """

    return comb(n, i) * (t ** (n - i)) * (1 - t) ** i


def bezier_curve(points, nTimes=1000):
    """
       Given a set of control points, return the
       bezier curve defined by the control points.

       points should be a list of lists, or list of tuples
       such as [ [1,1], 
                 [2,3], 
                 [4,5], ..[Xn, Yn] ]
        nTimes is the number of time steps, defaults to 1000

        See http://processingjs.nihongoresources.com/bezierinfo/
    """

    nPoints = len(points)
    xPoints = np.array([p[0] for p in points])
    yPoints = np.array([p[1] for p in points])

    t = np.linspace(0.0, 1.0, nTimes)

    polynomial_array = np.array(
        [bernstein_poly(i, nPoints - 1, t) for i in range(0, nPoints)]
    )

    xvals = np.dot(xPoints, polynomial_array)
    yvals = np.dot(yPoints, polynomial_array)

    return xvals, yvals


def plot_curve(xys, height, ax, nTimes=100, r=0.3, color="blue"):
    xys = sorted(xys, key=lambda x: x[0])
    num_points = len(xys)

    verts = [xys[0]]
    for i, xy in enumerate(xys):
        if i != 0:
            qleft = (xys[i][0] - (xys[i][0] - xys[i - 1][0]) * r, xys[i][1])
            verts += [qleft]
            verts += [xy]

        if i != (num_points - 1):
            qright = (xys[i][0] + (xys[i + 1][0] - xys[i][0]) * r, xys[i][1])
            verts += [qright]
    xvals, yvals = bezier_curve(verts, nTimes=nTimes)

    verts = [[xys[0][0], xys[0][1] - height]]
    for i, xy in enumerate(xys):
        if i != 0:
            qleft = (xys[i][0] - (xys[i][0] - xys[i - 1][0]) * r, xys[i][1] - height)
            verts += [qleft]
            verts += [(xy[0], xy[1] - height)]

        if i != (num_points - 1):
            qright = (xys[i][0] + (xys[i + 1][0] - xys[i][0]) * r, xys[i][1] - height)
            verts += [qright]
    xvals_low, yvals_low = bezier_curve(verts, nTimes=nTimes)

    ax.fill_between(xvals, yvals, yvals_low, color=color)


def plot_curves(xys, height, ax, nTimes=100, r=0.3, color="red"):
    for i, xy in enumerate(xys):
        if i == 0:
            continue
        plot_curve([xys[i - 1], xys[i]], height, ax, nTimes, r, color)


def make_color_palette(dg, columns, color, palette):
    if (color is None) and (palette is not None):
        cmap = plt.get_cmap(palette)
        cols = []
        for i in range(cmap.N):
            rgb = cmap(i)[:3]  # will return rgba, we take only first 3 so we get rgb
            cols += [matplotlib.colors.rgb2hex(rgb) + "aa"]
        keys = dg[columns[0]].drop_duplicates().values
        cmap = {}
        for i, key in enumerate(keys):
            colid = i % len(cols)
            cmap[key] = cols[colid]
        color = lambda x: cmap[x[0][1]]
    elif color is None:
        color = "#cdcdcdaa"
    return color


def order_groups_by_rows(dg, columns, row_order):
    def calc_order(row, columns, row_order):
        s = 0
        for i, col in enumerate(columns):
            col_row_order = [r[1] for r in row_order if r[0] == col]
            rank = np.where(np.isin(col_row_order, row[col]))[0]
            if len(rank) == 0:
                rank = len(col_row_order) + 1
            else:
                rank = rank[0]
            s += rank * np.power(len(columns) - i - 1, 100)
        return s

    if len(row_order) > 0:
        dg["_order"] = dg.apply(lambda x: calc_order(x, columns, row_order), axis=1)
        dg = dg.sort_values(by="_order")
    return dg
