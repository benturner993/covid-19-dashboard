import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import dash_table
from datetime import datetime as dt
import pandas as pd
import numpy as np

from data import *
from functions import *
from navbar import Navbar

# Navigation Bar
nav = Navbar()

# Main header
heading = dbc.Container(
    dbc.Row([dbc.Col((html.H1([dbc.Badge("Country Insights Miner", color="danger", pill=True, className="ml-1")]),
                      ), align="center", xl=4, lg=12, md=12, sm=12, xs=12),
             dbc.Col((html.H6("Country:"),
                      html.H4(""),
                      html.H4(id='country', style={'color': 'black', 'font-weight': 'bold'},
                              className="card-subtitle"),
                      ), xl=2, lg=3, md=3, sm=3, xs=3),
             dbc.Col((html.H6("Tested:"),
                      html.H4(""),
                      html.H4(id='country_tests_units', style={'color': 'black', 'font-weight': 'bold'},
                              className="card-subtitle"),
                      ), xl=2, lg=3, md=3, sm=3, xs=3),
             dbc.Col((html.H6("Confirmed Cases:"),
                      html.H4(""),
                      html.H4(id='country_cases', style={'color': 'orange', 'font-weight': 'bold'},
                              className="card-subtitle"),
                      ), xl=2, lg=3, md=3, sm=3, xs=3),
             dbc.Col((html.H6("Deaths:"),
                      html.H4(""),
                      html.H4(id='country_deaths', style={'color': 'red', 'font-weight': 'bold'},
                              className="card-subtitle"),
                      ), xl=2, lg=3, md=3, sm=3, xs=3), ])
    , className="mt-4", fluid=True)

# Date selector
date_range = html.Div([
    dcc.DatePickerRange(
        id='country_dates',
        min_date_allowed=dt(2019, 12, 31),
        max_date_allowed=dt(2020, 9, 19),
        initial_visible_month=dt(2019, 12, 31),
        start_date=dt(2019, 12, 31).date(),
        end_date=dt.today(),
        display_format='DD/MM/YYYY',
    )
])

radio3 = dcc.RadioItems(
    options=[
        {'label': 'Actual', 'value': 'actual'},
        {'label': 'Log', 'value': 'log'}
    ],
    id='radioinput3',
    value='actual',
    labelStyle={'display': 'inline-block'},
    inputStyle={"margin-right": "5px", "margin-left": "10px"}
)

radio4 = dcc.RadioItems(
    options=[
        {'label': 'Actual', 'value': 'actual'},
        {'label': 'Log', 'value': 'log'}
    ],
    id='radioinput4',
    value='actual',
    labelStyle={'display': 'inline-block'},
    inputStyle={"margin-right": "5px", "margin-left": "10px"}
)

# Dropdown menu
dropdown = dbc.Container(html.Div([html.Label(["Select Countries:", dcc.Dropdown(
    id='dropdown',
    options=[{'label': x, 'value': x} for x in covid_dataset['location'].sort_values().unique()],
    value='United Kingdom', multi=True
), "Select Date Range:", date_range])]), className="mt-4", fluid=True)

# Main body
country_table = dash_table.DataTable(
    id='table-filtering-radardata',
    columns=[
        {"name": i, "id": i} for i in (radar_plot_database_df.columns)
    ], style_as_list_view=True,
    style_cell={'padding': '4px'},
    style_header={
        'backgroundColor': 'white',
        'fontWeight': 'bold'
    },

    filter_action='custom',
    filter_query=''
)

collapse1 = html.Div([dbc.Button("More Information", id="collapse-button1", className="mb-3", color="light"
                                 ), dbc.Collapse(dbc.Card(dbc.CardBody(card4)),
    id="collapse1", ), ])

collapse2 = html.Div([dbc.Button("More Information", id="collapse-button2", className="mb-3", color="light"
                                 ), dbc.Collapse(dbc.Card(dbc.CardBody(card5)),
    id="collapse2", ), ])

collapse3 = html.Div([dbc.Button("More Information", id="collapse-button3", className="mb-3", color="light"
                                 ), dbc.Collapse(dbc.Card(dbc.CardBody(card6)),
                                                 id="collapse3", ), ])

card1 = dbc.Card(dbc.CardBody([html.Div([
    dcc.Tabs(id='country_tabs_card1', value='c1tabgraph2', children=[
        # dcc.Tab(label='Daily Tests', value='c1tabgraph1'),
        dcc.Tab(label='Daily Cases', value='c1tabgraph2'),
        dcc.Tab(label='Daily Deaths', value='c1tabgraph3')
    ], colors={
        "border": "white",
        "primary": "grey",
        "background": "#E9ECEF"
    }),
    html.Div(id='country_tabs_card1-content'), html.Br(), collapse1
])]), inverse=False)  # color="light",

card2 = dbc.Card(dbc.CardBody([html.Div(
    [dcc.Tabs(id='c2tabgraph', value='c2tabgraph1',
              children=[dcc.Tab(label='Radar Plot', value='c2tabgraph1'),
                        #dcc.Tab(label='Country Database', value='c2tabgraph2'),
                        ], colors={
            "border": "white",
            "primary": "grey",
            "background": "#E9ECEF"
        }),
     html.Div(id='c2tabgraph1-content'), html.Br(), collapse2
     ])]), inverse=False)  # color="light",

card3 = dbc.Card(dbc.CardBody([html.Div(
    [dcc.Tabs(id='country_tabs_card3', value='c3tabgraph1',
              children=[dcc.Tab(label='Total Population %', value='c3tabgraph1'),
                        # dcc.Tab(label='Population', value='c3tabgraph2'),
                        dcc.Tab(label='Male Population %', value='c3tabgraph3'),
                        dcc.Tab(label='Female Population %', value='c3tabgraph4'), ], colors={
            "border": "white",
            "primary": "grey",
            "background": "#E9ECEF"
        }),
     html.Div(id='country_tabs_card3-content'), html.Br(), collapse3
     ])]),
    inverse=False)  # color="light",

page_main_body = dbc.Container(
    dbc.Row([dbc.Col(card1, xl=4, lg=12, md=12, sm=12, xs=12),
             dbc.Col(card2, xl=4, lg=12, md=12, sm=12, xs=12),
             dbc.Col(card3, xl=4, lg=12, md=12, sm=12, xs=12),
             ], align='stretch'
            ), className="mt-4", fluid=True)

# Footnote
disclaimer = dbc.Container(dbc.Col(html.H6(disclaimer_text, id="disclaimer")), className="mt-4", fluid=True)


def CountryPage():
    layout = html.Div([
        nav,
        heading,
        dropdown,
        page_main_body,
        disclaimer
    ], style={'backgroundColor': 'white'})
    return layout


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])
server=app.server
app.layout = CountryPage()

if __name__ == "__main__":
    app.run_server()

def build_deaths_graph(country, start_date, end_date):

    ''' Function to create the number of deaths graph'''

    # Create a list for dictionaries
    data_plot_cases_list = []

    if type(country) == str:

        # Define world average
        cases_data = {"type": "line", "x": covid_dataset.loc[(covid_dataset['location'] == country) &
                                                             (pd.to_datetime(covid_dataset['date']) <= pd.to_datetime(
                                                                 end_date)) &
                                                             (pd.to_datetime(covid_dataset['date']) >= pd.to_datetime(
                                                                 start_date))]['date'],
                      'marker': {"color": "black"},
                      "y": covid_dataset.loc[(covid_dataset['location'] == country) &
                                             (pd.to_datetime(covid_dataset['date']) <= pd.to_datetime(end_date)) &
                                             (pd.to_datetime(covid_dataset['date']) >= pd.to_datetime(start_date))][
                          'new_deaths'],
                      "name": '{} Cases'.format(country)}

        # Append
        data_plot_cases_list.append(cases_data)

    elif type(country) == list:

        # For each country in dropdown selected
        for u, v in zip(graph_colours, country):
            # Define world average
            cases_data = {"type": "line", "x": covid_dataset.loc[(covid_dataset['location'] == v) &
                                                                 (pd.to_datetime(
                                                                     covid_dataset['date']) <= pd.to_datetime(
                                                                     end_date)) &
                                                                 (pd.to_datetime(
                                                                     covid_dataset['date']) >= pd.to_datetime(
                                                                     start_date))]['date'],
                          'marker': {"color": u},
                          "y": covid_dataset.loc[(covid_dataset['location'] == v) &
                                                 (pd.to_datetime(covid_dataset['date']) <= pd.to_datetime(end_date)) &
                                                 (pd.to_datetime(covid_dataset['date']) >= pd.to_datetime(start_date))][
                              'new_deaths'],
                          "name": '{} Deaths'.format(v)}

            # Append
            data_plot_cases_list.append(cases_data)

    graph = dcc.Graph(
        figure={
            'data': data_plot_cases_list,
            'layout': go.Layout(margin=dict(l=80, r=80, t=20, b=40),
                                # title='xxx',
                                legend={'orientation': 'v', 'x': 0, 'y': 1},
                                yaxis={'title': 'Number of Deaths', 'showgrid': False},
                                xaxis={'title': 'Time', 'showgrid': False}
                                )
        }
    )
    return graph

def build_deaths_log_graph(country, start_date, end_date):

    ''' Function to create the number of deaths graph'''

    # Create a list for dictionaries
    data_plot_cases_list = []

    if type(country) == str:

        # Define world average
        cases_data = {"type": "line", "x": covid_dataset.loc[(covid_dataset['location'] == country) &
                                                             (pd.to_datetime(covid_dataset['date']) <= pd.to_datetime(
                                                                 end_date)) &
                                                             (pd.to_datetime(covid_dataset['date']) >= pd.to_datetime(
                                                                 start_date))]['date'],
                      'marker': {"color": "black"},
                      "y": np.log(covid_dataset.loc[(covid_dataset['location'] == country) &
                                             (pd.to_datetime(covid_dataset['date']) <= pd.to_datetime(end_date)) &
                                             (pd.to_datetime(covid_dataset['date']) >= pd.to_datetime(start_date))][
                          'new_deaths']),
                      "name": '{} Cases'.format(country)}

        # Append
        data_plot_cases_list.append(cases_data)

    elif type(country) == list:

        # For each country in dropdown selected
        for u, v in zip(graph_colours, country):
            # Define world average
            cases_data = {"type": "line", "x": covid_dataset.loc[(covid_dataset['location'] == v) &
                                                                 (pd.to_datetime(
                                                                     covid_dataset['date']) <= pd.to_datetime(
                                                                     end_date)) &
                                                                 (pd.to_datetime(
                                                                     covid_dataset['date']) >= pd.to_datetime(
                                                                     start_date))]['date'],
                          'marker': {"color": u},
                          "y": np.log(covid_dataset.loc[(covid_dataset['location'] == v) &
                                                 (pd.to_datetime(covid_dataset['date']) <= pd.to_datetime(end_date)) &
                                                 (pd.to_datetime(covid_dataset['date']) >= pd.to_datetime(start_date))][
                              'new_deaths']),
                          "name": '{} Deaths'.format(v)}

            # Append
            data_plot_cases_list.append(cases_data)

    graph = dcc.Graph(
        figure={
            'data': data_plot_cases_list,
            'layout': go.Layout(margin=dict(l=80, r=80, t=40, b=40),
                                # title='xxx',
                                legend={'orientation': 'v', 'x': 0, 'y': 1},
                                yaxis={'title': 'Log Number of Deaths', 'showgrid': False},
                                xaxis={'title': 'Time', 'showgrid': False}
                                )
        }
    )
    return graph


def build_confirmed_graph(country, start_date, end_date):

    ''' Function to create the number of deaths graph'''

    # Create a list for dictionaries
    data_plot_cases_list = []

    if type(country) == str:

        # Define world average
        cases_data = {"type": "line", "x": covid_dataset.loc[(covid_dataset['location'] == country) &
                                                             (pd.to_datetime(covid_dataset['date']) <= pd.to_datetime(
                                                                 end_date)) &
                                                             (pd.to_datetime(covid_dataset['date']) >= pd.to_datetime(
                                                                 start_date))]['date'],
                      'marker': {"color": "black"},
                      "y": covid_dataset.loc[(covid_dataset['location'] == country) &
                                             (pd.to_datetime(covid_dataset['date']) <= pd.to_datetime(end_date)) &
                                             (pd.to_datetime(covid_dataset['date']) >= pd.to_datetime(start_date))][
                          'new_cases'],
                      "name": '{} Cases'.format(country)}

        # Append
        data_plot_cases_list.append(cases_data)

    elif type(country) == list:

        # For each country in dropdown selected
        for u, v in zip(graph_colours, country):
            # Define world average
            cases_data = {"type": "line", "x": covid_dataset.loc[(covid_dataset['location'] == v) &
                                                                 (pd.to_datetime(
                                                                     covid_dataset['date']) <= pd.to_datetime(
                                                                     end_date)) &
                                                                 (pd.to_datetime(
                                                                     covid_dataset['date']) >= pd.to_datetime(
                                                                     start_date))]['date'],
                          'marker': {"color": u},
                          "y": covid_dataset.loc[(covid_dataset['location'] == v) &
                                                 (pd.to_datetime(covid_dataset['date']) <= pd.to_datetime(end_date)) &
                                                 (pd.to_datetime(covid_dataset['date']) >= pd.to_datetime(start_date))][
                              'new_cases'],
                          "name": '{} Cases'.format(v)}

            # Append
            data_plot_cases_list.append(cases_data)

    graph = dcc.Graph(
        figure={
            'data': data_plot_cases_list,
            'layout': go.Layout(margin=dict(l=80, r=80, t=40, b=40),
                                # title='xxx',
                                legend={'orientation': 'v', 'x': 0, 'y': 1},
                                yaxis={'title': 'Number of Cases', 'showgrid': False},
                                xaxis={'title': 'Time', 'showgrid': False}
                                )
        }
    )
    return graph

def build_confirmed_log_graph(country, start_date, end_date):
    ''' Function to create the number of deaths graph'''

    # Create a list for dictionaries
    data_plot_cases_list = []

    if type(country) == str:

        # Define world average
        cases_data = {"type": "line", "x": covid_dataset.loc[(covid_dataset['location'] == country) &
                                                             (pd.to_datetime(covid_dataset['date']) <= pd.to_datetime(
                                                                 end_date)) &
                                                             (pd.to_datetime(covid_dataset['date']) >= pd.to_datetime(
                                                                 start_date))]['date'],
                      'marker': {"color": "black"},
                      "y": np.log(covid_dataset.loc[(covid_dataset['location'] == country) &
                                             (pd.to_datetime(covid_dataset['date']) <= pd.to_datetime(end_date)) &
                                             (pd.to_datetime(covid_dataset['date']) >= pd.to_datetime(start_date))][
                          'new_cases']),
                      "name": '{} Cases'.format(country)}

        # Append
        data_plot_cases_list.append(cases_data)

    elif type(country) == list:

        # For each country in dropdown selected
        for u, v in zip(graph_colours, country):
            # Define world average
            cases_data = {"type": "line", "x": covid_dataset.loc[(covid_dataset['location'] == v) &
                                                                 (pd.to_datetime(
                                                                     covid_dataset['date']) <= pd.to_datetime(
                                                                     end_date)) &
                                                                 (pd.to_datetime(
                                                                     covid_dataset['date']) >= pd.to_datetime(
                                                                     start_date))]['date'],
                          'marker': {"color": u},
                          "y": np.log(covid_dataset.loc[(covid_dataset['location'] == v) &
                                                 (pd.to_datetime(covid_dataset['date']) <= pd.to_datetime(end_date)) &
                                                 (pd.to_datetime(covid_dataset['date']) >= pd.to_datetime(start_date))][
                              'new_cases']),
                          "name": '{} Cases'.format(v)}

            # Append
            data_plot_cases_list.append(cases_data)

    graph = dcc.Graph(
        figure={
            'data': data_plot_cases_list,
            'layout': go.Layout(margin=dict(l=80, r=80, t=40, b=40),
                                # title='xxx',
                                legend={'orientation': 'v', 'x': 0, 'y': 1},
                                yaxis={'title': 'Log Number of Cases', 'showgrid': False},
                                xaxis={'title': 'Time', 'showgrid': False}
                                )
        }
    )
    return graph


def build_tested_graph(country, start_date, end_date):

    ''' Function to create the number of deaths graph'''

    # Create a list for dictionaries
    data_plot_cases_list = []

    if type(country) == str:

        # Define world average
        cases_data = {"type": "line", "x": covid_dataset.loc[(covid_dataset['location'] == country) &
                                                             (pd.to_datetime(covid_dataset['date']) <= pd.to_datetime(
                                                                 end_date)) &
                                                             (pd.to_datetime(covid_dataset['date']) >= pd.to_datetime(
                                                                 start_date))]['date'],
                      'marker': {"color": "black"},
                      "y": covid_dataset.loc[(covid_dataset['location'] == country) &
                                             (pd.to_datetime(covid_dataset['date']) <= pd.to_datetime(end_date)) &
                                             (pd.to_datetime(covid_dataset['date']) >= pd.to_datetime(start_date))][
                          'new_tests'],
                      "name": '{} Cases'.format(country)}

        # Append
        data_plot_cases_list.append(cases_data)

    elif type(country) == list:

        # For each country in dropdown selected
        for u, v in zip(graph_colours, country):
            # Define world average
            cases_data = {"type": "line", "x": covid_dataset.loc[(covid_dataset['location'] == v) &
                                                                 (pd.to_datetime(
                                                                     covid_dataset['date']) <= pd.to_datetime(
                                                                     end_date)) &
                                                                 (pd.to_datetime(
                                                                     covid_dataset['date']) >= pd.to_datetime(
                                                                     start_date))]['date'],
                          'marker': {"color": u},
                          "y": covid_dataset.loc[(covid_dataset['location'] == v) &
                                                 (pd.to_datetime(covid_dataset['date']) <= pd.to_datetime(end_date)) &
                                                 (pd.to_datetime(covid_dataset['date']) >= pd.to_datetime(start_date))][
                              'new_tests'],
                          "name": '{} Cases'.format(v)}

            # Append
            data_plot_cases_list.append(cases_data)

    graph = dcc.Graph(
        figure={
            'data': data_plot_cases_list,
            'layout': go.Layout(margin=dict(l=80, r=80, t=40, b=40),
                                # title='xxx',
                                yaxis={'title': 'Number of Tests', 'showgrid': False},
                                legend={'orientation': 'v', 'x': 0, 'y': 1},
                                xaxis={'title': 'Time', 'showgrid': False}
                                )
        }
    )
    return graph


def build_average_life_expectancy(country):
    ''' Function to create the average population graph'''

    # Create a list for dictionaries
    data_plot_list = []

    # Define world average
    data = {"type": "bar", "x": wbdf4['Population Rates'],
            "y": wbdf4['World'],
            "name": 'World Average',
            'marker': {"color": "grey"}, }

    # Append world average
    data_plot_list.append(data)

    try:

        if type(country) == str:

            new_dataset = {"type": "bar", "x": wbdf4['Population Rates'],
                           "y": wbdf4[country],
                           'marker': {"color": "black"},
                           "name": '{}'.format(country)}
            data_plot_list.append(new_dataset)

        elif type(country) == list:

            # For each country in dropdown selected
            for u, v in zip(graph_colours, country):
                # Create new dictionary item
                new_dataset = {"type": "bar",
                               "x": wbdf4['Population Rates'],
                               "y": wbdf4[v],
                               'marker': {"color": u},
                               "name": '{}'.format(v)}

                # Append to list
                data_plot_list.append(new_dataset)

    except KeyError:

        data_plot_list = data_plot_list

    graph = dcc.Graph(
        figure={
            'data': data_plot_list,
            'layout': go.Layout(
                # title='{} Population Statistics vs Benchmark Averages'.format(country),
                margin=dict(l=80, r=80, t=40, b=40),
                yaxis={'title': 'Percentage of Total Population', 'showgrid': False},
                xaxis={'showgrid': False},
                legend={'orientation': 'v', 'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )
    return graph


def build_population_actuals(country):
    ''' Function to create the average population graph'''

    # Create a list for dictionaries
    data_plot_list = []

    try:

        if type(country) == str:

            new_dataset = {"type": "bar", "x": population_numbers_df['Population'],
                           "y": population_numbers_df[country],
                           'marker': {"color": "black"},
                           "name": '{}'.format(country)}
            data_plot_list.append(new_dataset)

        elif type(country) == list:

            # For each country in dropdown selected
            for u, v in zip(graph_colours, country):
                # Create new dictionary item
                new_dataset = {"type": "bar",
                               "x": population_numbers_df['Population'],
                               "y": population_numbers_df[v],
                               'marker': {"color": u},
                               "name": '{}'.format(v)}

                # Append to list
                data_plot_list.append(new_dataset)

    except KeyError:

        data_plot_list = data_plot_list

    graph = dcc.Graph(
        figure={
            'data': data_plot_list,
            'layout': go.Layout(
                yaxis={'title': 'Total Population', 'showgrid': False},
                margin=dict(l=80, r=80, t=40, b=40),
                legend={'orientation': 'v', 'x': 0, 'y': 1},
                xaxis={'showgrid': False},
                hovermode='closest'
            )
        }
    )
    return graph


def build_average_life_expectancy(country):
    ''' Function to create the average population graph'''

    # Create a list for dictionaries
    data_plot_list = []

    # Define world average
    data = {"type": "bar", "x": wbdf4['Population Rates'],
            "y": wbdf4['World'],
            "name": 'World Average',
            'marker': {"color": "grey"}, }

    # Append world average
    data_plot_list.append(data)

    try:

        if type(country) == str:

            new_dataset = {"type": "bar", "x": wbdf4['Population Rates'],
                           "y": wbdf4[country],
                           'marker': {"color": "black"},
                           "name": '{}'.format(country)}
            data_plot_list.append(new_dataset)

        elif type(country) == list:

            # For each country in dropdown selected
            for u, v in zip(graph_colours, country):
                # Create new dictionary item
                new_dataset = {"type": "bar",
                               "x": wbdf4['Population Rates'],
                               "y": wbdf4[v],
                               'marker': {"color": u},
                               "name": '{}'.format(v)}

                # Append to list
                data_plot_list.append(new_dataset)

    except KeyError:

        data_plot_list = data_plot_list

    graph = dcc.Graph(
        figure={
            'data': data_plot_list,
            'layout': go.Layout(
                # title='{} Population Statistics vs Benchmark Averages'.format(country),
                yaxis={'title': 'Percentage of Total Population', 'showgrid': False},
                margin=dict(l=80, r=40, t=40, b=40),
                xaxis={'showgrid': False},
                legend={'orientation': 'v', 'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )
    return graph


def build_radar_plot(country):
    plot_list = []

    if type(country) == str:
        i = country
        data_list = {"type": "scatterpolar",
                     "r": [radar_plot_df(covid_dataset, i)['population_percentile_rank'].values[0],
                           radar_plot_df(covid_dataset, i)['population_density_percentile_rank'].values[0],
                           radar_plot_df(covid_dataset, i)['diabetes_prevalence_percentile_rank'].values[0],
                           radar_plot_df(covid_dataset, i)['gdp_per_capita_percentile_rank'].values[0],
                           #radar_plot_df(covid_dataset, i)['hospital_beds_per_100k_percentile_rank'].values[0],
                           radar_plot_df(covid_dataset, i)['median_age_percentile_rank'].values[0]],
                     "theta": ['Population', 'Population Density', 'Diabetes Prevalence', 'GDP Per Capita',
                               #'Hospital Beds Per 100k',
                               'Median Age'],
                     "fill": "toself",
                     'marker': {"color": "black"},
                     "name": i
                     }

        plot_list.append(data_list)

    if type(country) == list:
        for u, v in zip(graph_colours, country):
            data_list = {"type": "scatterpolar",
                         "r": [radar_plot_df(covid_dataset, v)['population_percentile_rank'].values[0],
                               radar_plot_df(covid_dataset, v)['population_density_percentile_rank'].values[0],
                               radar_plot_df(covid_dataset, v)['diabetes_prevalence_percentile_rank'].values[0],
                               radar_plot_df(covid_dataset, v)['gdp_per_capita_percentile_rank'].values[0],
                               #radar_plot_df(covid_dataset, v)['hospital_beds_per_100k_percentile_rank'].values[0],
                               radar_plot_df(covid_dataset, v)['median_age_percentile_rank'].values[0]],
                         "theta": ['Population', 'Population Density', 'Diabetes Prevalence', 'GDP Per Capita',
                                   #'Hospital Beds Per 100k',
                                   'Median Age'],
                         "fill": "toself",
                         'marker': {"color": u},
                         "name": v
                         }

            plot_list.append(data_list)

    graph = dcc.Graph(figure={
        'data': plot_list,
        'layout': go.Layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            showlegend=False
        )})

    return graph


def build_population_male_actuals(country):
    ''' Function to create the average population graph'''

    # Create a list for dictionaries
    data_plot_list = []

    # Define world average
    data = {"type": "bar", "x": population_male_numbers_df['Population'],
            "y": population_male_numbers_df['World'],
            "name": 'World Average',
            'marker': {"color": "grey"}, }

    # Append world average
    data_plot_list.append(data)

    try:

        if type(country) == str:

            new_dataset = {"type": "bar", "x": population_male_numbers_df['Population'],
                           "y": population_male_numbers_df[country],
                           'marker': {"color": "black"},
                           "name": '{}'.format(country)}
            data_plot_list.append(new_dataset)

        elif type(country) == list:

            # For each country in dropdown selected
            for u, v in zip(graph_colours, country):
                # Create new dictionary item
                new_dataset = {"type": "bar",
                               "x": population_male_numbers_df['Population'],
                               "y": population_male_numbers_df[v],
                               'marker': {"color": u},
                               "name": '{}'.format(v)}

                # Append to list
                data_plot_list.append(new_dataset)

    except KeyError:

        data_plot_list = data_plot_list

    graph = dcc.Graph(
        figure={
            'data': data_plot_list,
            'layout': go.Layout(
                # title='{} Population Statistics vs Benchmark Averages'.format(country),
                yaxis={'title': 'Total Population', 'showgrid': False},
                xaxis={'showgrid': False},
                margin=dict(l=80, r=40, t=40, b=40),
                legend={'orientation': 'v', 'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )
    return graph


def build_population_female_actuals(country):
    ''' Function to create the average population graph'''

    # Create a list for dictionaries
    data_plot_list = []

    # Define world average
    data = {"type": "bar", "x": population_female_numbers_df['Population'],
            "y": population_female_numbers_df['World'],
            "name": 'World Average',
            'marker': {"color": "grey"}, }

    # Append world average
    data_plot_list.append(data)

    try:

        if type(country) == str:

            new_dataset = {"type": "bar", "x": population_female_numbers_df['Population'],
                           "y": population_female_numbers_df[country],
                           'marker': {"color": "black"},
                           "name": '{}'.format(country)}
            data_plot_list.append(new_dataset)

        elif type(country) == list:

            # For each country in dropdown selected
            for u, v in zip(graph_colours, country):
                # Create new dictionary item
                new_dataset = {"type": "bar",
                               "x": population_female_numbers_df['Population'],
                               "y": population_female_numbers_df[v],
                               'marker': {"color": u},
                               "name": '{}'.format(v)}

                # Append to list
                data_plot_list.append(new_dataset)

    except KeyError:

        data_plot_list = data_plot_list

    graph = dcc.Graph(
        figure={
            'data': data_plot_list,
            'layout': go.Layout(
                # title='{} Population Statistics vs Benchmark Averages'.format(country),
                yaxis={'title': 'Total Population', 'showgrid': False},
                margin=dict(l=80, r=40, t=40, b=40),
                legend={'orientation': 'v', 'x': 0, 'y': 1},
                xaxis={'showgrid': False},
                hovermode='closest'
            )
        }
    )
    return graph