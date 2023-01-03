# finSankey
 Create sankey diagrams from a (cashflow) Excel sheet

## Usage
```python
import pandas as pd
import plotly.io as pio
pio.renderers.default='browser'
from finSankey import data_prep, sankey_to_text, sankey

column_name = 'Monatsdurchschnitt'
title = 'Cashflow<br>Monthly average'

df = pd.read_excel('cashflow_randomized.xlsx',
                   header=0,
                   index_col=None)

# Write to text file
income, expenses, df, data, node_labels, link_sources, link_targets, link_vals = data_prep(df, column_name, label_includes_value=False)
sankey_to_text(node_labels, link_sources, link_targets, link_vals)

# Plot
income, expenses, df, data, node_labels, link_sources, link_targets, link_vals = data_prep(df, column_name)
fig = sankey(data, title)
fig.show()
```
