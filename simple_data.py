# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 21:02:11 2022
"""

import plotly.graph_objects as go
import urllib, json
import plotly.io as pio
pio.renderers.default='browser'


data = {
        'node':{
            'label':[
                'Einnahmen',    # 0
                'Budget',       # 1
                'Ausgabe_1',    # 2
                'Ausgabe_11',   # 3
                'Ausgabe_12',   # 4
                'Ausgabe_2',    # 5
                'Ausgabe_21',   # 6
                'Ausgabe_22'    # 7
                ],
            },
        'link':{
            'source':[
                0,
                1,
                2,
                2,
                1,
                5,
                5
                ],
            'target':[
                1,
                2,
                3,
                4,
                5,
                6,
                7
                ],
            'value':[
                1000.,
                500.,
                250.,
                250.,
                500.,
                250.,
                250.
                ]
            }
        }


fig = go.Figure(data=[go.Sankey(
    valueformat = ".0f",
    valuesuffix = "EUR",
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

fig.update_layout(title_text="Simple Test Data",
                  font_size=10)
fig.show()