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
from dash.dependencies import Input, Output, Event
import psycopg2
import pandas as pd
import numpy as np
import os
import plotly.plotly as py
import plotly.graph_objs as go
from datetime import datetime

print("################################################")
print("Dengue Fever Prediction System")
print("Visualization Layer: Dashboard Service")
print("################################################")
print(" ")
print(str(datetime.now())+": Initiating Dash context...")

# Initiate Dash App
app = dash.Dash()

try:
    mapbox_access_token = os.environ['MAPBOX_ACCESS_TOKEN']
except:
    print(str(datetime.now())+": Unable to get Mapbox Access Token from environment variable!")

app.layout = html.Div(children=[
    html.H1(children='Dengue Prediction System'),

    html.Div(children='''
        Live Dengue Predictions For The Next Week
    '''),

    dcc.Graph(id='live-data-map'),

    dcc.Interval(
            id='update-interval',
            interval=10*1000 # in milliseconds
    )
])

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

@app.callback(Output('live-data-map', 'figure'),events=[Event('update-interval', 'interval')])
def update_graph_live():

    # Gather the data from the PostreSQL database
    wkfrstday = datetime.now().strftime("%Y-%m-%d")
    try:
        # Connect and get
        conn = psycopg2.connect(database="denguepred", user="postgres", password="pass", host="localhost", port="5432")
        cur = conn.cursor()
        cur.execute("SELECT * FROM predictions WHERE wkfrstday = '%s';" % wkfrstday)
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

    # Set up the circles for the live map
    live_data = []
    for record in records:
        index = record[0]
        city = record[1]
        wkfrstday = record[2].strftime("%b. %d, %Y")
        avg_temp_K = record[3]
        dew_pt_temp_K = record[4]
        max_temp_K = record[5]
        min_temp_K = record[6]
        rel_hum_pct = record[7]
        avg_temp_C = record[8]
        num_cases = int(record[9])
        coords = city_coords[city]
        text = city + "<br>Predicted number of cases: " + str(num_cases)
        text += "<br><br>Weather Forecast:<br>"
        text += "Temperature: " + str(avg_temp_K-273.15) + "°C (average), " + str(max_temp_K-273.15) + "°C (max), " + str(min_temp_K-273.15) + "°C (min)<br>"
        text += "Dew Point: " + str(dew_pt_temp_K-273.15) + "°C<br>"
        text += "Relative Humidity: " + str(rel_hum_pct) + "%"

        city_data = go.Scattermapbox(
                        mode = 'markers',
                        lon = [coords["long"]],
                        lat = [coords["lat"]],
                        text = [text],
                        marker = go.Marker(
                            size = np.log10(num_cases)*10,
                            color = "rgb(255,75,75)",
                            opacity = 0.8,
                            sizemode = 'area'
                        ),
                        name = city)
        live_data.append(city_data)

    live_map_layout = go.Layout(
        title = 'Live Prediction Of Number of Dengue Cases<br>Week Starting On ' + wkfrstday,
        autosize=True,
        hovermode='closest',
        showlegend=True,
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            pitch=0,
            zoom=1,
            style='light'
        )
    )

    figure = {"data": go.Data(live_data), "layout": live_map_layout}

    return figure

print(str(datetime.now())+": Starting Dash server...")
if __name__ == '__main__':
    app.run_server(debug=False, host="0.0.0.0")
