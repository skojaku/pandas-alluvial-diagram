# pandas-alluvial-diagram

A python library for drawing alluvial diagram


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

allu_pandas.draw(df, ["species", "island", "sex"], palette = "Set1")
```

`allu_pandas.draw` draws an alluvial diagram, with flows between groups specified by columns of `df`.
Specifically, each group is a set of records with the same column (say `col`) and value in the column (say `v`).
The groups are orderd horizontally based on `col` and vertically based on `v`.
The height of a group represents the number of records that the group contains.

- `df`: pandas.DataFrame
- `columns`: list of str
    - Name of columns
- `color`: str or func
    - Name of color of a function for each flow across multiple groups. A flow starts from the left-most group, go through middle groups and end at the right-most group. If a function is given, the function will receive a list of (`col`, `v`) pairs in order of the groups along the path. For example, if a flow goes along a path of groups, ('col1', 'a'), ('col2', 'x'), ('col3', 'W'), then the function will receive list [('col1', 'a'), ('col2', 'x'), ('col3', 'W')].
- `palette`: str
    - Palette of colors. Flow will be colored based on the left-most group.
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
