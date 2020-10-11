# A python library for drawing alluvial diagram based on pandas

![example](https://raw.githubusercontent.com/skojaku/pandas-alluvial-diagram/main/figs/example.png)

# Motivation

Alluvial diagram is a powerful way to visualize different groupings of the same data.
Although there are a plethora of visualization methods such as `plotly`, `d3.js` and `matplotlib`, they require a specially formatted data, resulting many lines of codes.

I am developing a tool that takes `pandas`, a widely-used data table, to visualize a beautiful alluvial diagram, without relaying on non-standard libraries.
The tool is under development and any contribution is more than welcome:smirk_cat:.  

# Installation

Download the repository

```
git clone https://github.com/skojaku/pandas-alluvial-diagram.git
```

The package sits in `allu_pandas` directory. You can import the package by


```
import sys
import os
sys.path.append(os.path.abspath(os.path.join(`<path to the directory in which allu_pandas locates>`))
```

Or install:

(conda)
```
conda develop . 
```

(pip)
```
pip install . 
```

# Usage

```python
import allu_pandas

allu_pandas.draw(df, columns, palette = "Set1")
```

`allu_pandas.draw` draws an alluvial diagram, with flows between groups specified by columns of `df`.
Specifically, each group is a set of records with the same column (say `col`) and value in the column (say `v`).
The groups are ordered horizontally based on `col` and vertically based on `v`.
The height of a group represents the number of records that the group contains.

- `df`: pandas.DataFrame
- `columns`: list of str
    - Name of columns
- `colore_by`: str
    - The flow will be colored by df[color_by]. If not specified, columns[0] will be used.
- `palette`: str or list
    - Palette of colors. Flow will be colored based on the left-most group. Acceptable color code are hex (e.g., "#aabbcc"), name of colors (e.g., "red"), and the name of matplolib color palette (e.g., "Set1" and "tab10").
- `ax`: matplotlib.pyplo.gca
- `margin`: vertical margin between groups
- `label_pad`: margin between the flow and labels 
- `row_order`: list of tuples
    - Each tuple is (`col`, `v`), where `col` is the column name and `v` is the value of the group. Force a group with row_order[i] to be placed above row_order[i+1]


# Examples

- [Get started](https://github.com/skojaku/pandas-alluvial-diagram/blob/main/notebooks/example1.ipynb)
- [Advanced](https://github.com/skojaku/pandas-alluvial-diagram/blob/main/notebooks/example2.ipynb)
- [Beyond](https://github.com/skojaku/pandas-alluvial-diagram/blob/main/notebooks/example3.ipynb)

# Sample data
- penguins: https://github.com/allisonhorst/penguins (compiled by https://github.com/mwaskom/seaborn-data)
- taitanic: https://github.com/mwaskom/seaborn-data/blob/master/titanic.csv
