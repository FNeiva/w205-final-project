# -*- coding: utf-8 -*-

##########################################################################################
# Dengue Fever Prediction System
# W205 Summer 2017 Final Project
# Felipe Campos, Frank Shannon, Josh Wilson and Matthew Holmes
##########################################################################################
# Visualization Layer: Dashboard service
#
# This is the main script in the visualization layer. This script builds the
# visualizations and starts Dash, who serves them on a Web Server.
#
##########################################################################################

import dash
import dash_core_components as dcc
import dash_html_components as html
import psycopg2
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go

print("################################################")
print("Dengue Fever Prediction System")
print("Visualization Layer: Dashboard Service")
print("################################################")
print(" ")
print(str(datetime.now())+": Initiating Dash context...")

# Initiate Dash App
app = dash.Dash()

# Gather the data from the PostreSQL database
wkfrstday = datetime.now().strftime("%Y-%m-%d")
try:
    # Connect and get
    conn = psycopg2.connect(database="denguepred", user="postgres", password="pass", host="localhost", port="5432")
    cur = conn.cursor()
    cur.execute("SELECT * FROM predictions WHERE wkfrstday=%s;",wkfrstday)
    records = cur.fetchall()
    conn.commit()
    conn.close()
except:
    print(str(datetime.now())+": Unable to get dengue cases update from database table with predictions!")

# City coordinates for plotting
city_coords = {"San Juan":{"lat":18.4374,"long":-66.0045},
               "Iquitos":{"lat":-3.7847,"long":-73.3086},
               "Rio de Janeiro":{"lat":-22.9111,"long":-43.1649},
               "Brasilia":{"lat":-15.8697,"long":-47.9172},
               "Sao Paulo":{"lat":-23.6273,"long":-46.6566},
               "Salvador":{"lat":-12.9111,"long":-38.3312} }
colors = { "High": "rgb(255,75,75)",
           "Medium": "rgb(255,208,75)",
           "Low": "rgb(178,255,75)"}

# Set up the circles for the live map
live_data = []
for record in records:
    city = record[0]
    wkfrstday = record[1]
    avg_temp_K = record[2]
    dew_pt_temp_K = record[3]
    max_temp_K = record[4]
    min_temp_K = record[5]
    rel_hum_pct = record[6]
    avg_temp_C = record[7]
    num_cases = record[8]
    coords = city_coords[city]
    text = city + "<br>Predicted number of cases: " + num_cases.astype(str)
    text += "<br><br>Weather Forecast:<br>"
    text += "Temperature: " + avg_temp_K-273.15 + "°C (average), " + max_temp_K-273.15 + "°C (max), " + min_temp_K-273.15 + "°C (min)<br>"
    text += "Dew Point: " + dew_pt_temp_K-273.15 + "°C<br>"
    text += "Relative Humidity: " + rel_hum_pct + "%"
    if num_cases > 300:
        bubble_color = "High"
    elif num_cases < 300 and num_cases > 80:
        bubble_color = "Medium"
    else:
        bubble_color = "Low"
    city_data = dict(
        type = 'scattergeo',
        locationmode = 'ISO-3',
        lon = coords["long"],
        lat = coords["lat"],
        text = text,
        marker = dict(
            size = num_cases,
            color = colors[bubble_color],
            line = dict(width=0.5, color='rgb(40,40,40)'),
            sizemode = 'area'
        ),
        name = city)
    live_data.append(city_data)

layout = dict(
        title = 'Live Prediction Of Number of Dengue Cases<br>Week Starting On ' + wkfrstday,
        showlegend = True,
        geo = dict(
            scope='americas',
            projection=dict( type='mercator' ),
            showland = True,
            landcolor = 'rgb(217, 217, 217)',
            subunitwidth=1,
            countrywidth=1,
            subunitcolor="rgb(255, 255, 255)",
            countrycolor="rgb(255, 255, 255)"
        ),
    )

app.layout = html.Div(children=[
    html.H1(children='Dengue Prediction System'),

    html.Div(children='''
        Live Dengue Predictions For The Next Week
    '''),

    dcc.Graph(
        id='live-data',
        figure={
            'data': live_data,
            'layout': layout
        }
    )
])

print(str(datetime.now())+": Starting Dash server...")
if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0")
