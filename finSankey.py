# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 21:48:30 2022
"""
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default='browser'


def sankey(data, title):
    # https://plotly.com/python/sankey-diagram/
   
    fig = go.Figure(data=[go.Sankey(
        valueformat = ".0f",
        valuesuffix = " EUR",
        # Define nodes
        node = dict(
          pad = 15,
          thickness = 15,
          line = dict(color = "black", width = 0.5),
          label =  data['node']['label'],
        ),
        # Add links
        link = dict(
          source =  data['link']['source'],
          target =  data['link']['target'],
          value =  data['link']['value'],
    ))])

    fig.update_layout(title_text=title,
                      font_size=10)
    
    return fig


def data_prep(df, column_name, label_includes_value=True):
    df = df[:-1]  # Remove last row
    start = 8-2
    end = 133-2
    income = df.iloc[start:end]
    expenses = df.drop(df.index[start:end])
    
    # Remove rows which equal zero
    income = income[df[column_name] != 0.00]
    expenses = expenses[df[column_name] != 0.00]
    
    # Income

    i = 0
    node_labels = []
    link_sources = []
    link_targets = []
    link_vals = []
    ebenen = []
        
    for index, row in income.iterrows():
        if label_includes_value:
            label = row['Kategorie (Hierarchie)'] + f" ({row[column_name]:.0f})"
        else:
            label = row['Kategorie (Hierarchie)']
            
        node_labels.append(label)
        ebenen.append(row['Ebene'])

        parent_ebene = row['Ebene'] - 1
        
        if row['Ebene'] > 1:
                link_sources.append(i)
                link_vals.append(row[column_name])
                
                all_the_parent_indexes = [i for i,x in enumerate(ebenen) if x==parent_ebene] # => [1, 3]
                parent_index = all_the_parent_indexes[-1]
                
                link_targets.append(parent_index)

        i += 1
        
    # Expenses
    print("i: {}".format(i))

    ebenen = []
    for index, row in expenses.iterrows():
        ebenen.append(row['Ebene'])
        
    deepest = max(ebenen)
    start_index = len(node_labels) - 1
    print("start_index: {}".format(start_index))
    ebenen = []
    
    for index, row in expenses.iterrows():
        if label_includes_value:
            label = row['Kategorie (Hierarchie)'] + f" ({row[column_name]:.0f})"
        else:
            label = row['Kategorie (Hierarchie)']
            
        node_labels.append(label)
        print("node_label: {}".format(row['Kategorie (Hierarchie)']))
        ebenen.append(row['Ebene'])
        
        parent_ebene = row['Ebene'] - 1

        if row['Ebene'] > 1:
            all_the_parent_indexes = [i for i,x in enumerate(ebenen) if x==parent_ebene]
            parent_index = all_the_parent_indexes[-1] + start_index + 1
            print("parent_index: {}".format(parent_index))
            
        elif row['Ebene'] == 1:
            parent_index = 0  # "Einnahmen"
            print("parent_index: {}".format(parent_index))
        
        if row['Ebene'] < deepest:  
            link_sources.append(parent_index)
            link_vals.append(-row[column_name])
            
            link_targets.append(i)
            print("source: {}\ntarget: {}\nval: {}".format(parent_index, i, row[column_name]))
                
        i += 1
        print('------------------------')
        
    data = {
            'node':{
                'label':node_labels,
                },
            'link':{
                'source':link_sources,
                'target':link_targets,
                'value':link_vals
                }
            }
    
    return income, expenses, df, data, node_labels, link_sources, link_targets, link_vals

def sankey_to_text(node_labels, link_sources, link_targets, link_vals):
   
    s = ''
    for source, value, target in zip(link_sources, link_vals, link_targets):
    
        s = s + node_labels[source] + f' [{value:.1f}] ' + node_labels[target] + '\n'
    
    with open('sankey.txt', 'w', encoding='utf8') as f:
        f.write(s)
            
    return f
        


if __name__ == "__main__":

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
    