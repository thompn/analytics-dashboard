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

garagely = go.Histogram(
    x=comp.utimes.loc[comp.utimes['name'] == 'Garagely'].date.dt.hour,
    name='Garagely'
)
ds = go.Histogram(
    x=comp.utimes.loc[comp.utimes['name'] == 'C'].date.dt.hour,
    name='Ds'
)
simon = go.Histogram(
    x=comp.utimes.loc[comp.utimes['name'] == '.'].date.dt.hour,
    name='qx'
)
abdul = go.Histogram(
    x=comp.utimes.loc[comp.utimes['name'].isin(['raheem','ABDUL',\
                                    'Abdul GREAZE +61'])].date.dt.hour,
    name='Abdul'
)
ian = go.Histogram(
    x=comp.utimes.loc[comp.utimes['name'].isin(['I','Ian'])].date.dt.hour,
    name='Ian'
)
ah = go.Histogram(
    x=comp.utimes.loc[comp.utimes['name'] == 'AH'].date.dt.hour,
    name='Ash'
)
ben = go.Histogram(
    x=comp.utimes.loc[comp.utimes['name'] == 'Ben'].date.dt.hour,
    name='Ben'
)
tony = go.Histogram(
    x=comp.utimes.loc[comp.utimes['name'] == 'Tony'].date.dt.hour,
    name='Tony'
)
luke = go.Histogram(
    x=comp.utimes.loc[comp.utimes['name'].isin(['L','Luke',\
                                'lxk'])].date.dt.hour,
    name='Luke'
)
helder = go.Histogram(
    x=comp.utimes.loc[comp.utimes['name'] == 'Slow'].date.dt.hour,
    name='Slow'
)
henri = go.Histogram(
    x=comp.utimes.loc[comp.utimes['name'] == 'Zorro'].date.dt.hour,
    name='Henri'
)
wops = go.Histogram(
    x=comp.utimes.loc[comp.utimes['name'] == 'Wops'].date.dt.hour,
    name='Wops'
)
vast = go.Histogram(
    x=comp.utimes.loc[comp.utimes['name'] == 'Wops'].date.dt.hour,
    name='Vast'
)
eu = go.Histogram(
    x=comp.utimes.loc[comp.utimes['name'].isin(['L','Luke','lxk','Wops', \
                                        'Garagely','Zorro', 'Slow','Tony', \
                                        'Ben', 'AH', 'raheem','ABDUL', \
                                        'Abdul GREAZE +61', '.'])].date.dt.hour,
    name='Europeans'
)
noneu = go.Histogram(
    x=comp.utimes.loc[comp.utimes['name'].isin(['Vast','C','Ian','I','L','Luke',\
                                    'lxk'])].date.dt.hour,
    name='Non-EU'
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
            data = [eu, noneu, garagely, ds, simon, abdul, ian, ah, ben, \
                    tony, luke, helder, henri, wops, vast],
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
                                args=['visible', [True, True, True, True, True,\
                                                True, True, True, True, True,\
                                                True, True, True, True, True]],
                                label='All',
                                method='restyle'
                            ),
                            dict(
                                args=['visible', [True, False, False, False,\
                                                False, False, False, False,\
                                                False, False, False, False,\
                                                False, False, False]],
                                label='Europeans',
                                method='restyle'
                            ),
                            dict(
                                args=['visible', [False, True, False, False,\
                                                False, False, False, False,\
                                                False, False, False,False,\
                                                False, False, False]],
                                label='Non-Europeans',
                                method='restyle'
                            ),
                            dict(
                                args=['visible', [False, False, True, False,\
                                                False, False, False, False,\
                                                False, False, False, False,\
                                                False, False, False]],
                                label='Garagely',
                                method='restyle'
                            ),
                            dict(
                                args=['visible', [False, False, False, True,\
                                                False, False, False, False,\
                                                False, False, False, False,\
                                                False, False, False]],
                                label='Ds',
                                method='restyle'
                            ),
                            dict(
                                args=['visible', [False, False, False, False,\
                                                True, False, False, False,\
                                                False, False, False, False,\
                                                False, False, False]],
                                label='qx',
                                method='restyle'
                            ),
                            dict(
                                args=['visible', [False, False, False, False,\
                                                False, True, False, False,\
                                                False, False, False, False,\
                                                False, False, False]],
                                label='Abdul',
                                method='restyle'
                            ),
                            dict(
                                args=['visible', [False, False, False, False,\
                                                False, False, True, False,\
                                                False, False, False, False,\
                                                False, False, False]],
                                label='Ian',
                                method='restyle'
                            ),
                            dict(
                                args=['visible', [False, False, False, False,\
                                                False, False, False, True,\
                                                False, False, False, False,\
                                                False, False, False]],
                                label='Ash',
                                method='restyle'
                            ),
                            dict(
                                args=['visible', [False, False, False, False,\
                                                False, False, False, False,\
                                                True, False, False, False,\
                                                False, False, False]],
                                label='Ben',
                                method='restyle'
                            ),
                            dict(
                                args=['visible', [False, False, False, False,\
                                                False, False, False, False,\
                                                False, True, False, False,\
                                                False, False, False]],
                                label='Tony',
                                method='restyle'
                            ),
                            dict(
                                args=['visible', [False, False, False, False,\
                                                False, False, False, False,\
                                                False, False, True, False,\
                                                False, False, False]],
                                label='Luke',
                                method='restyle'
                            ),
                            dict(
                                args=['visible', [False, False, False, False,\
                                                False, False, False, False,\
                                                False, False, False, True,\
                                                False, False, False]],
                                label='Helder',
                                method='restyle'
                            ),
                            dict(
                                args=['visible', [False, False, False, False,\
                                                False, False, False, False,\
                                                False, False, False, False,\
                                                True, False, False]],
                                label='Henri',
                                method='restyle'
                            ),
                            dict(
                                args=['visible', [False, False, False, False,\
                                                False, False, False, False,\
                                                False, False, False, False,\
                                                False, True, False]],
                                label='Wops',
                                method='restyle'
                            ),
                            dict(
                                args=['visible', [False, False, False, False,\
                                                False, False, False, False,\
                                                False, False, False, False,\
                                                False, False, True]],
                                label='Vast',
                                method='restyle'
                            )
                        ]),
                    )
                ]),
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


    # Add "ids" to each of the graphs to pass up to the client
    # for templating
    ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]
    idhist = ['graph-{}'.format(i) for i, _ in enumerate(graphs[2])]

    # Convert the figures to JSON
    # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
    # objects to their JSON equivalents
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    histJSON = json.dumps(graphs[2], cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('layouts/index.html',
                           ids=ids,
                           graphJSON=graphJSON,
                           histJSON=histJSON,
                           idhist=idhist)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999, debug=True)
