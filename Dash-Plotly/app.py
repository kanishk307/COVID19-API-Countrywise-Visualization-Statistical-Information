from __future__ import print_function
import requests
import numpy as np
import pprint
import pandas as pd
from matplotlib import pyplot as plt
from datetime import datetime, timedelta
from matplotlib import dates
from matplotlib.pyplot import figure
import ipywidgets as widgets
from ipywidgets import interact, interactive, fixed, interact_manual
from dateutil.parser import parse
import locale
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
from collections import OrderedDict
import dash_table
from dash.dependencies import Input, Output, State



locale.setlocale(locale.LC_ALL, 'en_US')

url_countries = "https://api.covid19api.com/countries"
countries = requests.get(url_countries) #countries.status_code Assuming status code is 200
countries = countries.json()
country_slug_list = []
country_list = []
for country in countries:
    country_slug_list.append(country['Slug'])
for country in countries:
    country_list.append(country['Country'])
country_slug_list.sort()
country_list.sort()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)


df= pd.DataFrame({
    'c' : country_slug_list
})

print(country_slug_list)
print("Choose a country name from the list above")
country_name = input()

url_complete_status = f"https://api.covid19api.com/total/dayone/country/{country_name}"
stats_since_day_one = requests.get(url_complete_status)
stats_since_day_one = stats_since_day_one.json()
active_list = []
confirmed_list =[]
deaths_list = []
recovered_list = []
date_list = []
new_date_list = []

for stat in stats_since_day_one:
    active_list.append(stat['Active'])
    confirmed_list.append(stat['Confirmed'])
    deaths_list.append(stat['Deaths'])
    recovered_list.append(stat['Recovered'])
    date_list.append(stat['Date'])


for date in date_list:
    new_date_list.append(date[:10])

date_objects = [datetime.strptime(date, '%Y-%m-%d').date() for date in new_date_list]


country_name_capitalized = country_name.capitalize()
country_name_capitalized_spaced = country_name_capitalized.replace('-',' ')
country_name_final_representation = country_name_capitalized_spaced.title()


def max_one_day_increase(empty_list,data_list):
    for i in range(1,len(data_list)):
        empty_list.append(data_list[i]-data_list[(i-1)])
    return max(empty_list)

def change_past_24_hours(data_list):
    return (data_list[-1]-data_list[-2])

total_confirmed_cases = confirmed_list[-1]
total_active_cases = active_list[-1]
total_deaths = deaths_list[-1]
total_recovered = recovered_list[-1]
percent_active = round(total_active_cases/total_confirmed_cases*100,2)
percent_death = round(total_deaths/total_confirmed_cases*100,2)
percent_recovered = round(total_recovered/total_confirmed_cases*100,2)

# days calculation
first_case_reported = new_date_list[0]
date_list_calculate = [datetime.strptime(dateInDatetime, '%Y-%m-%d') for dateInDatetime in new_date_list]
date_first_case = date_list_calculate[0]
current_date = datetime.now()
days_since_first_case = (current_date - date_first_case).days

# Average calculation
avg_cases_per_day = round(total_confirmed_cases/days_since_first_case)
avg_deaths_per_day = round(total_deaths/days_since_first_case)
avg_recoveries_per_day = round(total_recovered/days_since_first_case)

# 2 weeks calculation
date_before_14_days = current_date - timedelta(days=14)
year = date_before_14_days.strftime("%Y")
month = date_before_14_days.strftime("%m")
day = date_before_14_days.strftime("%d")

date_before_14_days_string = f"{year}-{month}-{day}"
date_before_14_days_string

index_before_14_days = new_date_list.index(date_before_14_days_string)
confirmed_cases_14_days = total_confirmed_cases - confirmed_list[index_before_14_days]
active_cases_14_days = total_active_cases - active_list[index_before_14_days]
deaths_14_days = total_deaths - deaths_list[index_before_14_days]
recovered_14_days = total_recovered - recovered_list[index_before_14_days]
avg_cases_per_day_14_days = round(confirmed_cases_14_days/14)
avg_deaths_per_day_14_days = round(deaths_14_days/14)
avg_recoveries_per_day_14_days = round(recovered_14_days/14)

#Max One Day increase
one_day_increase_confirmed_cases = []
max_one_day_increase_confirmed_cases = max_one_day_increase(one_day_increase_confirmed_cases,confirmed_list)
one_day_increase_deaths = []
max_one_day_increase_deaths = max_one_day_increase(one_day_increase_deaths,deaths_list)
one_day_increase_recovered = []
max_one_day_increase_recovered = max_one_day_increase(one_day_increase_recovered,recovered_list)


#Past 24 hours
past_24_hours_confirmed_cases = change_past_24_hours(confirmed_list)
past_24_hours_active_cases = change_past_24_hours(active_list)
past_24_hours_deaths = change_past_24_hours(deaths_list)
past_24_hours_recovered = change_past_24_hours(recovered_list)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

app.layout = html.Div(children=[
# dcc.Dropdown(
#             id='dropdown',
#             options=[
#                 {'label':i, 'value':i} for i in df['c'].unique()
#             ],
#         value = 'united-states'
#         ),
#     html.Div(id='output'),
        # html.Div(id='dd-output-container'),

    
    html.H1(children=f"Statistics for {country_name_final_representation}"),

    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div(children = [html.H4(f'Past 24 hours (1 day)'),
                                     html.P(f'Confirmed Cases - {past_24_hours_confirmed_cases:n}'),
                                     html.P(f'Active Cases - {past_24_hours_active_cases:n}'),
                                     html.P(f'Deaths - {past_24_hours_deaths:n}'),
                                     html.P(f'Recovered - {past_24_hours_recovered:n}')
                                     ])),
                    dbc.Col(html.Div(children=[html.H4(f'All time'),
                                               html.P(f'Total Confirmed Cases - {total_confirmed_cases:n}'),
                                               html.P(f'Total Active Cases - {total_active_cases:n}'),
                                               html.P(f'Total Deaths - {total_deaths:n}'),
                                               html.P(f'Total Recovered - {total_recovered:n}'),
                                               html.P(f'Active Percentage - {percent_active:n}%'),
                                               html.P(f'Death Percentage - {percent_death:n}%'),
                                               html.P(f'Recovery Percentage - {percent_recovered}%'),
                                               html.P(f'First Case Reported - {first_case_reported}'),
                                               html.P(f'Days since First Case - {days_since_first_case:n}'),
                                               html.P(f'Average Cases Per Day - {avg_cases_per_day:n}'),
                                               html.P(f'Average Deaths Per Day - {avg_deaths_per_day:n}'),
                                               html.P(f'Average Recoveries Per Day - {avg_recoveries_per_day:n}'),
                                               html.P(f'Maximum one day increase in confirmed cases - {max_one_day_increase_confirmed_cases:n}'),
                                               html.P(f'Maximum one day increase in deaths - {max_one_day_increase_deaths:n}'),
                                               html.P(f'Maximum one day increase in recoveries - {max_one_day_increase_recovered:n}')
                                               ])),
                    dbc.Col(html.Div(children=[html.H4(f'Past 14 days (2 weeks)'),
                                               html.P(f'Confirmed Cases - {confirmed_cases_14_days:n}'),
                                               html.P(f'Active Cases - {active_cases_14_days:n}'),
                                               html.P(f'Deaths - {deaths_14_days:n}'),
                                               html.P(f'Recoveries - {recovered_14_days:n}'),
                                               html.P(f'Average Cases Per Day - {avg_cases_per_day_14_days:n}'),
                                               html.P(f'Average Deaths Per Day - {avg_deaths_per_day_14_days:n}'),
                                               html.P(f'Average Recoveries Per Day - {avg_recoveries_per_day_14_days:n}')
                                               ])),
                ]
            ),
        ]
    ),

    dcc.Graph(
        id='confirmed-cases-graph',
        figure={
            'data': [
                {'x': date_objects, 'y': confirmed_list, 'type': 'scatter'},
            ],
            'layout': {
                'title': f'Confirmed Cases in {country_name_final_representation} || Total confirmed cases: {total_confirmed_cases:n} ',
                'xaxis':{
                    'title':'Date'
                },
                'yaxis':{
                     'title':'Confirmed Cases'
                }
            }
        }
    ),

    dcc.Graph(
            id='active-cases-graph',
            figure={
                'data': [
                    {'x': date_objects, 'y': active_list, 'type': 'scatter'},
                ],
                'layout': {
                    'title': f'Active Cases in {country_name_final_representation} || Total active cases: {total_active_cases:n} ',
                    'xaxis':{
                        'title':'Date'
                    },
                    'yaxis':{
                         'title':'Active Cases'
                    }
                }
            }
        ),

    dcc.Graph(
            id='death-graph',
            figure={
                'data': [
                    {'x': date_objects, 'y': deaths_list, 'type': 'scatter'},
                ],
                'layout': {
                    'title': f'Deaths in {country_name_final_representation} || Total deaths: {total_deaths:n} ',
                    'xaxis':{
                        'title':'Date'
                    },
                    'yaxis':{
                         'title':'Total Deaths'
                    }
                }
            }
        ),

    dcc.Graph(
            id='recovered-graph',
            figure={
                'data': [
                    {'x': date_objects, 'y': recovered_list, 'type': 'scatter'},
                ],
                'layout': {
                    'title': f'Recoveries in {country_name_final_representation} || Total recovered:  {total_recovered:n} ',
                    'xaxis':{
                        'title':'Date'
                    },
                    'yaxis':{
                         'title':'Total Recovered'
                    }
                }
            }
        )
])





@app.callback(Output('output', 'children'),
              [Input('dropdown', 'value')])
def update_output_1(value):

    filtered_df = df[df['c'] == value]
    return filtered_df.iloc[0]['c']



if __name__ == '__main__':
    app.run_server(debug=True)