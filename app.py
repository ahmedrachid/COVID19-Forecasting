import dash
import dash_core_components as dcc
import dash_html_components as html
import json
import datetime
import time
import pandas as pd
import plotly.graph_objs as go
import plotly.figure_factory as ff
from urllib.request import urlopen
import numpy as np
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_table
import plotly.express as px
from dash.dependencies import Input, Output, State
from plotly import tools
from datetime import date
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from itertools import combinations
from dash.exceptions import PreventUpdate
from sir import SIRModel
from seir import SEIRModel
from seird import SEIRDModel

print(dcc.__version__) 

external_stylesheets = ["https://fonts.googleapis.com/css?family=Overpass:300,300i",
                        "https://cdn.rawgit.com/plotly/dash-app-stylesheets/dab6f937fd5548cebf4c6dc7e93a10ac438f5efb/dash-technical-charting.css",
                        dbc.themes.BOOTSTRAP]
                        
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True

def get_data(country):
    
    df_confirmed = pd.read_csv('./COVID-19-master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv', sep = ',')
    df_deaths = pd.read_csv('./COVID-19-master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv', sep = ',')
    df_recovered = pd.read_csv('./COVID-19-master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv', sep = ',')

    df_confirmed = df_confirmed[df_confirmed['Country/Region']== country]
    df_confirmed.index=df_confirmed["Country/Region"]
    df_confirmed=df_confirmed.drop(columns=["Country/Region",'Lat','Long','Province/State'])
    df_confirmed=df_confirmed.groupby("Country/Region").sum()

    df_deaths = df_deaths[df_deaths['Country/Region']== country]
    df_deaths.index=df_deaths["Country/Region"]
    df_deaths=df_deaths.drop(columns=["Country/Region",'Lat','Long','Province/State'])
    df_deaths=df_deaths.groupby("Country/Region").sum()

    df_recovered = df_recovered[df_recovered['Country/Region']== country]
    df_recovered.index=df_recovered["Country/Region"]
    df_recovered=df_recovered.drop(columns=["Country/Region",'Lat','Long','Province/State'])
    df_recovered=df_recovered.groupby("Country/Region").sum()

    return df_confirmed, df_deaths, df_recovered

def get_countries():
    df_confirmed = pd.read_csv('./COVID-19-master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv', sep = ',')
    return df_confirmed['Country/Region'].unique().tolist()

def data_cases_countries():
    df = pd.read_csv('./COVID-19-master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv', sep = ',')
    df = df.sort_values(by='6/15/20', ascending=False)
    countries = df['Country/Region'].values.tolist()[:20]
    number_cases = df['6/15/20'].values.tolist()[:20]
    return countries, number_cases

def data_deaths_countries():
    df = pd.read_csv('./COVID-19-master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv', sep = ',')
    list_country = ['US',
    'Brazil',
    'Russia',
    'India',
    'United Kingdom',
    'Spain',
    'Italy',
    'Peru',
    'Iran',
    'France',
    'Germany',
    'Turkey',
    'Chile',
    'Mexico',
    'Pakistan',
    'Saudi Arabia']
    deaths_cases = df[df['Country/Region'].isin(list_country)]['6/15/20'].values.tolist()
    return deaths_cases

def data_recovered_countries():
    df = pd.read_csv('./COVID-19-master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv', sep = ',')
    list_country = ['US',
    'Brazil',
    'Russia',
    'India',
    'United Kingdom',
    'Spain',
    'Italy',
    'Peru',
    'Iran',
    'France',
    'Germany',
    'Turkey',
    'Chile',
    'Mexico',
    'Pakistan',
    'Saudi Arabia']
    recovered_cases = df[df['Country/Region'].isin(list_country)]['6/15/20'].values.tolist()
    return recovered_cases


def pie_data(country):
    df_confirmed = pd.read_csv('./COVID-19-master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv', sep = ',')
    df_confirmed = df_confirmed[df_confirmed['Country/Region']== country]
    states = df_confirmed['Province/State'].values.tolist()
    number_states = df_confirmed['6/15/20'].values.tolist()
    return states, number_states

def get_data_country():
    df_confirmed = pd.read_csv('./COVID-19-master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv', sep = ',')
    return df_confirmed

def get_population(country):
    df_population = pd.read_csv('./COVID-19-master/csse_covid_19_data/UID_ISO_FIPS_LookUp_Table.csv')
    population  = df_population[df_population['Country_Region']==country]['Population'].values.tolist()[0]
    return population
#List of countries
list_countries = get_countries()
countries, number_cases = data_cases_countries()
deaths_cases = data_deaths_countries()
recovered_cases = data_recovered_countries()
app.layout = html.Div([
    html.Div(
        [
            html.Div("Ahmed Rachid HAZOURLI"),
            html.Div("Anes MEKKI"),
            html.Div("Anis BOUAZIZ")
        ],
        style={
            "textAlign": "right",
            "color": "gray",
            "textSize":'60px',
        }
    ),
    html.H1("COVID Dashboard",style={'text-align':'center', 'margin-top':'10px'}),
        html.Div([
            html.H4("Country"),
            dcc.Dropdown(
                id="country-dropdown",
                options=[{'label':i,'value':i} for i in list_countries],
                searchable=True,
                multi = False,
                value='France'
            ),
            
            ],
            style = {'display': 'inline-block','width': '33%'}),

        html.Div([
            html.H4("Model"),
            dcc.Dropdown(
                id="models-dropdown",
                options=[{'label':"SIR",'value':"SIR"},
                {'label':"SEIR",'value':"SEIR"}, 
                {'label':"SEIRD",'value':"SEIRD"},
                ],
                searchable=True,
                multi = False,
                value='SIR'
            ),
            ],
            style = {'display': 'inline-block','width': '33%'}),

    html.Div([
        dcc.Graph(id='map-covid'),

        dcc.Graph(
                id='covid-countries',
                figure={
                    "data": [
                        {
                            "x": countries,
                            "y": number_cases,
                            "type": "bar",
                            'name': 'Confirmed Cases'
                        },
                        {
                            "x": countries,
                            "y": recovered_cases,
                            "type": "bar",
                            'name': 'Recovered Cases'
                        }
                    ],
                    "layout": {
                        'title': 'COVID over the world',
                        "xaxis": {"title": "Country"},
                        "yaxis": {"title": "Cases"},
                    },
                },
                style={'height':600},

        ),
        dcc.Graph(id="covid-pie",
            style={'height':600},
        ),
        dcc.Graph(id="covid-graph",
            style={'height':600},
        ),      
        html.Br(),
        html.H2('MODEL', style={'text-align':'center', 'margin-top':'10px'}),
        dcc.Graph(id="sir-graph",
            style={'height':600},
        ),    
         html.H2('MODEL', style={'text-align':'center', 'margin-top':'10px'}),
        dcc.Graph(id="sir-graph-final",
            style={'height':600},
        ),

    ]),          
],
    style={
        'width': '100%',
        'max-width': '1200',
        'margin-left': 'auto',
        'margin-right': 'auto',
        'font-family': 'overpass',
        'background-color': '#F3F3F3',
        'padding': '40',
        'padding-top': '10',
        'padding-bottom': '10',
    },)


#Update our Graph 
@app.callback([Output("covid-graph","figure"),
                Output("covid-pie","figure"),
                Output("sir-graph","figure"),
                Output('sir-graph-final', 'figure'),
                Output('map-covid', 'figure')
                ],
              [Input("country-dropdown","value"),
              Input('models-dropdown', 'value') 
              ])
def update_graph(country, model):
    try:
        df_confirmed, df_deaths, df_recovered = get_data(country)
        states, number_states = pie_data(country)

        pie_chart = {
            "data": [go.Pie(labels=states,
                        values=number_states,
                        textinfo='label')],
            "layout": go.Layout(
                            margin={"l": 300, "r": 300, 't':280},
                            legend={"x": 1, "y": 0.7})
                            
        }


        dates = df_confirmed.columns.tolist()
        list_confirmed = df_confirmed.values.tolist()[0]
        list_deaths = df_deaths.values.tolist()[0]
        list_recovered = df_recovered.values.tolist()[0]

        graph_lines = {
            'data': [ 
            go.Scatter(
                x=dates,
                y=list_confirmed,
                name="Confirmed Cases",
                mode='lines',
            ),
            go.Scatter(
                x=dates,
                y=list_deaths,
                name="Deaths Cases",
                mode='lines',
            ),
            go.Scatter(
                x=dates,
                y=list_recovered,
                name="Recovered Cases",
                mode='lines',
            ),

            ],
            'layout': go.Layout(

                yaxis={
                    'title': "COVID",
                },
                margin={'l': 70, 'b': 40, 't': 10, 'r': 0},
                hovermode='closest'
            )
        }
        N = get_population(country)
        ydata = df_confirmed.loc[country].values.tolist()
        xdata = [i for i in range(len(df_confirmed.columns))]
        y = np.array(ydata, dtype=float)
        x = np.array(xdata, dtype=float)

        if model == 'SIR':
            sir = SIRModel(N=N)
            sir.fit(x, y)
            xdata = [i for i in range(365)]
            x = np.array(xdata, dtype=float)
            S = sir.predict(x)[0]
            I = sir.predict(x)[1]
            R = sir.predict(x)[2]
        if model == 'SEIR':
            sir = SEIRModel(N=N)
            sir.fit(x, y)
            xdata = [i for i in range(365)]
            x = np.array(xdata, dtype=float)
            S = sir.predict(x)[0]
            I = sir.predict(x)[2]
            R = sir.predict(x)[3]
        if model == 'SEIRD':
            sir = SEIRDModel(N=N)
            sir.fit(x, y)
            xdata = [i for i in range(365)]
            x = np.array(xdata, dtype=float)
            S = sir.predict(x)[0]
            I = sir.predict(x)[2]
            R = sir.predict(x)[3]
            D = sir.predict(x)[4]
        

        graph_sir = {
            'data': [ 
            go.Scatter(
                x=xdata,
                y=I,
                name="Model Infected",
                mode='lines',
            ),

            go.Scatter(
                x=xdata,
                y=ydata,
                name="Real Infected",
                mode='lines',
            ),
            ],
            'layout': go.Layout(

                yaxis={
                    'title': "COVID",
                },
                margin={'l': 70, 'b': 40, 't': 10, 'r': 0},
                hovermode='closest',
            )
        }
        graph_sir_final = {
            'data': [ 
            go.Scatter(
                x=xdata,
                y=S,
                name="Suspected ",
                mode='lines',
            ),
            go.Scatter(
                x=xdata,
                y=I,
                name="Infected",
                mode='lines',
            ),
            go.Scatter(
                x=xdata,
                y=R,
                name="Recovered",
                mode='lines',
            ),
            ],
            'layout': go.Layout(

                yaxis={
                    'title': "COVID",
                },
                yaxis_type='linear',

                margin={'l': 70, 'b': 40, 't': 10, 'r': 0},
                hovermode='closest',
            )
        }

        df_country = get_data_country()
   #     px.set_mapbox_access_token("pk.eyJ1IjoicHduZWRhaG1lZCIsImEiOiJja2JqMjkzZnowbDNmMnhsc2ZzYm50cXBsIn0.nhyet_O9a8jF5Mg5VmACsQ")
        
        mapbox_access_token = "pk.eyJ1IjoicHduZWRhaG1lZCIsImEiOiJja2JqMjkzZnowbDNmMnhsc2ZzYm50cXBsIn0.nhyet_O9a8jF5Mg5VmACsQ"

        fig = go.Figure(go.Scattermapbox(
                lat=df_country['Lat'],
                lon=df_country['Long'],
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size=12
                ),
                text=df_country['6/15/20'],
            ))

        fig.update_layout(
            autosize=True,
            hovermode='closest',
            mapbox=dict(
                accesstoken=mapbox_access_token,
                bearing=0,
                center=dict(
                    lat=46.2276,
                    lon=2.2137
                ),
                pitch=0,
                zoom=5
            ),
        )
    except Exception as error:
        print(error)
        raise

    return graph_lines, pie_chart, graph_sir, graph_sir_final, fig
if __name__ == '__main__':
    app.run_server(host='0.0.0.0',debug=True, port=8050)