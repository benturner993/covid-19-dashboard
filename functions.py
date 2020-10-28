import dash_bootstrap_components as dbc
import dash_html_components as html
import world_bank_data as wb
import pandas as pd

def create_single_card(input1):

    ''' Function to automate the build of headline statistics cards'''

    card = dbc.Card(dbc.CardBody([input1]),color="light", inverse=False)
    return card

def create_card(input1, input2):

    ''' Function to automate the build of headline statistics cards'''

    card = dbc.Card(dbc.CardBody([input1, input2]), inverse=False)
    return card

def create_country_card(input1, input2, input3, input4, input5):

    ''' Function to automate the build of headline statistics cards'''

    card = dbc.Card(dbc.CardBody([input1, input2, input3, input4, input5]),color="light", inverse=False)
    return card

def card_title(text):

    ''' Function to shorten the creation of a card heading title'''

    card_title=html.H6(text, className="card-title")
    return card_title

def add_commas(value):

    ''' Function to add commas so that the number is more readable '''

    val = "{:,}".format(value)
    return val

operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]

def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3

# Population statistics p2g3
def population_numbers():

    wbdf1 = wb.get_series('SP.POP.0014.TO', mrv=1).reset_index()[['Country', 'Year', 'SP.POP.0014.TO']]
    wbdf1.columns = ['countriesAndTerritories', 'Year', 'Pop. ages 0-14']

    wbdf2 = wb.get_series('SP.POP.1564.TO', mrv=1).reset_index()[['Country', 'SP.POP.1564.TO']]
    wbdf2.columns = ['countriesAndTerritories', 'Pop. ages 15-64']

    wbdf3 = wb.get_series('SP.POP.65UP.TO', mrv=1).reset_index()[['Country', 'SP.POP.65UP.TO']]
    wbdf3.columns = ['countriesAndTerritories', 'Pop. ages 65+']

    wbdf4 = wbdf1.merge(wbdf2, on='countriesAndTerritories', how='left').merge(wbdf3, on='countriesAndTerritories',
                                                                           how='left')

    # Transform dataset so that it can be plotted on a graph
    wbdf4 = wbdf4.transpose()
    wbdf4.columns = wbdf4.iloc[0]
    wbdf4 = wbdf4[1:]
    wbdf4 = wbdf4.reset_index()
    wbdf4 = wbdf4.loc[wbdf4['index'] != 'Year']
    wbdf4['Population'] = wbdf4['index']

    return wbdf4


def population_male_numbers():
    wbdf1 = wb.get_series('SP.POP.0014.MA.ZS', mrv=1).reset_index()[['Country', 'Year', 'SP.POP.0014.MA.ZS']]
    wbdf1.columns = ['countriesAndTerritories', 'Year', 'Male Pop. ages 0-14 %']

    wbdf2 = wb.get_series('SP.POP.1564.MA.ZS', mrv=1).reset_index()[['Country', 'SP.POP.1564.MA.ZS']]
    wbdf2.columns = ['countriesAndTerritories', 'Male Pop. ages 15-64 %']

    wbdf3 = wb.get_series('SP.POP.65UP.MA.ZS', mrv=1).reset_index()[['Country', 'SP.POP.65UP.MA.ZS']]
    wbdf3.columns = ['countriesAndTerritories', 'Male Pop. ages 65+ &']

    wbdf4 = wbdf1.merge(wbdf2, on='countriesAndTerritories', how='left').merge(wbdf3, on='countriesAndTerritories',
                                                                               how='left')
    wbdf4.columns = ['countriesAndTerritories',
                     'Year',
                     'Male Pop % aged 0-14',
                     'Male Pop % aged 15-64',
                     'Male Pop % aged 65+']

    # Transform dataset so that it can be plotted on a graph
    wbdf4 = wbdf4.transpose()
    wbdf4.columns = wbdf4.iloc[0]
    wbdf4 = wbdf4[1:]
    wbdf4 = wbdf4.reset_index()
    wbdf4 = wbdf4.loc[wbdf4['index'] != 'Year']
    wbdf4['Population'] = wbdf4['index']

    return wbdf4


def population_female_numbers():
    wbdf1 = wb.get_series('SP.POP.0014.FE.ZS', mrv=1).reset_index()[['Country', 'Year', 'SP.POP.0014.FE.ZS']]
    wbdf1.columns = ['countriesAndTerritories', 'Year', 'Pop. ages 0-14']

    wbdf2 = wb.get_series('SP.POP.1564.FE.ZS', mrv=1).reset_index()[['Country', 'SP.POP.1564.FE.ZS']]
    wbdf2.columns = ['countriesAndTerritories', 'Pop. ages 15-64']

    wbdf3 = wb.get_series('SP.POP.65UP.FE.ZS', mrv=1).reset_index()[['Country', 'SP.POP.65UP.FE.ZS']]
    wbdf3.columns = ['countriesAndTerritories', 'Pop. ages 65+']

    wbdf4 = wbdf1.merge(wbdf2, on='countriesAndTerritories', how='left').merge(wbdf3, on='countriesAndTerritories',
                                                                               how='left')
    wbdf4.columns = ['countriesAndTerritories',
                     'Year',
                     'Female Pop % aged 0-14',
                     'Female Pop % aged 15-64',
                     'Female Pop % aged 65+']

    # Transform dataset so that it can be plotted on a graph
    wbdf4 = wbdf4.transpose()
    wbdf4.columns = wbdf4.iloc[0]
    wbdf4 = wbdf4[1:]
    wbdf4 = wbdf4.reset_index()
    wbdf4 = wbdf4.loc[wbdf4['index'] != 'Year']
    wbdf4['Population'] = wbdf4['index']

    return wbdf4

def total_population_numbers_per():
    # Create a dataset which shows the proportionate age of the population of a country
    wbdf1 = wb.get_series('SP.POP.0014.TO.ZS', mrv=1).reset_index()[['Country', 'Year', 'SP.POP.0014.TO.ZS']]
    wbdf1.columns = ['countriesAndTerritories', 'Year', 'Pop. ages 0-14 (% of total population)']

    wbdf2 = wb.get_series('SP.POP.1564.TO.ZS', mrv=1).reset_index()[['Country', 'SP.POP.1564.TO.ZS']]
    wbdf2.columns = ['countriesAndTerritories', 'Pop. ages 15-64 (% of total population)']

    wbdf3 = wb.get_series('SP.POP.65UP.TO.ZS', mrv=1).reset_index()[['Country', 'SP.POP.65UP.TO.ZS']]
    wbdf3.columns = ['countriesAndTerritories', 'Pop. ages 65+ (% of total population)']

    wbdf4 = wbdf1.merge(wbdf2, on='countriesAndTerritories', how='left').merge(wbdf3, on='countriesAndTerritories',
                                                                               how='left')
    wbdf4.columns = ['countriesAndTerritories',
                     'Year',
                     'Pop % aged 0-14',
                     'Pop % aged 15-64',
                     'Pop % aged 65+']

    # Transform dataset so that it can be plotted on a graph
    wbdf4 = wbdf4.transpose()
    wbdf4.columns = wbdf4.iloc[0]
    wbdf4 = wbdf4[1:]
    wbdf4 = wbdf4.reset_index()
    wbdf4 = wbdf4.loc[wbdf4['index'] != 'Year']
    wbdf4['Population Rates'] = wbdf4['index']

    return wbdf4

def windsorize(df, col):
    # Append new col
    df[col + '_original'] = df[col]

    # Find mean and std
    mean = df[col].mean()
    std = df[col].std()

    # Windsorize
    df[col][df[col] >= mean + (3 * std)] = mean + (3 * std)
    df[col][df[col] <= mean - (3 * std)] = mean - (3 * std)

    return df

# Case fatality rate: deaths/cases (percent)
def case_fatality_df(df, date_col, min_date, max_date, output_col_name):
    # Define the date boundaries
    criteria1 = pd.to_datetime(df[date_col]) <= pd.to_datetime(max_date)
    criteria2 = pd.to_datetime(df[date_col]) >= pd.to_datetime(min_date)

    # Filter dataframe to boundaries
    df = df.loc[criteria1 & criteria2]

    # Calculate cases_count and death_count
    cases_count = df.groupby(['iso_code'])['new_cases'].transform('sum')
    death_count = df.groupby(['iso_code'])['new_deaths'].transform('sum')

    df[output_col_name] = round((death_count / cases_count) * 100000, 2)

    # Filter for one row per country by taking last availabe
    df = df.sort_values(date_col).groupby('iso_code').tail(1)
    df=windsorize(df, output_col_name)

    return df

def cause_fatality_df(df, date_col, min_date, max_date, output_col_name):

    # Retrieve data from wb
    wbdf = wb.get_series('SP.POP.TOTL', mrv=1).reset_index()
    wbdf.columns = ['Country', 'Series', 'Year', 'Population']

    # Join to covid df
    df = df.merge(wbdf, left_on='location', right_on='Country', how='left')
    df = df.loc[df['iso_code'] != 'OWID_WRL']

    # Define the date boundaries and filter
    criteria1 = pd.to_datetime(df[date_col]) <= pd.to_datetime(max_date)
    criteria2 = pd.to_datetime(df[date_col]) >= pd.to_datetime(min_date)
    df = df.loc[criteria1 & criteria2]

    # Filter down dataframe
    cols = ['iso_code', 'location', 'date', 'total_cases', 'new_deaths', 'total_deaths', 'Population']
    df = df[cols]

    # Define cause fatality cols and calculate
    number_of_deaths = df.groupby('location')['new_deaths'].transform('sum')
    population = df['Population']
    df[output_col_name] = round((number_of_deaths / population) * 100000, 2)

    df = df.loc[df[date_col] == max_date]
    df = windsorize(df, output_col_name)

    return df


# Compress Dataset
def radar_plot_df(df, country_list):
    #df = df.loc[df['date'] == max(df['date'])]
    df=df.sort_values(by='date').groupby('location').tail(1)

    # Cols for percentile rank
    cols = ['population',
            'population_density',
            'diabetes_prevalence',
            'gdp_per_capita',
            'handwashing_facilities',
            #'hospital_beds_per_100k',
            'median_age']

    df_cols_list = []

    for i in cols:
        df_cols_list.append(i)
        df[i + '_percentile_rank'] = round(df[i].rank(pct=True) * 100, 2)
        df_cols_list.append(i + '_percentile_rank')

    # Subset dataframe
    df_cols_list.append('location')
    df = df[df_cols_list]
    if type(country_list) == str:
        df = df.loc[df['location'] == country_list]
    else:
        df = df.loc[df['location'].isin(country_list)]

    return df

def country_statistics(df):

    wbdf = wb.get_series('SP.POP.TOTL', mrv=1).reset_index()
    wbdf.columns = ['Country','Series','Year','Population']

    # Group data and combine
    df=df.groupby(['location']).agg({'new_cases': ['sum'], 'new_deaths': ['sum'], 'new_tests': ['sum']}).reset_index()
    df.columns=['location', 'cases', 'deaths', 'tests']
    df['tests']=df['tests'].astype(int)
    df=df.merge(wbdf, left_on='location', right_on='Country', how='left')

    # Create additional features
    df['cases_per_hund']=round((df['cases']/df['Population'])*100000,2)
    df['deaths_per_hund']=round((df['deaths']/df['Population'])*100000,2)
    df['tests_per_hund']=round((df['tests']/df['Population'])*100000,2)
    cols=['location','cases','deaths','tests','Population','cases_per_hund','deaths_per_hund','tests_per_hund']
    df=df[cols]
    return df

def radar_plot_database(df):
    df = df.sort_values(by='date').groupby('location').tail(1)

    # Cols for percentile rank
    cols = ['population',
            'population_density',
            'diabetes_prevalence',
            'gdp_per_capita',
            'handwashing_facilities',
            #'hospital_beds_per_100k',
            'median_age']

    df_cols_list = []

    for i in cols:
        df_cols_list.append(i)
        df[i + '_percentile_rank'] = round(df[i].rank(pct=True) * 100, 2)
        df_cols_list.append(i + '_percentile_rank')

    # Subset dataframe
    df_cols_list.append('location')
    df = df[df_cols_list]

    cols = ['location',
            'population',
            'population_percentile_rank',
            'population_density',
            'population_density_percentile_rank',
            'diabetes_prevalence',
            'diabetes_prevalence_percentile_rank',
            'gdp_per_capita',
            'gdp_per_capita_percentile_rank',
            'handwashing_facilities',
            'handwashing_facilities_percentile_rank',
            #'hospital_beds_per_100k',
            #'hospital_beds_per_100k_percentile_rank',
            'median_age',
            'median_age_percentile_rank']
    df = df.loc[df['location'] != 'International'][cols]
    return df

def hotspot_table(df):

    df = df.loc[df['location'] != 'World']
    criteria1 = (8 * df['new_deaths']) >= (df['total_deaths'])
    criteria2 = df['total_deaths'] > 9
    df['per_new_deaths'] = round((df['new_deaths'] / df['total_deaths']), 2) * 100
    df['per_new_deaths']=round(df['per_new_deaths'],0)
    cols = ['location', 'date', 'total_deaths', 'new_deaths', 'per_new_deaths']
    df = df.loc[criteria1 & criteria2].sort_values(by=['date', 'total_deaths'])[cols]
    df.columns = ['Country', 'Date', 'Total Deaths', 'New Deaths', 'Percentage']
    df = df.groupby('Country').tail(1).sort_values(by='Percentage', ascending=False)

    return df

if __name__ == "__main__":
    app.run_server()