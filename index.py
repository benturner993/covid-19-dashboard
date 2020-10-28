import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd

from homepage import *
from countrypage import *
from homepage import Homepage

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])
server=app.server
app.title = 'COVID-19 Tracking Centre'

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id = 'url', refresh = False),
    html.Div(id = 'page-content')
])

# Navbar
@app.callback(Output('page-content', 'children'),
            [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/countrypage':
        return CountryPage()
    else:
        return Homepage()

# Deaths time
@app.callback(
    Output('deaths_graph_time', 'children'),
    [Input('dropdown', 'value'),
     dash.dependencies.Input('radioinput4', 'value'),
     dash.dependencies.Input('country_dates', 'start_date'),
     dash.dependencies.Input('country_dates', 'end_date')]
)
def deaths_graph(country, radio, start_date, end_date):

    if radio=='actual':

        graph = build_deaths_graph(country, start_date, end_date)
    else:

        graph = build_deaths_log_graph(country, start_date, end_date)

    return graph

# Deaths and Confirmed over time
@app.callback(
    Output('confirmed_graph_time', 'children'),
    [Input('dropdown', 'value'),
     dash.dependencies.Input('radioinput3', 'value'),
     dash.dependencies.Input('country_dates', 'start_date'),
     dash.dependencies.Input('country_dates', 'end_date')]
)
def confirmed_graph(country, radio, start_date, end_date):

    if radio=='actual':

        graph = build_confirmed_graph(country, start_date, end_date)

    else:
        graph=build_confirmed_log_graph(country, start_date, end_date)

    return graph

# Average life expectancy
@app.callback(
    Output('total_population_graph', 'children'),
    [Input('dropdown', 'value')]
)
def population_actuals(country):
    graph =  build_population_actuals(country)
    return graph

# Average life expectancy
@app.callback(
    Output('total_male_population_graph', 'children'),
    [Input('dropdown', 'value')]
)
def population_actuals(country):
    graph =  build_population_male_actuals(country)
    return graph

@app.callback(
    Output('total_female_population_graph', 'children'),
    [Input('dropdown', 'value')]
)
def population_actuals(country):
    graph =  build_population_female_actuals(country)
    return graph

# Average life expectancy
@app.callback(
    Output('per_population_graph', 'children'),
    [Input('dropdown', 'value')]
)
def average_life_expectancy(country):
    graph = build_average_life_expectancy(country)
    return graph

# Heading
@app.callback(
    Output('heading', 'children'),
    [Input('dropdown', 'value')]
)
def return_heading_value(country):
    return '{} Coronavirus Daily Report'.format(country)

# Tabs1
@app.callback(Output('tabs1-content', 'children'),
              [Input('tabs1', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return dbc.Col(html.Div([html.Br(),html.P(news_list_group), html.Br()]), style={'overflowY': 'scroll', "height":"54.5vh"})
    elif tab == 'tab-2':
        return #dbc.Col(html.Div([html.Br(),html.P(tweets_list_group),]), style={'overflowY': 'scroll', "height":"54.5vh"})

# Tabs2
@app.callback(Output('tabs2-content', 'children'),
              [Input('tabs2', 'value')])
def render_content(tab):
    if tab == 'tabs2tab1':
        return dbc.Col(html.Div([html.Br(), radio, html.Br(), html.Div(id='xoutput2', children=[]), html.Br(), ]), style={"height": "50%"})
    elif tab == 'tabs2tab2':
        return dbc.Col(html.Div([html.Div(id='xoutput3', children=[]), html.Br(), ]), style={"height": "50%"})
    elif tab == 'tabs2tab3':
        return dbc.Col(html.Div([html.Br(), html.Br(), html.Br(), html.Div(id='hotspot_table'), html.Br()]), style={"height": "50%"})
        #dbc.Col(html.Div([html.Div([table])]), style={'overflowY': 'scroll', "height": "50%"})

# Tabs3
@app.callback(Output('tabs-graph-content', 'children'),
              [Input('tabs-example123', 'value')])
def render_content(tab):
    if tab == 'tabgraph1':
        return dbc.Col(html.Div([radio1, html.Br(), html.Div(id='cum_deaths'), html.Br()]), style={"height": "50%"}) #'overflowY': 'scroll',
    elif tab == 'tabgraph2':
        return dbc.Col(html.Div([radio2, html.Br(), html.Div(id='daily_deaths'), html.Br()]), style={"height": "50%"})

# Open expand button #1
@app.callback(
    Output("collapse1", "is_open"),
    [Input("collapse-button1", "n_clicks")],
    [State("collapse1", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

# Open expand button #2
@app.callback(
    Output("collapse2", "is_open"),
    [Input("collapse-button2", "n_clicks")],
    [State("collapse2", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

# Open expand button #3
@app.callback(
    Output("collapse3", "is_open"),
    [Input("collapse-button3", "n_clicks")],
    [State("collapse3", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

# Date range
@app.callback(
    dash.dependencies.Output('cum_deaths', 'children'),
    [dash.dependencies.Input('radioinput1', 'value'),
     dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')])
def cumulative_deaths(value, start_date, end_date):

    if start_date is None:

        start_date=pd.to_datetime(dt(2019, 12, 31))

    if value=='actual':

        graph=build_cumulative_deaths(start_date, end_date) # if radio = x then xradioinput1

    else:

        graph=build_cumulative_log_deaths(start_date, end_date)

    return graph

@app.callback(
    dash.dependencies.Output('daily_deaths', 'children'),
    [dash.dependencies.Input('radioinput2', 'value'),
     dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')])
def daily_deaths(value, start_date, end_date):

    if start_date is None:

        start_date=pd.to_datetime(dt(2019, 12, 31))

    if value=='actual':

        graph=build_daily_deaths(start_date, end_date)

    else:

        graph=build_daily_log_deaths(start_date, end_date)

    return graph

@app.callback(
    dash.dependencies.Output('xoutput2', 'children'),
    [dash.dependencies.Input('radioinput', 'value'),
     dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')])
def confirmed_graph(map_type, start_date, end_date):
    ''' Function to create the number of deaths graph'''

    graph=choropleth_map(map_type, start_date, end_date)
    return graph

# Worldwide New Tests Sum
@app.callback(
    dash.dependencies.Output('ww_new_tests_sum', 'children'),
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')])
def update_text(start_date, end_date):

    if start_date is None:

        start_date=pd.to_datetime(dt(2019, 12, 31))

    criteria1 = pd.to_datetime(covid_dataset['date']) <= pd.to_datetime(end_date)
    criteria2 = pd.to_datetime(covid_dataset['date']) >= pd.to_datetime(start_date)
    value=round(covid_dataset.loc[(criteria1) & (criteria2)]['new_tests'].sum().astype(int))
    value=add_commas(value)
    return value

# Worldwide New Cases Sum
@app.callback(
    dash.dependencies.Output('ww_new_cases_sum', 'children'),
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')])
def update_text(start_date, end_date):

    if start_date is None:

        start_date=pd.to_datetime(dt(2019, 12, 31))

    criteria1 = pd.to_datetime(covid_dataset['date']) <= pd.to_datetime(end_date)
    criteria2 = pd.to_datetime(covid_dataset['date']) >= pd.to_datetime(start_date)
    value=round(covid_dataset.loc[(criteria1) & (criteria2)]['new_cases'].sum().astype(int))
    value=add_commas(value)
    return value

# Worldwide New Deaths Sum
@app.callback(
    dash.dependencies.Output('ww_new_deaths_sum', 'children'),
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')])
def update_text(start_date, end_date):

    if start_date is None:

        start_date=pd.to_datetime(dt(2019, 12, 31))

    criteria1 = pd.to_datetime(covid_dataset['date']) <= pd.to_datetime(end_date)
    criteria2 = pd.to_datetime(covid_dataset['date']) >= pd.to_datetime(start_date)
    value=round(covid_dataset.loc[(criteria1) & (criteria2)]['new_deaths'].sum().astype(int))
    value=add_commas(value)
    return value

# Table
@app.callback(
    Output('table-filtering-be', "data"),
    [Input('table-filtering-be', "filter_query"),
     dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')])
def update_table(filter, start_date, end_date):
    filtering_expressions = filter.split(' && ')
    criteria1 = pd.to_datetime(hotspot_table_df['Date']) <= pd.to_datetime(end_date)
    criteria2 = pd.to_datetime(hotspot_table_df['Date']) >= pd.to_datetime(start_date)
    dff = hotspot_table_df.loc[criteria1&criteria2]
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)

        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]

    return dff.to_dict('records')

# Radar Plot
@app.callback(
    Output('output_radar', 'children'),
    [Input('dropdown', 'value')]
)
def radar_plot(country):
    if country is not None:
        graph = build_radar_plot(country)
        return graph

# Country New Tests Sum
@app.callback(
    dash.dependencies.Output('country_tests', 'children'),
    [Input('dropdown', 'value'),
     dash.dependencies.Input('country_dates', 'start_date'),
     dash.dependencies.Input('country_dates', 'end_date')])
def update_text(country, start_date, end_date):

    if start_date is None:
        start_date = pd.to_datetime(dt(2019, 12, 31))

    output=[]
    if type(country)==str:
        criteria1 = pd.to_datetime(covid_dataset['date']) <= pd.to_datetime(end_date)
        criteria2 = pd.to_datetime(covid_dataset['date']) >= pd.to_datetime(start_date)
        criteria3 = covid_dataset['location'] == country
        value = round(covid_dataset.loc[(criteria1) & (criteria2) & (criteria3)]['new_tests'].sum().astype(int))
        value = add_commas(value)
        output.append(html.H4(value, style={'color': 'black', 'font-weight': 'bold'}, className="card-subtitle"))

    else:

        for i in country:
            criteria1 = pd.to_datetime(covid_dataset['date']) <= pd.to_datetime(end_date)
            criteria2 = pd.to_datetime(covid_dataset['date']) >= pd.to_datetime(start_date)
            criteria3 = covid_dataset['location'] == i
            value = round(covid_dataset.loc[(criteria1) & (criteria2) & (criteria3)]['new_tests'].sum().astype(int))
            value = add_commas(value)
            output.append(html.H4(value, style={'color': 'black', 'font-weight': 'bold'}, className="card-subtitle"))
    return output

# Country New Deaths Sum
@app.callback(
    dash.dependencies.Output('country_deaths', 'children'),
    [Input('dropdown', 'value'),
     dash.dependencies.Input('country_dates', 'start_date'),
     dash.dependencies.Input('country_dates', 'end_date')])
def update_text(country, start_date, end_date):

    if start_date is None:
        start_date = pd.to_datetime(dt(2019, 12, 31))

    output=[]
    if type(country)==str:
        criteria1 = pd.to_datetime(covid_dataset['date']) <= pd.to_datetime(end_date)
        criteria2 = pd.to_datetime(covid_dataset['date']) >= pd.to_datetime(start_date)
        criteria3 = covid_dataset['location'] == country
        value = round(covid_dataset.loc[(criteria1) & (criteria2) & (criteria3)]['new_deaths'].sum().astype(int))
        value = add_commas(value)
        output.append(html.H4(value, style={'color': 'red', 'font-weight': 'bold'}, className="card-subtitle"))

    else:

        for i in country:
            criteria1 = pd.to_datetime(covid_dataset['date']) <= pd.to_datetime(end_date)
            criteria2 = pd.to_datetime(covid_dataset['date']) >= pd.to_datetime(start_date)
            criteria3 = covid_dataset['location'] == i
            value = round(covid_dataset.loc[(criteria1) & (criteria2) & (criteria3)]['new_deaths'].sum().astype(int))
            value = add_commas(value)
            output.append(html.H4(value, style={'color': 'red', 'font-weight': 'bold'}, className="card-subtitle"))
    return output

# Country New Tests Sum
@app.callback(
    dash.dependencies.Output('country_cases', 'children'),
    [Input('dropdown', 'value'),
     dash.dependencies.Input('country_dates', 'start_date'),
     dash.dependencies.Input('country_dates', 'end_date')])
def update_text(country, start_date, end_date):

    if start_date is None:
        start_date = pd.to_datetime(dt(2019, 12, 31))

    output=[]
    if type(country)==str:
        criteria1 = pd.to_datetime(covid_dataset['date']) <= pd.to_datetime(end_date)
        criteria2 = pd.to_datetime(covid_dataset['date']) >= pd.to_datetime(start_date)
        criteria3 = covid_dataset['location'] == country
        value = round(covid_dataset.loc[(criteria1) & (criteria2) & (criteria3)]['new_cases'].sum().astype(int))
        value = add_commas(value)
        output.append(html.H4(value, style={'color': 'orange', 'font-weight': 'bold'}, className="card-subtitle"))

    else:

        for i in country:
            criteria1 = pd.to_datetime(covid_dataset['date']) <= pd.to_datetime(end_date)
            criteria2 = pd.to_datetime(covid_dataset['date']) >= pd.to_datetime(start_date)
            criteria3 = covid_dataset['location'] == i
            value = round(covid_dataset.loc[(criteria1) & (criteria2) & (criteria3)]['new_cases'].sum().astype(int))
            value = add_commas(value)
            output.append(html.H4(value, style={'color': 'orange', 'font-weight': 'bold'}, className="card-subtitle"))
    return output

@app.callback(
    Output('country', 'children'),
    [Input('dropdown', 'value')]
)
def country_level_statistics(country):
    output=[]
    if type(country)==str:
        output.append(html.H4(country, style={'color': 'black', 'font-weight': 'bold'}, className="card-subtitle"))
    else:
        for i in country:
            output.append(html.H4(i, style={'color': 'black', 'font-weight': 'bold'}, className="card-subtitle"))

    return output

# Country page tabs
@app.callback(Output('c2tabgraph1-content', 'children'),
              [Input('c2tabgraph', 'value')])
def render_content(tab):
    if tab == 'c2tabgraph1':
        return dbc.Col(html.Div([html.Br(), html.Br(), html.Div(id='output_radar', children=[])]), style={"height": "100%"})
    elif tab == 'c2tabgraph2':
        return dbc.Col(html.Div([html.Br(),html.Br(), html.Div([country_table])]), style={"height": "100%"})

# Country page tabs
@app.callback(Output('country_tabs_card1-content', 'children'),
              [Input('country_tabs_card1', 'value')])
def render_content(tab):
    if tab == 'c1tabgraph2':
        return dbc.Col(html.Div([html.Br(), radio3, html.Div(id='confirmed_graph_time', children=[])]), style={"height": "100%"})
    elif tab == 'c1tabgraph3':
        return dbc.Col(html.Div([html.Br(), radio4, html.Div(id='deaths_graph_time', children=[])]), style={"height": "100%"})

# Country page tabs
@app.callback(Output('country_tabs_card3-content', 'children'),
              [Input('country_tabs_card3', 'value')])
def render_content(tab):
    if tab == 'c3tabgraph1':
        return dbc.Col(html.Div([html.Br(), html.Div(id='per_population_graph', children=[])]), style={"height": "100%"})
    elif tab == 'c3tabgraph2':
        return dbc.Col(html.Div([html.Br(), html.Div(id='total_population_graph', children=[])]), style={"height": "100%"})
    elif tab == 'c3tabgraph3':
        return dbc.Col(html.Div([html.Br(), html.Div(id='total_male_population_graph', children=[])]), style={"height": "100%"})
    elif tab == 'c3tabgraph4':
        return dbc.Col(html.Div([html.Br(), html.Div(id='total_female_population_graph', children=[])]), style={"height": "100%"})

# Database
@app.callback(
    Output('table-filtering-radardata', "data"),
    [Input('table-filtering-radardata', "filter_query")])
def update_table(filter):
    filtering_expressions = filter.split(' && ')
    dff = radar_plot_database_df
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)

        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]

    return dff.to_dict('records')

@app.callback(
    dash.dependencies.Output('country_tests_units', 'children'),
    [Input('dropdown', 'value'),
     dash.dependencies.Input('country_dates', 'start_date'),
     dash.dependencies.Input('country_dates', 'end_date')])
def testing_numbers_and_units(country, start_date, end_date):
    output=[]

    if type(country)==str:
        criteria1 = pd.to_datetime(covid_dataset['date']) <= pd.to_datetime(end_date)
        criteria2 = pd.to_datetime(covid_dataset['date']) >= pd.to_datetime(start_date)
        criteria3 = covid_dataset['location'] == country
        value = round(covid_dataset.loc[(criteria1) & (criteria2) & (criteria3)]['new_tests'].sum().astype(int))
        value=add_commas(value)

        try:

            criteria4 = covid_dataset['location'] == country
            criteria5 = covid_dataset['tests_units'].notnull()
            unit = covid_dataset.loc[criteria4 & criteria5]['tests_units'].unique()[0]

        except IndexError:

            unit=""

        print_output=str(value)+" "+str(unit)

        output.append(html.H4(print_output, style={'color': 'black', 'font-weight': 'bold'}, className="card-subtitle"))

    elif type(country)==list:

        for i in country:
            criteria1 = pd.to_datetime(covid_dataset['date']) <= pd.to_datetime(end_date)
            criteria2 = pd.to_datetime(covid_dataset['date']) >= pd.to_datetime(start_date)
            criteria3 = covid_dataset['location'] == i
            value = round(covid_dataset.loc[(criteria1) & (criteria2) & (criteria3)]['new_tests'].sum().astype(int))
            value = add_commas(value)

            try:

                criteria4 = covid_dataset['location'] == i
                criteria5 = covid_dataset['tests_units'].notnull()
                unit = covid_dataset.loc[criteria4 & criteria5]['tests_units'].unique()[0]

            except IndexError:

                unit=""

            print_output=str(value)+" "+str(unit)

            output.append(html.H4(print_output, style={'color': 'black', 'font-weight': 'bold'}, className="card-subtitle"))

    return output

@app.callback(Output('navitem1', 'children'),
            [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/countrypage':
        return dbc.NavItem(html.Span(dbc.NavLink("Worldwide Information Centre", href="/homepage"), style={'color': 'black'})),\
               dbc.NavItem(html.Span(dbc.NavLink("Country Insights Miner", href="/countrypage"),style={'color': 'black', 'font-weight': 'bold'}))
    else:
        return dbc.NavItem(html.Span(dbc.NavLink("Worldwide Information Centre", href="/homepage"), style={'color': 'black', 'font-weight': 'bold'})),\
               dbc.NavItem(html.Span(dbc.NavLink("Country Insights Miner", href="/countrypage"),style={'color': 'black'}))

@app.callback(
    dash.dependencies.Output('hotspot_table', 'children'),
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')])
def hotspot_graph(start_date, end_date):

    if start_date is None:

        start_date=pd.to_datetime(dt(2019, 12, 31))

    graph=build_hotspot_graph(start_date, end_date)
    return graph


# Main to run
if __name__ == '__main__':
    app.run_server(debug=True)