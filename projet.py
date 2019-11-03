# https://perso.esiee.fr/~courivad/PythonViz/

# ------------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------------

import pandas as pd
import numpy as np
import plotly_express as px

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# ------------------------------------------------------------------------------------
# Data
# ------------------------------------------------------------------------------------

CSV = pd.read_csv("Sex_Offenders_completed.csv")

AGES = CSV["age"]

AGE = 36
AGES = np.sort(AGES.unique())
DATA_AGE = {age:CSV.query("age == @age") for age in AGES}

# ------------------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------------------

if __name__ == '__main__':

    APP = dash.Dash(__name__)

    FIG_HISTO_1 = px.histogram(CSV, x="age", color="race", title='Age repartition', nbins=20)
    FIG_HISTO_2 = px.histogram(CSV, x="race", color="race", title='Number of offence per race')

    FIG_AGE = px.scatter(DATA_AGE[AGE], x="height (m)", y="weight (Kg)",
                         title='''Weight vs height relation of the offenders
                               ({} years old)'''.format(AGE),
                         color='race',
                         size='age',
                         hover_data=['birth date', 'block'],
                         hover_name="name")

    FIG_HISTO_AVG = px.histogram(CSV, x="race", y='age', color="race",
                                 title="Age average per race",
                                 histfunc='avg')

    px.set_mapbox_access_token('pk.eyJ1IjoiYmFwdGlzdGVhZGFtIiwiYSI6ImNrMmdwdmNncDByZWIzbG9lbTExMmY5YmkifQ.D7vXobtSiwy2Z-_OAtUoeQ')
    FIG_MAP = px.scatter_mapbox(CSV, lat="lat", lon="lon",
                                title='Map of the offences',
                                color="race",
                                size="age",
                                hover_name='name',
                                hover_data=['birth date', 'block'],
                                zoom=9)

    FIG_HISTO_1.update_layout(legend_orientation="h", legend=dict(x=-0.01, y=1.115))
    FIG_HISTO_2.update_layout(legend_orientation="h", legend=dict(x=-0.01, y=1.1), showlegend=False)
    FIG_AGE.update_layout(legend_orientation="h", legend=dict(x=-0.01, y=1.1))
    FIG_HISTO_AVG.update_layout(legend_orientation="h", legend=dict(x=-0.01, y=1.1))
    FIG_MAP.update_layout(legend_orientation="h", legend=dict(x=-0.01, y=1.1))

    APP.layout = html.Div(children=[
        html.H1(id='H1', children='Data analysis of sex offenders in Chicago in 2017',
                style={'textAlign': 'center', 'color': '#7FDBFF'}),
        # ------------------------------------------------------------------------------------
        # Presentation
        # ------------------------------------------------------------------------------------
        html.Div([
            html.Div([
                html.Div(
                    children='''We will analyse the data of sex offenders registered during the year
                    2017 in chicago to try to find recuring factors or criteria that may help to assert 
                    what lead someone to do sex offences. As I have downloaded this dataset two years 
                    ago, it no longer is available on the internet. But here is a link to the updated 
                    version of the same dataset : '''
                    ),
                html.A("Link to external site",
                       href='https://www.chicago.gov/city/en/dataset/registered_sex_offenders.html',
                       target="_blank"
                      ),
                ], style={'width': '93%', 'display': 'inline-block',
                          'marginTop':'2%', 'marginBottom':'1%'},
                    ),
            html.Div(
                children=['''This dataset contains the first and last name, the age and birth date,
                the height, the weight, the gender, the race of the offender, the block where the 
                offence has been perpetrated and if the victim is a minor. The datas were completed 
                with the coordinates of the blocks using the Nominatim API and the weight  and height
                where converted from the imperial system to the international system.'''],
                style={'width': '93%', 'display': 'inline-block', 'marginBottom':'1%'},
            ),
            html.Div([
                html.Label('''We will be looking at this one criteria at the time.
                Choose the one to bring out :'''),
                dcc.Dropdown(
                    id="criteria",
                    options=[
                        {'label':"Race", 'value':'race'},
                        {'label':"Gender", 'value':'gender'},
                        {'label':"Minor and Major victims", 'value':'victim'},
                        {'label':"Total", 'value':'None'}
                    ],
                    value='race',
                ),
                ], style={'width': '92.5%', 'display': 'inline-block', 'marginBottom':'3%'}
                    ),
            # ------------------------------------------------------------------------------------
            # Basics charts
            # ------------------------------------------------------------------------------------
            html.Div(
                children='''Let's first look at some general charts.''',
                style={'width': '90%', 'display': 'inline-block'},
            ),
            ], style={'width': '95%', 'display': 'inline-block', 'marginLeft':'5%'},
                ),
        html.Div([
            dcc.Graph(
                id='graph_histo_1',
                figure=FIG_HISTO_1
            ),
        ], style={'width': '50%', 'display': 'inline-block'}
                ),
        html.Div([
            dcc.Graph(
                id='graph_histo_2',
                figure=FIG_HISTO_2
            )
            ], style={'width': '49%', 'display': 'inline-block'}
                ),
        # ------------------------------------------------------------------------------------
        # Age slider
        # ------------------------------------------------------------------------------------
        html.Div(
            children='''We have an overview of the matter, sex offenders are mostly people between
            35 and 60 years old and a huge majority are black people. By playing with the criteria, we see 
            that sex offences are almost solely perpetrated by men, and sadly there is a preference for 
            minor victims.''',
            style={'width': '88%', 'display': 'inline-block', 'marginLeft':'5%', 'marginTop':'1%'},
        ),
        html.Div(
            children='''Now, let's have a look at the physical caracteristics of the offenders
            depending on their age.''',
            style={'width': '88%', 'display': 'inline-block', 'marginLeft':'5%', 'marginTop':'2%'},
        ),

        dcc.Graph(
            id='graph_scatter',
            figure=FIG_AGE
        ),
        html.Div([
            html.Label('Age of the offenders :'),
            dcc.Slider(
                disabled=False,
                id="year-slider",
                min=20,
                max=97,
                step=None,
                marks={
                    20: {'label': '20'},
                    26: {'label': '26'},
                    28: {'label': '28'},
                    29: {'label': '29'},
                    30: {'label': '30'},
                    31: {'label': '31'},
                    32: {'label': '32'},
                    33: {'label': '33'},
                    34: {'label': '34'},
                    35: {'label': '35'},
                    36: {'label': '36'},
                    37: {'label': '37'},
                    38: {'label': '38'},
                    39: {'label': '39'},
                    40: {'label': '40'},
                    41: {'label': '41'},
                    42: {'label': '42'},
                    43: {'label': '43'},
                    44: {'label': '44'},
                    45: {'label': '45'},
                    46: {'label': '46'},
                    47: {'label': '47'},
                    48: {'label': '48'},
                    49: {'label': '49'},
                    50: {'label': '50'},
                    51: {'label': '51'},
                    52: {'label': '52'},
                    53: {'label': '53'},
                    54: {'label': '54'},
                    55: {'label': '55'},
                    56: {'label': '56'},
                    57: {'label': '57'},
                    58: {'label': '58'},
                    59: {'label': '59'},
                    60: {'label': '60'},
                    61: {'label': '61'},
                    62: {'label': '62'},
                    63: {'label': '63'},
                    64: {'label': '64'},
                    65: {'label': '65'},
                    66: {'label': '66'},
                    67: {'label': '67'},
                    68: {'label': '68'},
                    69: {'label': '69'},
                    70: {'label': '70'},
                    71: {'label': '71'},
                    72: {'label': '72'},
                    73: {'label': '73'},
                    74: {'label': '74'},
                    75: {'label': '75'},
                    76: {'label': '76'},
                    77: {'label': '77'},
                    78: {'label': '78'},
                    79: {'label': '79'},
                    80: {'label': '80'},
                    82: {'label': '82'},
                    83: {'label': '83'},
                    85: {'label': '85'},
                    86: {'label': '86'},
                    97: {'label': '97'}
                },
                value=36,
            ),
            html.Div(id='just to show labels on slider', children='''.'''),

            html.Button('Play', id='play', disabled=False),
            html.Button('Pause', id='pause', disabled=False),

            dcc.Interval(id='interval',
                         interval=1*1000, # in milliseconds
                         n_intervals=0,
                         disabled=True,
                        ),
            ], style={'width': '88%', 'display': 'inline-block', 'marginLeft':'5%', }
                ),
        html.Div(style={'width': '5%', 'display': 'inline-block'}),
        html.Div(
            children='''This shows us that weight or height doesn't influence the probability
            of being a sex offender as they range from small to tall and from lightweighted 
            to heavyweighted without that much of a discontinuity. And this, regardless of the 
            age lookted at. We do observe that taller people tends to be heavier, but this is not 
            related to our subject.''',
            style={'width': '88%', 'display': 'inline-block',
                   'marginTop':'2%', 'marginLeft':'5%', 'marginBottom':'2%'},
        ),
        # ------------------------------------------------------------------------------------
        # Customizable chart
        # ------------------------------------------------------------------------------------
        html.Div([
            html.Div(
                children='''This chart display the average of the information selected
                depending on the main criteria selected at the top of this page. It is 
                here for you to play with as it will let you display informations the 
                way you want according to what you want.''',
                style={'color':'#65C9EF', 'marginBottom':'10%'},
            ),
            html.Label('Choose the information you want :'),
            dcc.Dropdown(
                id="avg",
                options=[
                    {'label':"Age", 'value':'age'},
                    {'label':"Weight", 'value':'weight (Kg)'},
                    {'label':"Height", 'value':'height (m)'},
                ],
                value='age',
                style={'marginBottom':'10%'},
            ),
            html.Label('Choose by which criteria the histogram will be colored :'),
            dcc.Dropdown(
                id="color",
                options=[
                    {'label':"Race", 'value':'race'},
                    {'label':"Gender", 'value':'gender'},
                    {'label':"Minor and Major victims", 'value':'victim'},
                ],
                value='race',
            ),
            ], style={'width': '28%', 'display': 'inline-block', 'marginLeft':'5%'}
                ),
        html.Div([
            dcc.Graph(
                id='graph_histo_avg',
                figure=FIG_HISTO_AVG
            )
            ], style={'width': '66%', 'display': 'inline-block', 'vertical-align': 'middle'}
                ),
        html.Div(
            children='''From this histogram, we can extract a lot of information, for example :''',
            style={'width': '88%', 'display': 'inline-block',
                   'marginLeft':'5%', 'marginBottom':'0.5%'},
        ),
        html.Div(
            children='''  - The age average is, as much for all races than for men or women,
            around 50 years old (the average for women do fluctuate the most but it could 
            be argued that this is because of the scarcity of the datas).''',
            style={'width': '88%', 'display': 'inline-block', 'marginLeft':'5%',},
        ),
        html.Div(
            children='''  - Height and weight are the known average for their respective
            race (black people are naturally taller than asians for example).''',
            style={'width': '88%', 'display': 'inline-block', 'marginLeft':'5%',},
        ),
        html.Div(
            children='''  - On average, people that go for major victims are a bit older,
            taller and heavier than the ones going for minor victims (This could be explained 
            by the fact that major victims can actually defend themselves).''',
            style={'width': '88%', 'display': 'inline-block', 'marginLeft':'5%',},
        ),

        # ------------------------------------------------------------------------------------
        # Geolocalisation
        # ------------------------------------------------------------------------------------
        html.Div(
            children='''Finally, let's have a look at where all this offences took place.''',
            style={'width': '88%', 'display': 'inline-block', 'marginLeft':'5%', 'marginTop':'2%'},
        ),
        dcc.Graph(
            id='graph_map',
            figure=FIG_MAP
        ),
        html.Div(
            children='''What can be said about this map ?''',
            style={'width': '88%', 'display': 'inline-block',
                   'marginLeft':'5%', 'marginBottom':'0.5%'},
        ),
        html.Div(
            children='''Offences perpetrated by black people are mostly located
            in the south of the city while offences perpetrated by white and hispanic 
            people are mostly located in the north. But overall, the offences are spread 
            evenly around the city and there is no places that is really "safer" than another.''',
            style={'width': '88%', 'display': 'inline-block', 'marginLeft':'5%',},
        ),
        html.Div(
            children='''In conlusion, there is really no factors that could help to
            assert if someone has a higher probability to become a sex offender than 
            another. If one is a black male between 35 and 60 years old, one could 
            argue that he has a higher probability. But that is still really vague 
            and isn't really helpful. And as height, weight and geolocalisation doesnt 
            matter, we cannot conclude farther than that.''',
            style={'width': '88%', 'display': 'inline-block',
                   'marginLeft':'5%', 'marginTop':'5%', 'marginBottom':'15%'},
        ),
    ])
    # ------------------------------------------------------------------------------------
    # Callbacks
    # ------------------------------------------------------------------------------------

    # ------------- callback Age repartition -------------
    @APP.callback(
        Output('graph_histo_1', 'figure'),
        [Input('criteria', 'value')]
    )
    def update_histo_1(criteria_value):
        if criteria_value == 'None':
            value = None
        else:
            value = str(criteria_value)
        fig = px.histogram(CSV, x="age",
                           color=value,
                           title='Age repartition',
                           nbins=20)
        fig.update_layout(legend_orientation="h", legend=dict(x=-0.01, y=1.115))
        return fig

    # ------------- callback Number of offence -------------
    @APP.callback(
        Output('graph_histo_2', 'figure'),
        [Input('criteria', 'value')]
    )
    def update_histo_2(criteria_value):
        titre = 'Number of offence'
        if criteria_value == 'None':
            value = 'total'
        else:
            value = str(criteria_value)
            titre += ' per {}'.format(value)
        fig = px.histogram(CSV, x=value,
                           color=value,
                           title=titre)
        fig.update_layout(legend_orientation="h", legend=dict(x=-0.01, y=1.1), showlegend=False)
        return fig

    # ------------- callback Age slider -------------
    @APP.callback(
        [Output('graph_scatter', 'figure'),
         Output('play', 'disabled'),
         Output('pause', 'disabled'),
         Output('year-slider', 'disabled')],
        [Input('year-slider', 'value'),
         Input('criteria', 'value')]
    )
    def update_figure(slider_value, dropdown_value):
        titre = 'Weight vs height relation of the offenders'
        if dropdown_value == 'None':
            value = None
            data = CSV
            disabled = True
        else:
            value = str(dropdown_value)
            data = DATA_AGE[slider_value]
            disabled = False
            titre += ' ({} years old)'.format(slider_value)
        fig = px.scatter(data, x="height (m)", y="weight (Kg)",
                         title=titre,
                         color=value,
                         size='age',
                         hover_data=['birth date', 'block'],
                         hover_name="name")
        fig.update_layout(legend_orientation="h", legend=dict(x=-0.01, y=1.1))
        return fig, disabled, disabled, disabled

    # ------------- callback Interval -------------
    @APP.callback(
        Output('year-slider', 'value'),
        [Input('interval', 'n_intervals')]
    )
    def on_tick(n_intervals):
        if n_intervals is None:
            return 0
        elif n_intervals == 0:
            return 36
        return AGES[(n_intervals+1)%len(AGES)]

    # ------------- callback Buttons -------------
    @APP.callback(
        Output('interval', 'disabled'),
        [Input('play', 'n_clicks_timestamp'),
         Input('pause', 'n_clicks_timestamp')]
    )
    def on_click(play, pause):
        if play is None:
            return True
        elif pause is None or int(play) > int(pause):
            return False
        return True

    # ------------- callback Avg chart -------------
    @APP.callback(
        Output('graph_histo_avg', 'figure'),
        [Input('avg', 'value'),
         Input('criteria', 'value'),
         Input('color', 'value')]
    )
    def update_histo_avg(avg_value, criteria_value, color_value):
        avg = str(avg_value)[0].upper()+str(avg_value)[1:]
        titre = '{} average'.format(avg)
        if criteria_value == 'None':
            value = 'total'
        else:
            value = str(criteria_value)
            titre += ' per {}'.format(value)
        fig = px.histogram(CSV, x=value,
                           y=str(avg_value),
                           color=str(color_value),
                           title=titre,
                           histfunc='avg')
        fig.update_layout(legend_orientation="h", legend=dict(x=-0.01, y=1.1))
        return fig

    # ------------- callback Map -------------
    @APP.callback(
        Output('graph_map', 'figure'),
        [Input('criteria', 'value'),]
    )
    def update_map(criteria_value):
        if criteria_value == 'None':
            value = None
        else:
            value = str(criteria_value)
        fig = px.scatter_mapbox(CSV, lat="lat", lon="lon",
                                title='Map of the offences',
                                color=value,
                                size="age",
                                hover_name='name',
                                hover_data=['birth date', 'block'],
                                zoom=9)
        fig.update_layout(legend_orientation="h", legend=dict(x=-0.01, y=1.1))
        return fig

    # ------------------------------------------------------------------------------------
    # RUN APP
    # ------------------------------------------------------------------------------------

    APP.run_server(debug=True)
