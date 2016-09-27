from flask import Flask, render_template, request
import comp as comp
import json

import pandas as pd
import numpy as np
import matplotlib, scipy, time, MySQLdb
from collections import Counter
from datetime import datetime
import cufflinks as cf

import plotly
import plotly.offline as py
import plotly.graph_objs as go

app = Flask(__name__)
app.debug = True

users=comp.users
photos = go.Bar(
    x=users, y=comp.photos,
    marker=dict(
        color='blue'),
    name='photos'
)

stickers = go.Bar(
    x=users, y=comp.stickers,
    marker=dict(
        color='green'),
    name='stickers'
)

videos = go.Bar(
    x=users, y=comp.videos,
    marker=dict(
        color='red'),
    name='videos'
)
titles = go.Bar(
    x=users, y=comp.videos,
    marker=dict(
        color='purple'),
    name='titles'
)

user1 = go.Histogram(
    x=comp.utimes.loc[comp.utimes['name'] == 'user1'].date.dt.hour,
    name='user1'
)
user2 = go.Histogram(
    x=comp.utimes.loc[comp.utimes['name'] == 'user2'].date.dt.hour,
    name='user2'
)
user3 = go.Histogram(
    x=comp.utimes.loc[comp.utimes['name'] == 'user3'].date.dt.hour,
    name='user3'
)

@app.route('/')
def index():
    graphs = [

        dict(   # --- most active users --
            data=[
                go.Bar(
                    x=[x[0] for x in comp.totals.head().itertuples()],
                    y=[x[1] for x in comp.totals.head().itertuples()],
                    marker=dict(
                        color='rgb(55, 83, 109)')
                ),
            ],
            layout=go.Layout(
                title='Most Active Users',
                xaxis=dict(
                    title='Name'),
                yaxis=dict(
                    title='Chat Actions')
            )
        ),

        dict(   # --- by hours histogram
            data=[
                dict(
                x=comp.tots.date.dt.hour,
                type='histogram',
                orientation='v',
                histfunc='avg'
                ),
            ],
            layout=go.Layout(
                title='Chat Activity By Hour - CET',
                xaxis=dict(
                    title='Time of Day'),
                yaxis=dict(
                    title='Messages'),

            )
        ),

        dict( # --- by user hours histogram
            data = [user1, user2, user3],
            layout = dict(
                title='Chat Interactions By User / Hour - CET',
                barmode='overlay',
                bargap=0.25,
                bargroupgap=0.3,
                updatemenus=list([
                    dict(
                        yanchor='top',
                        buttons=list([

                            dict(
                                args=['visible', [True, True, True]],
                                label='All',
                                method='restyle'
                            ),
                            dict(
                                args=['visible', [True, False, False]],
                                label='User1',
                                method='restyle'
                            ),
                            dict(
                                args=['visible', [False, True, False]],
                                label='User2',
                                method='restyle'
                            ),
                            dict(
                                args=['visible', [False, False, True]],
                                label='User3',
                                method='restyle'
                            )
                            ])
                        )
                    ])
                )
        ),

        dict(   # --- popular types
            data=[
                dict(
                    labels=[x[0] for x in comp.chattypes.itertuples()],
                    values=[x[1] for x in comp.chattypes.itertuples()],
                    type='pie',
                    hoverinfo = 'label+percent',
                    textinfo = '',
                    textposition='outside+values',
                    rotation=180
                ),
            ],
            layout=dict(
                title='Most Popular Chat Types'
            )
        ),

        dict( # --- other media
            data=[photos,stickers,videos,titles],
            layout=dict(
                title='Other Shared Media',
                updatemenus=list([
                    dict(
                        yanchor='top',
                        buttons=list([
                            dict(
                                args=['visible', [True, True, True, True]],
                                label='All',
                                method='restyle'
                            ),
                            dict(
                                args=['visible', [True, False, False, False]],
                                label='Photos',
                                method='restyle'
                            ),
                            dict(
                                args=['visible', [False, True, False, False]],
                                label='Stickers',
                                method='restyle'
                            ),

                            dict(
                                args=['visible', [False, False, True, False]],
                                label='Videos',
                                method='restyle'
                            ),
                        ]),
                    )
                ])
                )
        )

    ]


    # Add "iuser2" to each of the graphs to pass up to the client
    # for templating
    iuser2 = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]
    idhist = ['graph-{}'.format(i) for i, _ in enumerate(graphs[2])]

    # Convert the figures to JSON
    # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
    # objects to their JSON equivalents
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    histJSON = json.dumps(graphs[2], cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('layouts/index.html',
                           iuser2=iuser2,
                           graphJSON=graphJSON,
                           histJSON=histJSON,
                           idhist=idhist)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999, debug=True)
