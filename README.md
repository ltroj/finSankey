# finSankey
Create sankey diagrams from a (cashflow) Excel sheet.

Returns a plotly plot of your diagram as well as a text file for the popular online diagram builder [SankeyMATIC](https://sankeymatic.com/).

## Input file
See ```cashflow_randomized.xlsx``` as a template spreadsheet file.

## Usage
```python
import pandas as pd
import plotly.io as pio
pio.renderers.default='browser'
from finSankey import data_prep, sankey_to_text, sankey

# Set corresponding column name from input file to evaluate
column_name = 'Monatsdurchschnitt'

# Plot title
title = 'Cashflow<br>Monthly average'

# Build pandas dataframe from input file
df = pd.read_excel('cashflow_randomized.xlsx',
                   header=0,
                   index_col=None)

# Write to text file
income, expenses, df, data, node_labels, link_sources, link_targets, link_vals = data_prep(df, column_name, label_includes_value=False)
sankey_to_text(node_labels, link_sources, link_targets, link_vals)

# Plot diagram using plotly
income, expenses, df, data, node_labels, link_sources, link_targets, link_vals = data_prep(df, column_name)
fig = sankey(data, title)
fig.show()
```
## Outputs

### Plot from ```finSankey.sankey```
![alt text](https://github.com/ltroj/finSankey/blob/main/sankey_plot.png?raw=true)

### Text file from ```finSankey.sankey_to_text```
The resulting text file can be used as an input file on https://sankeymatic.com/.

It follows the simple syntax of ```Source [Amount] Target```.

```
Gehalt/Lohn [418.8] Einkünfte
Kapitalerträge [6.2] Einkünfte
Wertpapier-Erträge [4.5] Kapitalerträge
...
Verkehr & Mobilität [11.7] Treibstoff
Einkünfte [119.8] Wohnen
Wohnen [6.0] Nebenkosten
Nebenkosten [6.1] Strom
Wohnen [106.2] Warmmiete
```
