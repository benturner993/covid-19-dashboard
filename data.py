# Import packages
import pandas as pd
import numpy as np
import world_bank_data as wb
import dash_html_components as html
import dash_bootstrap_components as dbc
from navbar import Navbar
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import pandas as pd
import re
from twitter import *
from functions import *

# Twitter Api Credentials
#consumerKey = 'XVKynWf2F3U9bskCDitDoVqHj'
#consumerSecret = 'PBUn88VdmwZXasLOt8pJd4jvXmfZav3ltCzVIx8oLB9NNcGAAy'
#accessToken = '1247524708955738115-d4ka9GW1QTbCdbvjhw89SifP4nDVHJ'
#accessTokenSecret = 'LWgI0N1OZLhBjLlNbhgjx9YmEVIY2sMB9FgqFR1uL9QZK'

# Create twitter API object
#twitter = Twitter(auth=OAuth(accessToken,
#                             accessTokenSecret,
#                             consumerKey,
#                             consumerSecret))

# Retrieve global trends
#results = twitter.trends.place(_id=23424975)

# trending_list = []
#
# for location in results:
#     for trend in location["trends"]:
#         trending_list.append(trend["name"])
#
# # Create a dataframe with a column called Tweets
# tweets_df = pd.DataFrame(trending_list, columns=['Tweets'])
#
# # Code for tweets
# tweets_list = []
#
# for tweets in tweets_df['Tweets'][:10]:
#     tweets_list.append(tweets)
#
# tweets_list_group = dbc.ListGroup(
#     [
#         dbc.ListGroupItem(tweets_list[0], color="link"),
#         dbc.ListGroupItem(tweets_list[1], color="link"),
#         dbc.ListGroupItem(tweets_list[2], color="link"),
#         dbc.ListGroupItem(tweets_list[3], color="link"),
#         dbc.ListGroupItem(tweets_list[4], color="link"),
#         dbc.ListGroupItem(tweets_list[5], color="link"),
#         dbc.ListGroupItem(tweets_list[6], color="link"),
#         dbc.ListGroupItem(tweets_list[7], color="link"),
#         dbc.ListGroupItem(tweets_list[8], color="link"),
#         dbc.ListGroupItem(tweets_list[9], color="link")
#     ]
# )

# News
news_url = "https://news.google.com/news/rss"
Client = urlopen(news_url)
xml_page = Client.read()
Client.close()

soup_page = soup(xml_page, "xml")
news_list = soup_page.findAll("item")

coronanews = []
coronanews_links = []

for news in news_list:

    matches = ["Coronavirus",
               "coronavirus",
               "Economy",
               "economy",
               "Virus",
               "virus",
               "Lockdown",
               "lockdown",
               "Testing",
               "testing",
               "Infected",
               "infected",
               "Covid-19",
               "COVID-19",
               "Covid19",
               "COVID19",
               "Pandemic",
               "pandemic"
               "Epidemic",
               "epidemic",
               "Outbreak",
               "outbreak",
               "Quarantine",
               "quarantine",
               "Distancing",
               "distancing",
               "Isolation",
               "isolation",
               "Deaths",
               "deaths"]

    if any(x in news.title.text for x in matches):
        coronanews.append(news.title.text)
        coronanews_links.append(news.link.text)
    else:
        continue

headlines_full_list = []
headlines_full_list_links = []

for news in coronanews[:10]:
    headlines_full_list.append(news)

for news_links in coronanews_links[:10]:
    headlines_full_list_links.append(news_links)

headline = []
news_outlet = []

for item in headlines_full_list:
    a, b = item.split(' - ', 1)
    headline.append(a)
    news_outlet.append(b)

news_list_group = dbc.ListGroup(
    [
        dbc.ListGroupItem([dbc.ListGroupItemHeading(headline[0]), dbc.ListGroupItemText(news_outlet[0]), ],
                          href=headlines_full_list_links[0], style={'color': 'black'}),
        dbc.ListGroupItem([dbc.ListGroupItemHeading(headline[1]), dbc.ListGroupItemText(news_outlet[1]), ],
                          href=headlines_full_list_links[1], style={'color': 'black'}),
        dbc.ListGroupItem([dbc.ListGroupItemHeading(headline[2]), dbc.ListGroupItemText(news_outlet[2]), ],
                          href=headlines_full_list_links[2], style={'color': 'black'}),
        dbc.ListGroupItem([dbc.ListGroupItemHeading(headline[3]), dbc.ListGroupItemText(news_outlet[3]), ],
                          href=headlines_full_list_links[3], style={'color': 'black'}),
#        dbc.ListGroupItem([dbc.ListGroupItemHeading(headline[4]), dbc.ListGroupItemText(news_outlet[4]), ],
#                          href=headlines_full_list_links[4], style={'color': 'black'}),
#        dbc.ListGroupItem([dbc.ListGroupItemHeading(headline[5]), dbc.ListGroupItemText(news_outlet[5]), ],
#                          href=headlines_full_list_links[5], style={'color': 'black'}),
#        dbc.ListGroupItem([dbc.ListGroupItemHeading(headline[6]), dbc.ListGroupItemText(news_outlet[6]), ],
#                          href=headlines_full_list_links[6], style={'color': 'black'}),
    ]
)

# Color scheme for graphs
graph_colours = ['Black', 'Red', 'Orange', 'Yellow', 'Blue']

# Primary dataset
covid_dataset = pd.read_excel('https://covid.ourworldindata.org/data/owid-covid-data.xlsx')
covid_dataset = covid_dataset.loc[covid_dataset['location'] != 'World']
covid_dataset.sort_values(by=['location', 'date'])

# Text for disclaimer footer
disclaimer_text = ["This dashboard is built upon publicly available data primarily provided and maintained by Our World \
in Data. The reason for using this source is because it is constantly maintained and enriched with other useful sources of \
information allowing the dashboard to be of continued use after the development of the dashboard is completed. \
The confirmed cases and deaths dataset comes from the European Centre for Disease Prevention and Control \
(ECDC) and is updated daily. The testing data for COVID-19 is collected by the Our World in Data team from official \
reports and is updated around twice a week. Other variables have been collated from a variety of sources (United \
Nations, World Bank, Global Burden of Disease, etc.) by Our World in Data. For more specific information, please visit \
Our World In Data's GitHub page (https://github.com/owid/covid-19-data/tree/master/public/data/). In addition, data has \
also been provided by the World Bank of Data (https://data.worldbank.org) through the Python API as well as Google News \
Feeds (https://news.google.com/news/rss) and the Twitter API (https://api.twitter.com/1.1/trends/place.json). The \
contents of this website are for information purposes only and are not guaranteed to be accurate. Reliance on this \
website for medial guidance is strictly prohibited."]

card1 = [
    "The 'Daily Deaths' card shows the number of daily cases and deaths at a worldwide level. The 'Total Deaths' card shows the cumulative number of cases and deaths over time at "
    "a worldwide level. Both graphs are plotted over the selected time range."]

card2 = [
    "The 'Case Mortality (Per 100k)' plot shows the proportion of deaths from COVID-19 compared to the total number of people diagnosed (per country per 100K people) over the selected "
    "time frame. The 'Transmission Rate' tab shows an ordered list of countries and days highlighting the areas and times that the COVID-19 death rate was most deadly."]

card3 = [
    "The 'Latest News' tab shows a Google News RSS feed which has been filtered for COVID-19 related stories and headlines. The 'Trending' tab shows what is currently trending live in the " \
    "United Kingdom and is provided by the Twitter API."]

card4 = [
    "The 'Daily Cases' and 'Daily Deaths' cards shows the number of daily cases and deaths for the selected countries over the selected time frame."]

card5 = [
    "The 'Radar Plot' shows the percentile rank of Population Density, Population, Median Age, Hospital Beds Per 100k, GDP Per Capita and Diabetes Prevalence for the selected countries. "]
#"The 'Country Database' provides the percentile rank and absolute values to support the Radar Plot."

card6 = [
    "The 'Total Population %', 'Male Population %' and 'Female Population %' tabs show the percetange of the populaton by demographic and age range (0-14, 15-64 and 65+). The World Average " \
    "is provided in grey and can be used as a benchmark."]

# World Bank Dataset Population
wbdf4 = total_population_numbers_per()


# World Bank Dataset Male Population
population_male_numbers_df = population_male_numbers()

# World Bank Dataset Female Population
population_female_numbers_df = population_female_numbers()

# World Bank Data Population Absolute
population_numbers_df = population_numbers()

# Radar Plot
radar_plot_database_df = radar_plot_database(covid_dataset)

# Fastest growing table
hotspot_table_df = hotspot_table(covid_dataset)

if __name__ == "__main__":
    app.run_server()