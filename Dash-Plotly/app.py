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

xternal_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)


global_variable=''
country_name ='india'

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
dcc.Dropdown(
            id='dropdown',
            options=[
                {'label': 'afghanistan', 'value': 'afghanistan'},
                {'label': 'ala-aland-islands', 'value': 'ala-aland-islands'},
                {'label': 'albania', 'value': 'albania'},
                {'label': 'algeria', 'value': 'algeria'},
                {'label': 'american-samoa', 'value': 'american-samoa'},
                {'label': 'andorra', 'value': 'andorra'},
                {'label': 'angola', 'value': 'angola'},
                {'label': 'anguilla', 'value': 'anguilla'},
                {'label': 'antarctica', 'value': 'antarctica'},
                {'label': 'antigua-and-barbuda', 'value': 'antigua-and-barbuda'},
                {'label': 'argentina', 'value': 'argentina'},
                {'label': 'armenia', 'value': 'armenia'},
                {'label': 'aruba', 'value': 'aruba'},
                {'label': 'australia', 'value': 'australia'},
                {'label': 'austria', 'value': 'austria'},
                {'label': 'azerbaijan', 'value': 'azerbaijan'},
                {'label': 'bahamas', 'value': 'bahamas'},
                {'label': 'bahrain', 'value': 'bahrain'},
                {'label': 'bangladesh', 'value': 'bangladesh'},
                {'label': 'barbados', 'value': 'barbados'},
                {'label': 'belarus', 'value': 'belarus'},
                {'label': 'belgium', 'value': 'belgium'},
                {'label': 'belize', 'value': 'belize'},
                {'label': 'benin', 'value': 'benin'},
                {'label': 'bermuda', 'value': 'bermuda'},
                {'label': 'bhutan', 'value': 'bhutan'},
                {'label': 'bolivia', 'value': 'bolivia'},
                {'label': 'bosnia-and-herzegovina', 'value': 'bosnia-and-herzegovina'},
                {'label': 'botswana', 'value': 'botswana'},
                {'label': 'bouvet-island', 'value': 'bouvet-island'},
                {'label': 'brazil', 'value': 'brazil'},
                {'label': 'british-indian-ocean-territory', 'value': 'british-indian-ocean-territory'},
                {'label': 'british-virgin-islands', 'value': 'british-virgin-islands'},
                {'label': 'brunei', 'value': 'brunei'},
                {'label': 'bulgaria', 'value': 'bulgaria'},
                {'label': 'burkina-faso', 'value': 'burkina-faso'},
                {'label': 'burundi', 'value': 'burundi'},
                {'label': 'cambodia', 'value': 'cambodia'},
                {'label': 'cameroon', 'value': 'cameroon'},
                {'label': 'canada', 'value': 'canada'},
                {'label': 'cape-verde', 'value': 'cape-verde'},
                {'label': 'cayman-islands', 'value': 'cayman-islands'},
                {'label': 'central-african-republic', 'value': 'central-african-republic'},
                {'label': 'chad', 'value': 'chad'},
                {'label': 'chile', 'value': 'chile'},
                {'label': 'china', 'value': 'china'},
                {'label': 'christmas-island', 'value': 'christmas-island'},
                {'label': 'cocos-keeling-islands', 'value': 'cocos-keeling-islands'},
                {'label': 'colombia', 'value': 'colombia'},
                {'label': 'comoros', 'value': 'comoros'},
                {'label': 'congo-brazzaville', 'value': 'congo-brazzaville'},
                {'label': 'congo-kinshasa', 'value': 'congo-kinshasa'},
                {'label': 'cook-islands', 'value': 'cook-islands'},
                {'label': 'costa-rica', 'value': 'costa-rica'},
                {'label': 'cote-divoire', 'value': 'cote-divoire'},
                {'label': 'croatia', 'value': 'croatia'},
                {'label': 'cuba', 'value': 'cuba'},
                {'label': 'cyprus', 'value': 'cyprus'},
                {'label': 'czech-republic', 'value': 'czech-republic'},
                {'label': 'denmark', 'value': 'denmark'},
                {'label': 'djibouti', 'value': 'djibouti'},
                {'label': 'dominica', 'value': 'dominica'},
                {'label': 'dominican-republic', 'value': 'dominican-republic'},
                {'label': 'ecuador', 'value': 'ecuador'},
                {'label': 'egypt', 'value': 'egypt'},
                {'label': 'el-salvador', 'value': 'el-salvador'},
                {'label': 'equatorial-guinea', 'value': 'equatorial-guinea'},
                {'label': 'eritrea', 'value': 'eritrea'},
                {'label': 'estonia', 'value': 'estonia'},
                {'label': 'ethiopia', 'value': 'ethiopia'},
                {'label': 'falkland-islands-malvinas', 'value': 'falkland-islands-malvinas'},
                {'label': 'faroe-islands', 'value': 'faroe-islands'},
                {'label': 'fiji', 'value': 'fiji'},
                {'label': 'finland', 'value': 'finland'},
                {'label': 'france', 'value': 'france'},
                {'label': 'french-guiana', 'value': 'french-guiana'},
                {'label': 'french-polynesia', 'value': 'french-polynesia'},
                {'label': 'french-southern-territories', 'value': 'french-southern-territories'},
                {'label': 'gabon', 'value': 'gabon'},
                {'label': 'gambia', 'value': 'gambia'},
                {'label': 'georgia', 'value': 'georgia'},
                {'label': 'germany', 'value': 'germany'},
                {'label': 'ghana', 'value': 'ghana'},
                {'label': 'gibraltar', 'value': 'gibraltar'},
                {'label': 'greece', 'value': 'greece'},
                {'label': 'greenland', 'value': 'greenland'},
                {'label': 'grenada', 'value': 'grenada'},
                {'label': 'guadeloupe', 'value': 'guadeloupe'},
                {'label': 'guam', 'value': 'guam'},
                {'label': 'guatemala', 'value': 'guatemala'},
                {'label': 'guernsey', 'value': 'guernsey'},
                {'label': 'guinea', 'value': 'guinea'},
                {'label': 'guinea-bissau', 'value': 'guinea-bissau'},
                {'label': 'guyana', 'value': 'guyana'},
                {'label': 'haiti', 'value': 'haiti'},
                {'label': 'heard-and-mcdonald-islands', 'value': 'heard-and-mcdonald-islands'},
                {'label': 'holy-see-vatican-city-state', 'value': 'holy-see-vatican-city-state'},
                {'label': 'honduras', 'value': 'honduras'},
                {'label': 'hong-kong-sar-china', 'value': 'hong-kong-sar-china'},
                {'label': 'hungary', 'value': 'hungary'},
                {'label': 'iceland', 'value': 'iceland'},
                {'label': 'india', 'value': 'india'},
                {'label': 'indonesia', 'value': 'indonesia'},
                {'label': 'iran', 'value': 'iran'},
                {'label': 'iraq', 'value': 'iraq'},
                {'label': 'ireland', 'value': 'ireland'},
                {'label': 'isle-of-man', 'value': 'isle-of-man'},
                {'label': 'israel', 'value': 'israel'},
                {'label': 'italy', 'value': 'italy'},
                {'label': 'jamaica', 'value': 'jamaica'},
                {'label': 'japan', 'value': 'japan'},
                {'label': 'jersey', 'value': 'jersey'},
                {'label': 'jordan', 'value': 'jordan'},
                {'label': 'kazakhstan', 'value': 'kazakhstan'},
                {'label': 'kenya', 'value': 'kenya'},
                {'label': 'kiribati', 'value': 'kiribati'},
                {'label': 'korea-north', 'value': 'korea-north'},
                {'label': 'korea-south', 'value': 'korea-south'},
                {'label': 'kosovo', 'value': 'kosovo'},
                {'label': 'kuwait', 'value': 'kuwait'},
                {'label': 'kyrgyzstan', 'value': 'kyrgyzstan'},
                {'label': 'lao-pdr', 'value': 'lao-pdr'},
                {'label': 'latvia', 'value': 'latvia'},
                {'label': 'lebanon', 'value': 'lebanon'},
                {'label': 'lesotho', 'value': 'lesotho'},
                {'label': 'liberia', 'value': 'liberia'},
                {'label': 'libya', 'value': 'libya'},
                {'label': 'liechtenstein', 'value': 'liechtenstein'},
                {'label': 'lithuania', 'value': 'lithuania'},
                {'label': 'luxembourg', 'value': 'luxembourg'},
                {'label': 'macao-sar-china', 'value': 'macao-sar-china'},
                {'label': 'macedonia', 'value': 'macedonia'},
                {'label': 'madagascar', 'value': 'madagascar'},
                {'label': 'malawi', 'value': 'malawi'},
                {'label': 'malaysia', 'value': 'malaysia'},
                {'label': 'maldives', 'value': 'maldives'},
                {'label': 'mali', 'value': 'mali'},
                {'label': 'malta', 'value': 'malta'},
                {'label': 'marshall-islands', 'value': 'marshall-islands'},
                {'label': 'martinique', 'value': 'martinique'},
                {'label': 'mauritania', 'value': 'mauritania'},
                {'label': 'mauritius', 'value': 'mauritius'},
                {'label': 'mayotte', 'value': 'mayotte'},
                {'label': 'mexico', 'value': 'mexico'},
                {'label': 'micronesia', 'value': 'micronesia'},
                {'label': 'moldova', 'value': 'moldova'},
                {'label': 'monaco', 'value': 'monaco'},
                {'label': 'mongolia', 'value': 'mongolia'},
                {'label': 'montenegro', 'value': 'montenegro'},
                {'label': 'montserrat', 'value': 'montserrat'},
                {'label': 'morocco', 'value': 'morocco'},
                {'label': 'mozambique', 'value': 'mozambique'},
                {'label': 'myanmar', 'value': 'myanmar'},
                {'label': 'namibia', 'value': 'namibia'},
                {'label': 'nauru', 'value': 'nauru'},
                {'label': 'nepal', 'value': 'nepal'},
                {'label': 'netherlands', 'value': 'netherlands'},
                {'label': 'netherlands-antilles', 'value': 'netherlands-antilles'},
                {'label': 'new-caledonia', 'value': 'new-caledonia'},
                {'label': 'new-zealand', 'value': 'new-zealand'},
                {'label': 'nicaragua', 'value': 'nicaragua'},
                {'label': 'niger', 'value': 'niger'},
                {'label': 'nigeria', 'value': 'nigeria'},
                {'label': 'niue', 'value': 'niue'},
                {'label': 'norfolk-island', 'value': 'norfolk-island'},
                {'label': 'northern-mariana-islands', 'value': 'northern-mariana-islands'},
                {'label': 'norway', 'value': 'norway'},
                {'label': 'oman', 'value': 'oman'},
                {'label': 'pakistan', 'value': 'pakistan'},
                {'label': 'palau', 'value': 'palau'},
                {'label': 'palestine', 'value': 'palestine'},
                {'label': 'panama', 'value': 'panama'},
                {'label': 'papua-new-guinea', 'value': 'papua-new-guinea'},
                {'label': 'paraguay', 'value': 'paraguay'},
                {'label': 'peru', 'value': 'peru'},
                {'label': 'philippines', 'value': 'philippines'},
                {'label': 'pitcairn', 'value': 'pitcairn'},
                {'label': 'poland', 'value': 'poland'},
                {'label': 'portugal', 'value': 'portugal'},
                {'label': 'puerto-rico', 'value': 'puerto-rico'},
                {'label': 'qatar', 'value': 'qatar'},
                {'label': 'romania', 'value': 'romania'},
                {'label': 'russia', 'value': 'russia'},
                {'label': 'rwanda', 'value': 'rwanda'},
                {'label': 'réunion', 'value': 'réunion'},
                {'label': 'saint-barthélemy', 'value': 'saint-barthélemy'},
                {'label': 'saint-helena', 'value': 'saint-helena'},
                {'label': 'saint-kitts-and-nevis', 'value': 'saint-kitts-and-nevis'},
                {'label': 'saint-lucia', 'value': 'saint-lucia'},
                {'label': 'saint-martin-french-part', 'value': 'saint-martin-french-part'},
                {'label': 'saint-pierre-and-miquelon', 'value': 'saint-pierre-and-miquelon'},
                {'label': 'saint-vincent-and-the-grenadines', 'value': 'saint-vincent-and-the-grenadines'},
                {'label': 'samoa', 'value': 'samoa'},
                {'label': 'san-marino', 'value': 'san-marino'},
                {'label': 'sao-tome-and-principe', 'value': 'sao-tome-and-principe'},
                {'label': 'saudi-arabia', 'value': 'saudi-arabia'},
                {'label': 'senegal', 'value': 'senegal'},
                {'label': 'serbia', 'value': 'serbia'},
                {'label': 'seychelles', 'value': 'seychelles'},
                {'label': 'sierra-leone', 'value': 'sierra-leone'},
                {'label': 'singapore', 'value': 'singapore'},
                {'label': 'slovakia', 'value': 'slovakia'},
                {'label': 'slovenia', 'value': 'slovenia'},
                {'label': 'solomon-islands', 'value': 'solomon-islands'},
                {'label': 'somalia', 'value': 'somalia'},
                {'label': 'south-africa', 'value': 'south-africa'},
                {'label': 'south-georgia-and-the-south-sandwich-islands',
                 'value': 'south-georgia-and-the-south-sandwich-islands'},
                {'label': 'south-sudan', 'value': 'south-sudan'},
                {'label': 'spain', 'value': 'spain'},
                {'label': 'sri-lanka', 'value': 'sri-lanka'},
                {'label': 'sudan', 'value': 'sudan'},
                {'label': 'suriname', 'value': 'suriname'},
                {'label': 'svalbard-and-jan-mayen-islands', 'value': 'svalbard-and-jan-mayen-islands'},
                {'label': 'swaziland', 'value': 'swaziland'},
                {'label': 'sweden', 'value': 'sweden'},
                {'label': 'switzerland', 'value': 'switzerland'},
                {'label': 'syria', 'value': 'syria'},
                {'label': 'taiwan', 'value': 'taiwan'},
                {'label': 'tajikistan', 'value': 'tajikistan'},
                {'label': 'tanzania', 'value': 'tanzania'},
                {'label': 'thailand', 'value': 'thailand'},
                {'label': 'timor-leste', 'value': 'timor-leste'},
                {'label': 'togo', 'value': 'togo'},
                {'label': 'tokelau', 'value': 'tokelau'},
                {'label': 'tonga', 'value': 'tonga'},
                {'label': 'trinidad-and-tobago', 'value': 'trinidad-and-tobago'},
                {'label': 'tunisia', 'value': 'tunisia'},
                {'label': 'turkey', 'value': 'turkey'},
                {'label': 'turkmenistan', 'value': 'turkmenistan'},
                {'label': 'turks-and-caicos-islands', 'value': 'turks-and-caicos-islands'},
                {'label': 'tuvalu', 'value': 'tuvalu'},
                {'label': 'uganda', 'value': 'uganda'},
                {'label': 'ukraine', 'value': 'ukraine'},
                {'label': 'united-arab-emirates', 'value': 'united-arab-emirates'},
                {'label': 'united-kingdom', 'value': 'united-kingdom'},
                {'label': 'united-states', 'value': 'united-states'},
                {'label': 'uruguay', 'value': 'uruguay'},
                {'label': 'us-minor-outlying-islands', 'value': 'us-minor-outlying-islands'},
                {'label': 'uzbekistan', 'value': 'uzbekistan'},
                {'label': 'vanuatu', 'value': 'vanuatu'},
                {'label': 'venezuela', 'value': 'venezuela'},
                {'label': 'vietnam', 'value': 'vietnam'},
                {'label': 'virgin-islands', 'value': 'virgin-islands'},
                {'label': 'wallis-and-futuna-islands', 'value': 'wallis-and-futuna-islands'},
                {'label': 'western-sahara', 'value': 'western-sahara'},
                {'label': 'yemen', 'value': 'yemen'},
                {'label': 'zambia', 'value': 'zambia'},
                {'label': 'zimbabwe', 'value': 'zimbabwe'}
            ],
            value='united-states'
        ),
        html.Div(id='dd-output-container'),
    html.H1(children=f'Statistics for {country_name_final_representation} {a}'),

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


@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('dropdown', 'value')])
def update_output(value):
    return value
    copy(a,value)




if __name__ == '__main__':
    app.run_server(debug=True)