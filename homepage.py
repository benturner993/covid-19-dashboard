import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go

from datetime import datetime as dt
from data import *
from functions import *
from navbar import Navbar

# Navigation Bar
nav = Navbar()

# Date selector
date_range = html.Div([
    dcc.DatePickerRange(
        id='my-date-picker-range',
        min_date_allowed=dt(2019, 12, 31),
        max_date_allowed=dt(2020, 9, 19),
        initial_visible_month=dt(2019, 12, 31),
        start_date=dt(2019, 12, 31).date(),
        end_date=dt.today(),
        display_format='DD/MM/YYYY',
    )
])

# Main Header
heading = dbc.Container(
    dbc.Row([dbc.Col((html.H1([dbc.Badge("Worldwide Information Centre", color="danger", pill=True, className="ml-1")]),
                      ), align="center", xl=6, lg=6, md=12, sm=12, xs=12),
             dbc.Col((html.H6("Tested:"),
                      html.H4(""),
                      html.H4(id='ww_new_tests_sum', style={'color': 'black', 'font-weight': 'bold'},
                              className="card-subtitle"),
                      ), xl=2, lg=2, md=4, sm=4, xs=4),
             dbc.Col((html.H6("Confirmed Cases:"),
                      html.H4(""),
                      html.H4(id='ww_new_cases_sum', style={'color': 'orange', 'font-weight': 'bold'},
                              className="card-subtitle"),
                      ), xl=2, lg=2, md=4, sm=4, xs=4),
             dbc.Col((html.H6("Deaths:"),
                      html.H4(""),
                      html.H4(id='ww_new_deaths_sum', style={'color': 'red', 'font-weight': 'bold'},
                              className="card-subtitle"),
                      ), xl=2, lg=2, md=4, sm=4, xs=4), ])
    , className="mt-4", fluid=True)

dates = dbc.Container(html.Div([html.Label(["Select Date Range:", date_range])]), className="mt-4", fluid=True)

table = dash_table.DataTable(
    id='table-filtering-be',
    columns=[
        {"name": i, "id": i} for i in (hotspot_table_df.columns)
    ], style_as_list_view=True,
    style_cell={'padding': '4px'},
    style_header={
        'backgroundColor': 'white',
        'fontWeight': 'bold'
    },

    filter_action='custom',
    filter_query=''
)

radio = dcc.RadioItems(
    options=[
        {'label': 'Spinning Globe', 'value': 'orthographic'},
        {'label': 'Map', 'value': 'equirectangular'}
    ],
    id='radioinput',
    value='orthographic',
    labelStyle={'display': 'inline-block'},
    inputStyle={"margin-right": "5px", "margin-left": "10px"}
)

radio1 = dcc.RadioItems(
    options=[
        {'label': 'Actual', 'value': 'actual'},
        {'label': 'Log', 'value': 'log'}
    ],
    id='radioinput1',
    value='actual',
    labelStyle={'display': 'inline-block'},
    inputStyle={"margin-right": "5px", "margin-left": "10px"}
)

radio2 = dcc.RadioItems(
    options=[
        {'label': 'Actual', 'value': 'actual'},
        {'label': 'Log', 'value': 'log'}
    ],
    id='radioinput2',
    value='actual',
    labelStyle={'display': 'inline-block'},
    inputStyle={"margin-right": "5px", "margin-left": "10px"}
)

collapse1 = html.Div([dbc.Button("More Information", id="collapse-button1", className="mb-3", color="light"
                                 ), dbc.Collapse(dbc.Card(dbc.CardBody(card1)),
                                                 id="collapse1", ), ])

collapse2 = html.Div([dbc.Button("More Information", id="collapse-button2", className="mb-3", color="light"
                                 ), dbc.Collapse(dbc.Card(dbc.CardBody(card2)),
                                                 id="collapse2", ), ])

collapse3 = html.Div([dbc.Button("More Information", id="collapse-button3", className="mb-3", color="light"
                                 ), dbc.Collapse(dbc.Card(dbc.CardBody(card3)),
                                                 id="collapse3", ), ])

card1 = dbc.Card(dbc.CardBody([html.Div([
    dcc.Tabs(id='tabs-example123', value='tabgraph2', children=[
        dcc.Tab(label='Daily Deaths', value='tabgraph2'),
        dcc.Tab(label='Total Deaths', value='tabgraph1')
    ], colors={
        "border": "white",
        "primary": "grey",
        "background": "#E9ECEF"
    }),
    html.Br(), # style={'whiteSpace': 'pre-wrap'} html.P('Why no <br/> linebreak?'))
    html.Div(id='tabs-graph-content'), html.Br(), collapse1
])]), inverse=False)  # color="light",

card2 = dbc.Card(dbc.CardBody([html.Div(
    [dcc.Tabs(id='tabs2', value='tabs2tab1',
              children=[dcc.Tab(label='Case Mortality (Per 100k)', value='tabs2tab1'),
                        dcc.Tab(label='Transmission Rate', value='tabs2tab3'), ], colors={
            "border": "white",
            "primary": "grey",
            "background": "#E9ECEF"
        }),
     html.Div(id='tabs2-content'), html.Br(), collapse2])]), inverse=False)  # color="light",

card3 = dbc.Card(
    dbc.CardBody([
        html.Div([dcc.Tabs(id='tabs1', value='tab-1', children=[dcc.Tab(label='Latest News', value='tab-1'),
                                                                dcc.Tab(label='Trending',
                                                                        value='tab-2'), ], colors={
            "border": "white",
            "primary": "grey",
            "background": "#E9ECEF"
        }),
                  html.Div(id='tabs1-content'), html.Br(), collapse3])]), inverse=False)  # color="light",

page_main_body = dbc.Container(
    dbc.Row([dbc.Col(card1, xl=3, lg=12, md=12, sm=12, xs=12),
             dbc.Col(card2, xl=6, lg=12, md=12, sm=12, xs=12),
             dbc.Col(card3, xl=3, lg=12, md=12, sm=12, xs=12),
             ], align='stretch'
            ), className="mt-4", fluid=True)

# Footnote
disclaimer = dbc.Container(dbc.Col(html.P(disclaimer_text, id="wpdisclaimer")), className="mt-4", fluid=True)


def Homepage():
    layout = html.Div([
        nav,
        heading,
        dates,
        page_main_body,
        disclaimer,
    ], style={'backgroundColor': 'white'})
    return layout


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])
server=app.server
app.layout = Homepage()

if __name__ == "__main__":
    app.run_server()


# Plot 1
def build_cumulative_deaths(start_date, end_date):
    data = {"type": "line",
            "x": covid_dataset.loc[(pd.to_datetime(covid_dataset['date']) >= pd.to_datetime(start_date)) & (
                    pd.to_datetime(covid_dataset['date']) <= pd.to_datetime(end_date))].groupby('date')[
                'new_deaths'].sum().reset_index().sort_values(by='date')['date'],
            "y": covid_dataset.loc[(pd.to_datetime(covid_dataset['date']) >= pd.to_datetime(start_date)) & (
                    pd.to_datetime(covid_dataset['date']) <= pd.to_datetime(end_date))].groupby('date')[
                'new_deaths'].sum().reset_index().sort_values(by='date')['new_deaths'].cumsum(),
            'marker': {"color": "black"},
            "yaxis": "y1",
            "name": "Cumulative Deaths"
            }

    data1 = {"type": "line",
             "x": covid_dataset.loc[(pd.to_datetime(covid_dataset['date']) >= pd.to_datetime(start_date)) & (
                     pd.to_datetime(covid_dataset['date']) <= pd.to_datetime(end_date))].groupby('date')[
                 'new_deaths'].sum().reset_index().sort_values(by='date')['date'],
             "y": covid_dataset.loc[(pd.to_datetime(covid_dataset['date']) >= pd.to_datetime(start_date)) & (
                     pd.to_datetime(covid_dataset['date']) <= pd.to_datetime(end_date))].groupby('date')[
                 'new_cases'].sum().reset_index().sort_values(by='date')['new_cases'].cumsum(),
             'marker': {"color": "red"},
             "yaxis": "y2",
             "name": "Cumulative Cases"
             }
    plot1 = dcc.Graph(
        id='example-graph',
        figure={
            'data': [data, data1],
            'layout': go.Layout(margin=dict(l=40, r=40, t=0, b=40),
                                # title='Cumulative Number of Deaths',
                                legend={'orientation': 'v', 'x': 0, 'y': 1},
                                yaxis={'title': 'C. Number of Deaths', 'showgrid': False},
                                xaxis={'title': 'Date', 'showgrid': False},
                                yaxis2={'title': 'C. Number of Cases',
                                        'overlaying': 'y',
                                        'side': 'right',
                                        'showgrid': False,
                                        'showline': False},
                                autosize=True
                                ),
        },
        config={'responsive': False}
    )
    return plot1

def build_cumulative_log_deaths(start_date, end_date):
    data = {"type": "line",
            "x": covid_dataset.loc[(pd.to_datetime(covid_dataset['date']) >= pd.to_datetime(start_date)) & (
                    pd.to_datetime(covid_dataset['date']) <= pd.to_datetime(end_date))].groupby('date')[
                'new_deaths'].sum().reset_index().sort_values(by='date')['date'],
            "y": np.log(covid_dataset.loc[(pd.to_datetime(covid_dataset['date']) >= pd.to_datetime(start_date)) & (
                    pd.to_datetime(covid_dataset['date']) <= pd.to_datetime(end_date))].groupby('date')[
                'new_deaths'].sum().reset_index().sort_values(by='date')['new_deaths'].cumsum()),
            'marker': {"color": "black"},
            "yaxis": "y1",
            "name": "Log Cumulative Deaths"
            }

    data1 = {"type": "line",
             "x": covid_dataset.loc[(pd.to_datetime(covid_dataset['date']) >= pd.to_datetime(start_date)) & (
                     pd.to_datetime(covid_dataset['date']) <= pd.to_datetime(end_date))].groupby('date')[
                 'new_deaths'].sum().reset_index().sort_values(by='date')['date'],
             "y": np.log(covid_dataset.loc[(pd.to_datetime(covid_dataset['date']) >= pd.to_datetime(start_date)) & (
                     pd.to_datetime(covid_dataset['date']) <= pd.to_datetime(end_date))].groupby('date')[
                 'new_cases'].sum().reset_index().sort_values(by='date')['new_cases'].cumsum()),
             'marker': {"color": "red"},
             "yaxis": "y2",
             "name": "Log Cumulative Cases"
             }
    plot1 = dcc.Graph(
        id='example-graph',
        figure={
            'data': [data, data1],
            'layout': go.Layout(margin=dict(l=40, r=40, t=0, b=40),
                                # title='Cumulative Number of Deaths',
                                legend={'orientation': 'v', 'x': 0, 'y': 1},
                                yaxis={'title': 'C. Number of Deaths', 'showgrid': False},
                                xaxis={'title': 'Date', 'showgrid': False},
                                yaxis2={'title': 'C. Number of Cases',
                                        'overlaying': 'y',
                                        'side': 'right',
                                        'showgrid': False,
                                        'showline': False},
                                autosize=True
                                ),
        },
        config={'responsive': False}
    )
    return plot1


# Plot 2
def build_daily_deaths(start_date, end_date):
    data = {"type": "line",
            "x": covid_dataset.loc[(pd.to_datetime(covid_dataset['date']) >= pd.to_datetime(start_date)) & (
                    pd.to_datetime(covid_dataset['date']) <= pd.to_datetime(end_date))].groupby('date')[
                'new_deaths'].sum().reset_index()['date'],
            "y": covid_dataset.loc[(pd.to_datetime(covid_dataset['date']) >= pd.to_datetime(start_date)) & (
                    pd.to_datetime(covid_dataset['date']) <= pd.to_datetime(end_date))].groupby('date')[
                'new_deaths'].sum().reset_index()['new_deaths'],
            'marker': {"color": "black"},
            "yaxis": "y1",
            "name": "Daily Deaths"

            }

    data1 = {"type": "line",
             "x": covid_dataset.loc[(pd.to_datetime(covid_dataset['date']) >= pd.to_datetime(start_date)) & (
                     pd.to_datetime(covid_dataset['date']) <= pd.to_datetime(end_date))].groupby('date')[
                 'new_deaths'].sum().reset_index()['date'],
             "y": covid_dataset.loc[(pd.to_datetime(covid_dataset['date']) >= pd.to_datetime(start_date)) & (
                     pd.to_datetime(covid_dataset['date']) <= pd.to_datetime(end_date))].groupby('date')[
                 'new_cases'].sum().reset_index()['new_cases'],
             'marker': {"color": "red"},
             "yaxis": "y2",
             "name": "Daily Cases"

             }

    plot2 = dcc.Graph(
        id='example-graph',
        figure={
            'data': [data, data1],
            'layout': go.Layout(margin=dict(l=40, r=40, t=0, b=40),
                                # title='Daily Number of Deaths',
                                legend={'orientation': 'v', 'x': 0, 'y': 1},
                                yaxis={'title': 'Number of Deaths', 'showgrid': False},
                                #xaxis={'title': 'Date', 'showgrid': False},
                                yaxis2={'title': 'Number of Cases',
                                        'overlaying': 'y',
                                        'side': 'right',
                                        'showline': False,
                                        'showgrid': False},
                                autosize=True
                                )
        }
    )

    return plot2

def build_daily_log_deaths(start_date, end_date):
    data = {"type": "line",
            "x": covid_dataset.loc[(pd.to_datetime(covid_dataset['date']) >= pd.to_datetime(start_date)) & (
                    pd.to_datetime(covid_dataset['date']) <= pd.to_datetime(end_date))].groupby('date')[
                'new_deaths'].sum().reset_index()['date'],
            "y": np.log(covid_dataset.loc[(pd.to_datetime(covid_dataset['date']) >= pd.to_datetime(start_date)) & (
                    pd.to_datetime(covid_dataset['date']) <= pd.to_datetime(end_date))].groupby('date')[
                'new_deaths'].sum().reset_index()['new_deaths']),
            'marker': {"color": "black"},
            "yaxis": "y1",
            "name": "Log Daily Deaths"

            }

    data1 = {"type": "line",
             "x": covid_dataset.loc[(pd.to_datetime(covid_dataset['date']) >= pd.to_datetime(start_date)) & (
                     pd.to_datetime(covid_dataset['date']) <= pd.to_datetime(end_date))].groupby('date')[
                 'new_deaths'].sum().reset_index()['date'],
             "y": np.log(covid_dataset.loc[(pd.to_datetime(covid_dataset['date']) >= pd.to_datetime(start_date)) & (
                     pd.to_datetime(covid_dataset['date']) <= pd.to_datetime(end_date))].groupby('date')[
                 'new_cases'].sum().reset_index()['new_cases']),
             'marker': {"color": "red"},
             "yaxis": "y2",
             "name": "Log Daily Cases"

             }

    plot2 = dcc.Graph(
        id='example-graph',
        figure={
            'data': [data, data1],
            'layout': go.Layout(margin=dict(l=40, r=40, t=0, b=40),
                                # title='Daily Number of Deaths',
                                legend={'orientation': 'v', 'x': 0, 'y': 1},
                                yaxis={'title': 'Number of Deaths', 'showgrid': False},
                                #xaxis={'title': 'Date', 'showgrid': False},
                                yaxis2={'title': 'Number of Cases',
                                        'overlaying': 'y',
                                        'side': 'right',
                                        'showline': False,
                                        'showgrid': False},
                                autosize=True
                                )
        }
    )

    return plot2


def choropleth_map(map_type, start_date, end_date):
    if start_date is None:
        start_date = pd.to_datetime(dt(2019, 12, 31))

    # Define world average
    cases_data = {"type": "choropleth",
                  "locations": case_fatality_df(covid_dataset, 'date', start_date, end_date, 'case_fatality')[
                      'iso_code'],
                  "z": case_fatality_df(covid_dataset, 'date', start_date, end_date, 'case_fatality')['case_fatality'],
                  "hoverinfo":"case_fatality",
                  "colorscale": [[0.0, 'rgb(26,26,26)'],
                                 [0.1, 'rgb(77,77,77)'],
                                 [0.2, 'rgb(135,135,135)'],
                                 [0.3, 'rgb(186,186,186)'],
                                 [0.4, 'rgb(224,224,224)'],
                                 [0.5, 'rgb(255,255,255)'],
                                 [0.6, 'rgb(253,219,199)'],
                                 [0.7, 'rgb(244,165,130)'],
                                 [0.8, 'rgb(214,96,77)'],
                                 [0.9, 'rgb(178,24,43)'],
                                 [1.0, 'rgb(103,0,31)']]
                  }

    graph = dcc.Graph(
        figure={
            'data': [cases_data],
            'layout': go.Layout(
                #   yaxis={'title': 'Number of Cases'},
                hovermode='closest',
                margin=dict(l=20, r=20, t=20, b=20),
                geo=dict(
                    showframe=False,
                    showcoastlines=False,
                    projection=dict(
                        type=map_type
                    )
                ),
                hoverlabel=dict(
                    bgcolor="white",
                    font_size=12,
                    font_family="Rockwell"
                )
            )
        }
    )
    return graph


def build_hotspot_graph(start_date, end_date):
    data = {"type": "bar",
            "x": hotspot_table_df.loc[(pd.to_datetime(hotspot_table_df['Date']) >= pd.to_datetime(start_date)) & (
                    pd.to_datetime(hotspot_table_df['Date']) <= pd.to_datetime(end_date))]['Country'][:5],
            "y": hotspot_table_df[:5].loc[(pd.to_datetime(hotspot_table_df['Date']) >= pd.to_datetime(start_date)) & (
                    pd.to_datetime(hotspot_table_df['Date']) <= pd.to_datetime(end_date))]['Percentage'][:5],
            'marker': {"color": "grey"},
            "hovertemplate": "Date: " + hotspot_table_df['Date'][:5].astype(str) + "\t" +\
                             "Total Deaths: " + hotspot_table_df['Total Deaths'][:5].astype(str) +  "\t" +\
                             "New Deaths: " + hotspot_table_df['New Deaths'][:5].astype(str),
            "name": "Information"
            }

    plot2 = dcc.Graph(
        id='hotsport-graph',
        figure={
            'data': [data],
            'layout': go.Layout(margin=dict(l=40, r=40, t=0, b=40),
                                # title='Daily Number of Deaths',
                                legend={'orientation': 'v', 'x': 0, 'y': 1},
                                yaxis={'title': 'Percentage of New Deaths (to Total)',
                                       'showgrid': False},
                                xaxis={'title': 'Country', 'showgrid': False},
                                autosize=True
                                )
        }
    )

    return plot2