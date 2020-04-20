import pandas as pd
import numpy as np
import json
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import State, Input, Output
import plotly as py
from plotly import graph_objs as go
import pathlib



with open("/Users/lly/dash_az/Data/us-arizona-counties.json") as geocounty:
    azgeo = json.load(geocounty)


arizona_unemploy = pd.read_csv("/Users/lly/dash_az/Data/arizona_unemploy.csv")

#read population dataset
azPPL = pd.read_csv("/Users/lly/dash_az/Data/population.csv")
azPPL['CTYNAME']= azPPL['CTYNAME'].str.replace("County", "")

arizona_residentPop = pd.read_csv("/Users/lly/dash_az/Data/arizona_unemploy.csv")

arizona_commute = pd.read_csv("/Users/lly/dash_az/Data/arizona_commute.csv")

arizona_medianIncome = pd.read_csv("/Users/lly/dash_az/Data/arizona_medianIncome.csv")

arizona_edu = pd.read_csv("/Users/lly/dash_az/Data/arizona_edu.csv")

acsdata = pd.read_csv("/Users/lly/Data/ACS.csv")

#filter gender data
filter_pct = ["COUNTY", "PCT_FEMALE", "PCT_MALE"]
arizona_sexPCT = acsdata.loc[:, filter_pct]
arizona_gender = arizona_sexPCT.rename(columns = {"PCT_MALE": "Male", "PCT_FEMALE": "Female"})

#read age %
filter_age = ["COUNTY", "PCT_UNDER5", "PCT_AGE5TO9", "PCT_AGE10TO14", "PCT_AGE15TO19", "PCT_AGE20TO24", "PCT_AGE25TO34", "PCT_AGE35TO44", "PCT_AGE45TO54",
    "PCT_AGE55TO59","PCT_AGE60TO64","PCT_AGE65TO74", "PCT_AGE75TO84", "PCT_AGE85PLUS"]
df_age = acsdata.loc[:, filter_age]
arizona_age = df_age.rename(columns = {"PCT_UNDER5" : "UNDER5", "PCT_AGE5TO9": "AGE5TO9", "PCT_AGE10TO14": "AGE10TO14", "PCT_AGE15TO19": "AGE15TO19", "PCT_AGE20TO24": "AGE20TO24",
    "PCT_AGE25TO34": "AGE25TO34", "PCT_AGE35TO44": "AGE35TO44", "PCT_AGE45TO54": "AGE45TO54",
    "PCT_AGE55TO59": "AGE55TO59", "PCT_AGE60TO64": "AGE60TO64","PCT_AGE65TO74": "AGE65TO74", "PCT_AGE75TO84": "AGE75TO84", "PCT_AGE85PLUS": "AGE85PLUS"})
#reduce category levels
arizona_age['UNDER19'] = arizona_age["UNDER5"] + arizona_age["AGE5TO9"] + arizona_age["AGE10TO14"] + arizona_age["AGE15TO19"]
arizona_age['AGE20TO34'] = arizona_age["AGE20TO24"] + arizona_age["AGE25TO34"]
arizona_age["AGE35TO54"] = arizona_age["AGE35TO44"] + arizona_age["AGE45TO54"]
arizona_age["AGE55TO74"] = arizona_age["AGE55TO59"] + arizona_age["AGE60TO64"] + arizona_age["AGE65TO74"]
arizona_age["75PLUS"] = arizona_age["AGE75TO84"] + arizona_age["AGE85PLUS"]
arizona_ageMerge = arizona_age[["COUNTY", "UNDER19", "AGE20TO34", "AGE35TO54", "AGE55TO74", "75PLUS"]].copy()


#read race %
filter_race = ["COUNTY", "PCT_HISPANIC", "PCT_WHITE_NON_HISPANIC", "PCT_BLACK_NON_HISPANIC", "PCT_NATIVE_NON_HISPANIC", "PCT_ASIAN_NON_HISPANIC", "PCT_PACIFIC_NON_HISPANIC", "PCT_OTHER_NON_HISPANIC", "PCT_TWO_OR_MORE_NON_HISPANIC"]
df_race = acsdata.loc[:, filter_race]
df_race["HISPANIC"] = df_race["PCT_HISPANIC"]
df_race["WHITE"] = df_race["PCT_WHITE_NON_HISPANIC"]
df_race["BLACK"] = df_race["PCT_BLACK_NON_HISPANIC"]
df_race["ASIAN"] = df_race["PCT_ASIAN_NON_HISPANIC"]
df_race["NATIVE"] = df_race["PCT_NATIVE_NON_HISPANIC"]
df_race["OTHER"] = df_race["PCT_PACIFIC_NON_HISPANIC"] + df_race["PCT_OTHER_NON_HISPANIC"] + df_race["PCT_TWO_OR_MORE_NON_HISPANIC"]
arizona_race = df_race[["COUNTY", "HISPANIC", "WHITE", "BLACK", "ASIAN", "NATIVE", "OTHER"]].copy()


#read degree%
filter_degree = ["COUNTY", "PCT_LT9GRADE", "PCT_NOHSDIPLOMA", "PCT_HSGRAD", "PCT_SOMECOLLEGE", "PCT_ASSOCIATES", "PCT_BACHELORS", "PCT_GRADPROF"]
df_degree = acsdata.loc[:, filter_degree]
arizona_degree = df_degree.rename(columns = {"PCT_LT9GRADE": "LESS_THAN_9TH_GRADE", "PCT_NOHSDIPLOMA": "NO_HIGHSCHOOL", "PCT_HSGRAD": "HIGH_SCHOOL", "PCT_SOMECOLLEGE": "SOME_COLLEGE", "PCT_ASSOCIATES": "ASSOCIATES", "PCT_BACHELORS": "BACHELORS", "PCT_GRADPROF": "GRAD_OR_HIGHER"})


#read poverty Rate
filter_poverty = ["COUNTY", "PCT_INCOME_BELOW_POVERTY"]
df_poverty = acsdata.loc[:, filter_poverty]
arizona_poverty = df_poverty.rename(columns = {"PCT_INCOME_BELOW_POVERTY": "POVERTY_RATE"})

arizona_1bd = pd.read_csv("/Users/lly/dash_az/Data/arizona_1bd.csv")

arizona_2bd = pd.read_csv("/Users/lly/dash_az/Data/arizona_2bd.csv")

arizona_3bd = pd.read_csv("/Users/lly/dash_az/Data/arizona_3bd.csv")

arizona_4bd = pd.read_csv("/Users/lly/dash_az/Data/arizona_4bd.csv")

arizona_5bd = pd.read_csv("/Users/lly/dash_az/Data/arizona_5bd.csv")

#read national park dataset
with open("/Users/lly/dash_az/Data/national-parks.json") as parks:
    geoParks = json.load(parks)
state = ["Arizona"]
azparks = [d for d in geoParks if d['State'] in state]

df_azparks = pd.DataFrame(azparks)
df_azparks = df_azparks[~df_azparks['Location Name'].str.startswith('Glen')]

df_azdisaster = pd.read_csv("/Users/lly/dash_az/Data/df_azdisaster.csv")
#read median housing growth rate dataset
arizona_mHouseGrowth = pd.read_csv("/Users/lly/dash_az/Data/arizona_mHouse_growth.csv")

arizona_climate = pd.read_csv("/Users/lly/dash_az/Data/arizona_climate.csv")

arizona_occpwage = pd.read_csv("/Users/lly/dash_az/Data/arizona_occpwage.csv")
#####################################################################################################

app = dash.Dash()

#app.scripts.config.serve_locally = True

server = app.server

#choropleth map
def az_map():

    zmin, zmax = np.min(azPPL["Pop"]), np.max(azPPL["Pop"])

    az_data = [
        go.Choropleth(
            colorbar = dict(
                tickvals = [zmin, zmax],
                tickformat = ".2f",
                ticks = "",
                title = "Total Population",
                titlefont = dict(family = "Comic Sans MS", color = "#fae7cb", size = 15),
                thickness = 30,
                len = 0.7,
                tickcolor = "#fae7cb",
                tickfont = dict(color = "#fae7cb")
                            ),
            colorscale = [[0, "#f4eeff"],
                         [0.25, "#dcd6f7"],
                         [0.50, "#a6b1e1"],
                         [0.75, "#b590ca"],
                         [1, "#424874"]],
            reversescale = False,
            geojson = azgeo,
            featureidkey = "properties.name",
            locations = ['Maricopa', 'Pima', 'Pinal', 'Yavapai', 'Yuma', 'Mohave',
                'Coconino', 'Cochise', 'Navajo', 'Apache', 'Gila', 'Santa Cruz',
                'Graham', 'La Paz', 'Greenlee'],
            z = azPPL["Pop"].tolist(),
            marker = dict(line = {"color": "#fae7cb"}),
            marker_line_width = 3,
            locationmode = "geojson-id",
            customdata = azPPL["CTYNAME"].tolist(),
            hoverinfo = 'location+z',


        )
    ]

    layout = dict(
        title = '<br>' + '<b>            || Select a County First ||<b>',
        margin = dict(l=0, r=0, t=70, b=0),
        clickmode = "event+select",
        paper_bgcolor = "#252e3f",
        font = dict(family = 'Comic Sans MS', color = '#b3a4c6', size = 16),
        )


    fig = go.Figure(data = az_data, layout = layout)

    fig.update_geos(fitbounds="locations", visible=False)

    fig.add_traces(
        go.Scattergeo(
            lon = df_azparks["Longitude"],
            lat = df_azparks["Latitude"],
            text = df_azparks["Location Name"],
            mode = "markers",
            marker = dict(
            size = 12,
            symbol = "star-triangle-up",
            color = '#639a67',

        ),
    ))
    fig.update_layout(geo=dict(bgcolor= "#252e3f"))
    return fig


    #options = [{'label': i, 'value': i} for i in arizona_unemploy.columns]

app.layout =  html.Div(style = {'backgroundColor': '#1f2630', 'margin': '0 auto', 'padding': '0', 'width': '100%'},
    className = "Row",
    children = [
        html.Div(style = {'backgroundColor': '#b3a4c6', 'fontWeight': 'bold', 'color': '#fae7cb',
            'verticalAlign': 'top', 'marginBottom': '1%',
            'box-shadow': '0px 0px 0px grey', 'border': '1px solid grey', 'border-top': '#fae7cb solid .2rem'},
            id = 'header',
            children = [
                html.H1(style={'marginLeft': '3%','font-size': '24px'},
                    children = ("A r i z o n a")),
                ]
            ),
        html.Div(
            id = "numberPlate",
            style = {'marginLeft': '4%', 'marginBottom': '1.0%'},
            children = [
                html.Div(
                    style ={'width': '16%','backgroundColor': '#c6b3a4','display': 'inline-block', 'verticalAlign': 'top', 'box-shadow': '10px 10px 20px grey',
                        'border': '1px solid grey', 'border-top': '#fae7cb solid .2rem', 'height': '100px', 'marginRight': '4%'},
                        children = [
                            html.H3(style = {'textAlign': 'center',
                                    'fontWeight': 'bold', 'color': '#fbeeda', 'font-family': 'Comic Sans MS', 'marginLeft': '5%', 'font-size': '18px'},
                                children = [
                                    html.P("Population Growth")
                                ]
                            ),
                            html.Div(id = "pplGrowthRate",
                                style = {'textAlign': 'center', 'color': '#fbeeda', 'padding': '.1rem', 'fontWeight': 'bolder', 'font-size': '22px'},
                                )
                        ]
                    ),
                html.Div(
                    style ={'width': '16%', 'backgroundColor': '#c6a4a6', 'display': 'inline-block',
                        'marginRight': '4%', 'verticalAlign': 'top',
                        'box-shadow': '10px 10px 20px grey', 'border': '1px solid grey', 'border-top': '#fae7cb solid .2rem', 'height': '100px'},
                        children = [
                            html.H3(style = {'textAlign': 'center',
                                'fontWeight': 'bold', 'color': '#fbeeda', 'font-family': 'Comic Sans MS', 'font-size': '18px'},
                                children = [
                                    html.P(
                                        "Poverty Rate")
                                ]
                            ),
                            html.H3(id = "povertyRate",
                                style = {'textAlign': 'center', 'color': '#fbeeda', 'padding': '.1rem', 'fontWeight': 'bold', 'font-size': '22px'})

                        ]
                    ),
                html.Div(
                    style ={'width': '16%', 'backgroundColor': '#a6c6a4', 'display': 'inline-block',
                        'marginRight': '4%', 'verticalAlign': 'top',
                        'box-shadow': '10px 10px 20px grey', 'border': '1px solid grey', 'border-top': '#fae7cb solid .2rem', 'height': '100px'},
                        children = [
                            html.H3(style = {'textAlign': 'center',
                                'fontWeight': 'bold', 'color': '#fbeeda', 'font-family': 'Comic Sans MS', 'font-size': '16px'},
                                children = [
                                    html.P(
                                        "Median Housing Price Growth")
                                ]
                            ),
                            html.H3(style = {'textAlign': 'center', 'color': '#fbeeda', 'padding': '.1rem', 'fontWeight': 'bold', 'font-size': '22px'},
                                id = 'mhpGrowthRate')
                        ]
                    ),
                html.Div(
                    style ={'width': '16%', 'backgroundColor': '#ac9489', 'display': 'inline-block',
                        'marginRight': '4%', 'verticalAlign': 'top',
                        'box-shadow': '10px 10px 20px grey', 'border': '1px solid grey', 'border-top': '#fae7cb solid .2rem', 'height': '100px'},
                        children = [
                            html.H3(style = {'textAlign': 'center',
                                'fontWeight': 'bold', 'color': '#fbeeda', 'font-family': 'Comic Sans MS', 'font-size': '18px'},
                                children = [
                                    html.P(
                                        "Average Sunny Days")
                                ]
                            ),
                            html.H3(style = {'textAlign': 'center', 'color': '#fbeeda', 'padding': '.1rem', 'fontWeight': 'bold', 'font-size': '22px'},
                                id = "avgSunny")
                        ]
                    ),
                html.Div(
                    style ={'width': '16%', 'backgroundColor': '#a4a6c6', 'display': 'inline-block',
                        'verticalAlign': 'top','box-shadow': '10px 10px 20px grey', 'border': '1px solid grey', 'border-top': '#fae7cb solid .2rem', 'height': '100px'},
                        children = [
                            html.H3(style = {'textAlign': 'center',
                                'fontWeight': 'bold', 'color': '#fbeeda', 'font-family': 'Comic Sans MS', 'font-size': '18px'},
                                children = [
                                    html.P(
                                        "Winter Low")
                                ]
                            ),
                            html.H3(style = {'textAlign': 'center', 'color': '#fbeeda', 'padding': '.1rem', 'fontWeight': 'bold', 'font-size': '22px'},
                                id = "winderlow")
                        ]
                    ),
                ]
            ),
        html.Div(
            style = {'width': '27%', 'display': 'inline-block', 'marginRight': '1%', 'marginLeft': '2%', 'marginTop': '1%', 'marginBottom': '1%'},
            id = "bedroom-outer",
            children = [
                html.Div(style = {'width' : '200px', 'padding': '3px', 'border': '3px solid #b3a4c6', 'border-radius': '15px', 'backgroundColor': 'rgb(200, 133, 243)'},
                    children = [
                        dcc.Dropdown(style = {'color': 'rgb(200, 133, 243)', 'border-radius': '15px', 'content': '#FFFFFF'},
                        id = "first_dropdown",
                        options = [{'label': 'One Bedroom', 'value': 'bed1'}, {'label': 'Two Bedroom', 'value': 'bed2'},
                            {'label': 'Three Bedroom', 'value': 'bed3'}, {'label': 'Four Bedroom', 'value': 'bed4'},
                            {'label': 'Five or more', 'value': 'bed5'}],
                        value = 'bed1'

                    )
                ]
            ),
                html.Div(
                    children = [dcc.Graph(id = "bedroom")]
                )
            ]
        ),
        html.Div(
            style = {'width': '40%', 'display': 'inline-block', 'marginRight': '1%', 'marginTop': '1%', 'marginBottom': '1%'},
            id = "map-outer",
            children = [
                html.Div(style = {'color': '#363062'},
                    children = [dcc.Graph(id = "choropleth", figure = az_map())]
                )
            ]
        ),
        html.Div(
            style = {'width': '27%', 'display': 'inline-block', 'marginTop': '1%', 'marginBottom': '1%'},
            id = "racePie-outer",
            children = [
                html.Div(
                    children = [dcc.Graph(id = "racePie")]
                )
            ]
        ),
        html.Div(
            style = {'width': '27%', 'display': 'inline-block', 'marginRight': '1%', 'marginLeft' : '2%', 'marginBottom': '1%'},
            id = "unemployRate-outer",
            children = [
                html.Div(
                    children = [dcc.Graph(id = "unemployRate")]
                )
            ]
        ),
        html.Div(
            style = {'width': '40%', 'display': 'inline-block', 'marginTop': '1%',  'marginRight': '1%', 'marginBottom': '1%'},
            id = "degree-outer",
            children = [
                html.Div(
                    children = [dcc.Graph(id = "degree")]
                )
            ]
        ),
        html.Div(
            style = {'width': '27%', 'display': 'inline-block', 'marginRight': '1%', 'marginTop': '1%', 'marginBottom': '1%'},
            id = "mHouseIncome-outer",
            children = [
                html.Div(
                    children = [dcc.Graph(id = "mHouseIncome")]
                )
            ]
        ),
        html.Div(
            style = {'width': '27%', 'display': 'inline-block', 'marginLeft': '2%', 'marginRight': '1%', 'marginBottom': '1%'},
            id = "agePie-outer",
            children = [
                html.Div(
                    children = [dcc.Graph(id = "agePie")]
                )
            ]
        ),
        html.Div(
            style = {'width': '40%', 'display': 'inline-block', 'marginRight': '1%', 'marginTop': '1%', 'marginBottom': '1%'},
            id = "disaster-outer",
            children = [
                html.Div(
                    children = [dcc.Graph(id = "disaster")]
                )
            ]
        ),
        html.Div(
            style = {'width': '27%', 'display': 'inline-block', 'marginRight': '1%', 'marginTop': '1%', 'marginBottom': '1%'},
            id = "residentPop-outer",
            children = [
                html.Div(
                    children = [dcc.Graph(id = "residentPop")]
                )
            ]
        ),
        html.Div(
            style = {'width': '27%', 'display': 'inline-block', 'marginTop': '1%', 'marginRight': '1%', 'marginLeft': '2%'},
            id = "gender-outer",
            children = [
                html.Div(
                    children = [dcc.Graph(id = "genderPie")]
                )
            ]
        ),
        html.Div(
            style = {'width': '40%', 'display': 'inline-block', 'marginRight': '1%', 'marginTop': '1%'},
            id = "commuteWork-outer",
            children = [
                html.Div(
                    children = [dcc.Graph(id = "commuteWork")]
                )
            ]
        ),
        html.Div(
            style = {'width': '27%', 'display': 'inline-block', 'marginRight': '1%'},
            id = "education-outer",
            children = [
                html.Div(
                    children = [dcc.Graph(id = "education")]
                )
            ]
        ),
    ]
)

def generate_unemploy_rate(county):
    filter = ["DATE", county]
    filter_df = arizona_unemploy[(filter)]
    first_col = filter_df.iloc[:, 1]
    return{
        'data': [
            go.Scatter(
                x = filter_df.DATE,
                y = first_col,
                line = dict(color = 'rgb(200, 133, 243)', width = 3),

            )
        ],
        'layout': go.Layout(
            title = "Unemployment Rate in <b>{0}</b>, <b>{1}</b>".format(county, "AZ"),
            font = dict(family = 'Comic Sans MS', color = '#fae7cb'),
            yaxis = {'title': 'Percent', 'color': '#fae7cb'},
            xaxis = {'title': 'Time', 'color': '#fae7cb'},
            paper_bgcolor = "#252e3f",
            plot_bgcolor = "#252e3f"

        )
    }

def generate_residentPop(county):
    filter = ["DATE", county]
    filter_df = arizona_residentPop[(filter)]
    first_col = filter_df.iloc[:, 1]
    return{
        'data': [
            go.Scatter(
                x = filter_df.DATE,
                y = first_col,
                line = dict(color = 'rgb(200, 133, 243)', width = 3),

            )
        ],
        'layout': go.Layout(
            title = "Resident Population in <b>{0}</b>, <b>{1}</b>".format(county, "AZ"),
            font = dict(family = 'Comic Sans MS', color = '#fae7cb'),
            xaxis = {'title': 'Time', 'color': '#fae7cb'},
            yaxis = {'title': 'Thousands of Persons', 'color': '#fae7cb'},
            paper_bgcolor = "#252e3f",
            plot_bgcolor = "#252e3f"
        )
    }

def generate_commuteWork(county):
    filter = ["DATE", county]
    filter_df = arizona_commute[(filter)]
    first_col = filter_df.iloc[:, 1]
    return{
        'data': [
            go.Scatter(
                x = filter_df.DATE,
                y = first_col,
                line = dict(color = 'rgb(200, 133, 243)', width = 3),

            )
        ],
        'layout': go.Layout(
            title = "Mean Commuting Time for Workers in <b>{0}</b>, <b>{1}</b>".format(county, "AZ"),
            yaxis = {'title': 'Minutes'},
            font = dict(family = 'Comic Sans MS', color = '#fae7cb'),
            xaxis = {'title': 'Time', 'color': '#fae7cb'},
            paper_bgcolor = "#252e3f",
            plot_bgcolor = "#252e3f"

        )
    }

def generate_mHouseIncome(county):
    filter = ["DATE", county]
    filter_df = arizona_medianIncome[(filter)]
    first_col = filter_df.iloc[:, 1]
    return{
        'data': [
            go.Scatter(
                x = filter_df.DATE,
                y = first_col,
                line = dict(color = 'rgb(200, 133, 243)', width = 3),

            )
        ],
        'layout': go.Layout(
            title = "Estimate of Median Household Income for <b>{0}</b>, <b>{1}</b>".format(county, "AZ"),
            yaxis = {'title': 'Dollars'},
            font = dict(family = 'Comic Sans MS', color = '#fae7cb'),
            xaxis = {'title': 'Time', 'color': '#fae7cb'},
            paper_bgcolor = "#252e3f",
            plot_bgcolor = "#252e3f"

        )
    }

def generate_education(county):
    filter = ["DATE", county]
    filter_df = arizona_edu[(filter)]
    first_col = filter_df.iloc[:, 1]
    return{
        'data': [
            go.Scatter(
                x = filter_df.DATE,
                y = first_col,
                line = dict(color = 'rgb(200, 133, 243)', width = 3),

            )
        ],
        'layout': go.Layout(
            title = "Bachelor's Degree or Higher in <b>{0}</b>, <b>{1}</b>".format(county, "AZ"),
            yaxis = {'title': 'Percent'},
            font = dict(family = 'Comic Sans MS', color = '#fae7cb'),
            xaxis = {'title': 'Time', 'color': '#fae7cb'},
            paper_bgcolor = "#252e3f",
            plot_bgcolor = "#252e3f"

        )
    }

def generate_gender_pie(county):
    cty = []
    cty.append(county)
    filter_df = arizona_gender[arizona_gender['COUNTY'].isin(cty)]
    pct = filter_df.iloc[:,1:3].values.tolist()
    groups = filter_df.columns[1:3].tolist()
    colors = ['#e98074', '9fcbdf']
    return{
        'data': [
            go.Pie(
                labels = groups,
                values = pct[0],
                textfont = dict(size = 15),
                marker = dict(colors = colors,
                line = dict(color = '#fae7cb', width = 2))
            )
        ],
        'layout': go.Layout(
            title = "Population by Gender in <b>{0}</b>, <b>{1}</b>".format(county, "AZ"),
            font = dict(family = 'Comic Sans MS', color = '#fae7cb'),
            paper_bgcolor = "#252e3f",
            plot_bgcolor = "#252e3f"
            )
    }

def generate_age_pie(county):
    cty = []
    cty.append(county)
    filter_df = arizona_ageMerge[arizona_ageMerge['COUNTY'].isin(cty)]
    pct = filter_df.iloc[:, 1:6].values.tolist()
    groups = filter_df.columns[1:6].tolist()
    colors = ['#024170', '#e98074', 'fef9c7', 'fce181', '9fcbdf']
    return{
        'data': [
            go.Pie(
                labels = groups,
                values = pct[0],
                textfont = dict(size = 15),
                marker = dict(colors = colors,
                line = dict(color = '#fae7cb', width = 2))
            )
        ],
        'layout': go.Layout(
            title = "Population by Age Groups in <b>{0}</b>, <b>{1}</b>".format(county, "AZ"),
            font = dict(family = 'Comic Sans MS', color = '#fae7cb'),
            paper_bgcolor = "#252e3f",
            plot_bgcolor = "#252e3f"
        )
    }

def generate_race_pie(county):
    cty = []
    cty.append(county)
    filter_df = arizona_race[arizona_race['COUNTY'].isin(cty)]
    pct = filter_df.iloc[:, 1:7].values.tolist()
    groups = filter_df.columns[1:7].tolist()
    colors = ['#024170', '#e98074', 'fef9c7', 'fce181', '9fcbdf', '#d6fdcc']
    return{
        'data': [
            go.Pie(
                labels = groups,
                values = pct[0],
                textfont = dict(size = 15),
                marker = dict(colors = colors,
                line = dict(color = '#fae7cb', width = 2))
            )
        ],
        'layout': go.Layout(
            title = "Population by Race in <b>{0}</b>, <b>{1}</b>".format(county, "AZ"),
            font = dict(family = 'Comic Sans MS', color = '#fae7cb'),
            paper_bgcolor = "#252e3f",
            plot_bgcolor = "#252e3f"
        )
    }

def generate_degree_bar(county):
    cty = []
    cty.append(county)
    filter_df = arizona_degree[arizona_degree['COUNTY'].isin(cty)]
    pct = filter_df.iloc[:, 1:8].values.tolist()
    groups = filter_df.columns[1:8].tolist()
    return{
        'data': [
            go.Bar(
                x = groups,
                y = pct[0],
                marker_color = 'rgb(200, 133, 243)',
                opacity = 0.3,
                marker_line_width = 1.5
                )
        ],
        'layout': go.Layout(
            margin = dict(b=100),
            title = "Education Level in <b>{0}</b>, <b>{1}</b>".format(county, "AZ"),
            font = dict(family = 'Comic Sans MS', color = '#fae7cb'),
            yaxis = {'title': 'Percent %'},
            paper_bgcolor = "#252e3f",
            plot_bgcolor = "#252e3f"
        )
    }
def generate_disaster_histogram(county):
    filter_df = df_azdisaster[df_azdisaster['designatedArea'].str.contains(county)]
    return{
        'data': [
            go.Histogram(
                y = filter_df['incidentType'],
                marker_color = 'rgb(200, 133, 243)',
                opacity = 0.3,
                marker_line_width = 1.5
                )
        ],
        'layout': go.Layout(
            margin = dict(l=100, r=80, t=80, b=80),
            title = "Disaster in <b>{0}</b>, <b>{1}</b> -- since 1966 to 2020".format(county, "AZ"),
            font = dict(family = 'Comic Sans MS', color = '#fae7cb'),
            xaxis = {'title': 'Count'},
            paper_bgcolor = "#252e3f",
            plot_bgcolor = "#252e3f"
        )
    }

def generate_growth_rate(county):
    filter_df = azPPL[azPPL['CTYNAME'].str.contains(county)]
    rate = filter_df.iloc[:,2:3].values[0][0]

    return '{:.2f}%'.format(rate)

def generate_poverty_rate(county):
    filter_df = arizona_poverty[arizona_poverty['COUNTY'].str.contains(county)]
    rate = filter_df.iloc[:,1:2].values[0][0]

    return '{:.2f}%'.format(rate)

def generate_mhgrowth_rate(county):
    filter_df = arizona_mHouseGrowth[arizona_mHouseGrowth['County'].str.contains(county)]
    rate = filter_df.iloc[:,1:2].values[0][0]

    return rate

def generate_avgSunny_days(county):
    filter_df = arizona_climate[arizona_climate['CTYNAME'].str.contains(county)]
    days = filter_df.iloc[:,1:2].values[0][0]

    return days

def generate_winter_low(county):
    filter_df = arizona_climate[arizona_climate['CTYNAME'].str.contains(county)]
    lowTemp = filter_df.iloc[:,2:3].values[0][0]

    return '{}°'.format(lowTemp)

def generate_house_graph(county, dd_select):

    if dd_select == "bed1":
        housedata = arizona_1bd
        print(housedata)
    elif dd_select == "bed2":
        housedata = arizona_2bd
        print(housedata)
    elif dd_select == "bed3":
        housedata = arizona_3bd
        print(housedata)
    elif dd_select == "bed4":
        housedata = arizona_4bd
        print(housedata)
    else:
        housedata = arizona_5bd
        print(housedata)
    date = housedata.columns[2:52].tolist()
    filter_df = housedata[housedata['COUNTY'].str.contains(county)]
    prices = filter_df.iloc[:, 2:52].values

    return{
        'data': [
            go.Scatter(
                x = date,
                y = prices[0],
                line = dict(color = 'rgb(200, 133, 243)', width = 3),

            )
        ],
        'layout': go.Layout(
            title = "Home Values in <b>{0}</b>, <b>{1}</b>".format(county, "AZ"),
            yaxis = {'title': 'Dollars'},
            font = dict(family = 'Comic Sans MS', color = '#fae7cb'),
            xaxis = {'title': 'Time', 'color': '#fae7cb'},
            paper_bgcolor = "#252e3f",
            plot_bgcolor = "#252e3f"

        )
    }



@app.callback(Output("unemployRate", "figure"),
    [Input("choropleth", "clickData"), Input("choropleth", "figure")])
def update_unemploy_rate(choro_click, choro_figure):
    if choro_click is not None:
        county = []
        for point in choro_click["points"]:
            county.append(point["location"])
        return generate_unemploy_rate(county[0])
    else:
        return generate_unemploy_rate("Maricopa")

@app.callback(Output("residentPop", "figure"),
    [Input("choropleth", "clickData"), Input("choropleth", "figure")])
def update_residentPop(choro_click, choro_figure):
    if choro_click is not None:
        county = []
        for point in choro_click["points"]:
            county.append(point["location"])
        return generate_residentPop(county[0])
    else:
        return generate_residentPop("Maricopa")

@app.callback(Output("commuteWork", "figure"),
    [Input("choropleth", "clickData"), Input("choropleth", "figure")])
def update_commuteWork(choro_click, choro_figure):
    if choro_click is not None:
        county = []
        for point in choro_click["points"]:
            county.append(point["location"])
        return generate_commuteWork(county[0])
    else:
        return generate_commuteWork("Maricopa")

@app.callback(Output("mHouseIncome", "figure"),
    [Input("choropleth", "clickData"), Input("choropleth", "figure")])
def update_mHouseIncome(choro_click, choro_figure):
    if choro_click is not None:
        county = []
        for point in choro_click["points"]:
            county.append(point["location"])
        return generate_mHouseIncome(county[0])
    else:
        return generate_mHouseIncome("Maricopa")

@app.callback(Output("education", "figure"),
    [Input("choropleth", "clickData"), Input("choropleth", "figure")])
def update_education(choro_click, choro_figure):
    if choro_click is not None:
        county = []
        for point in choro_click["points"]:
            county.append(point["location"])
        return generate_education(county[0])
    else:
        return generate_education("Maricopa")

@app.callback(Output("genderPie", "figure"),
    [Input("choropleth", "clickData"), Input("choropleth", "figure")])
def update_gender_pie(choro_click, choro_figure):
    if choro_click is not None:
        county = []
        for point in choro_click["points"]:
            county.append(point["location"])
        return generate_gender_pie(county[0])
    else:
        return generate_gender_pie("Maricopa")

@app.callback(Output("agePie", "figure"),
    [Input("choropleth", "clickData"), Input("choropleth", "figure")])
def update_age_pie(choro_click, choro_figure):
    if choro_click is not None:
        county = []
        for point in choro_click["points"]:
            county.append(point["location"])
        return generate_age_pie(county[0])
    else:
        return generate_age_pie("Maricopa")

@app.callback(Output("racePie", "figure"),
    [Input("choropleth", "clickData"), Input("choropleth", "figure")])
def update_race_pie(choro_click, choro_figure):
    if choro_click is not None:
        county = []
        for point in choro_click["points"]:
            county.append(point["location"])
        return generate_race_pie(county[0])
    else:
        return generate_race_pie("Maricopa")

@app.callback(Output("disaster", "figure"),
    [Input("choropleth", "clickData"), Input("choropleth", "figure")])
def update_disaster_histogram(choro_click, choro_figure):
    if choro_click is not None:
        county = []
        for point in choro_click["points"]:
            county.append(point["location"])
        return generate_disaster_histogram(county[0])
    else:
        return generate_disaster_histogram("Maricopa")

@app.callback(Output("degree", "figure"),
    [Input("choropleth", "clickData"), Input("choropleth", "figure")])
def update_degree_pie(choro_click, choro_figure):
    if choro_click is not None:
        county = []
        for point in choro_click["points"]:
            county.append(point["location"])
        return generate_degree_bar(county[0])
    else:
        return generate_degree_bar("Maricopa")

@app.callback(Output("pplGrowthRate", "children"),
    [Input("choropleth", "clickData"), Input("choropleth", "figure")])
def update_ppl_growth(choro_click, choro_figure):
    if choro_click is not None:
        county = []
        for point in choro_click["points"]:
            county.append(point["location"])
        return generate_growth_rate(county[0])
    else:
        return generate_growth_rate("Maricopa")

@app.callback([Output("mhpGrowthRate", "children"), Output("avgSunny", "children"), Output("winderlow", "children")],
    [Input("choropleth", "clickData"), Input("choropleth", "figure")])
def update_ppl_growth(choro_click, choro_figure):
    if choro_click is not None:
        county = []
        for point in choro_click["points"]:
            county.append(point["location"])
        return (
            generate_mhgrowth_rate(county[0]),
            generate_avgSunny_days(county[0]),
            generate_winter_low(county[0])
            )

    else:
        return (
            generate_mhgrowth_rate("Maricopa"),
            generate_avgSunny_days("Maricopa"),
            generate_winter_low("Maricopa")
            )


@app.callback(Output("povertyRate", "children"),
    [Input("choropleth", "clickData"), Input("choropleth", "figure")])
def update_poverty_rate(choro_click, choro_figure):
    if choro_click is not None:
        county = []
        for point in choro_click["points"]:
            county.append(point["location"])
        return generate_poverty_rate(county[0])
    else:
        return generate_poverty_rate("Maricopa")

@app.callback(Output("bedroom", "figure"),
    [Input("choropleth", "clickData"), Input("choropleth", "figure"),Input("first_dropdown", "value")])
def update_house_price(choro_click, choro_figure, dd_select):
    if dd_select is None:
        dd_select = "bed1"

    if choro_click is not None:
        county = []
        for point in choro_click["points"]:
            county.append(point["location"])
        return generate_house_graph(county[0], dd_select)
    else:
        return generate_house_graph("Maricopa", dd_select)


if __name__ == '__main__':
    app.run_server()
