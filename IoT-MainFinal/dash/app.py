from operator import index
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input
import dash_daq as daq
import plotly.express as px
import ast

# data pre-processing-------------------------------------------------------------------------------------------------------------------------

data = pd.read_csv(
    "E:\VS_codes\IoT-MainFinal/IOT-yashwanth/dataBase/room01DB.csv"
)
masterData = pd.read_csv(
    "E:\VS_codes\IoT-MainFinal/IOT-yashwanth/dataBase/masteDB.csv"
)


# web layout ---------------------------------------------------------------------------------------------------------------------------------
external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
    {
        "href": "https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css",
        "rel": "stylesheet",
        "integrity": "sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC",
        "crossorigin": "anonymous",
    },
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "Smart Solar PV Panel Monitoring"

app.layout = html.Div(
    [
        dcc.Interval(
            id="my-interval",
            disabled=False,
            interval=1 * 1000,
            n_intervals=0,
            max_intervals=-1,
        ),
        html.Div(
            children=[
                html.P(children="⚓", className="header-emoji"),
                html.H1(
                    children="Smart Solar PV Panel Monitoring", className="header-title"
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(
                            html.P(id="temp-act", children=["Temperature Actuator:"]),
                            className="card right",
                        ),
                        html.Div(
                            html.P(id="moist-act", children=["Dust Actuator:"]),
                            className="card right",
                        ),
                       
                    ],
                    className="col-md-3 left-box",
                ),

                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.Div(
                                    daq.Gauge(
                                        id="humidity-guage",
                                        label="Relative Room Humidity",
                                        value=60,
                                        max=100,
                                        min=0,
                                        units="%",
                                        showCurrentValue=True,
                                        className="dark-theme-control",
                                        color="#599900",
                                    ),
                                    className="col",
                                ),
                                html.Div(
                                    daq.Gauge(
                                        color={
                                            "gradient": True,
                                            "ranges": {
                                                "green": [0, 6],
                                                "yellow": [6, 8],
                                                "red": [8, 10],
                                            },
                                        },
                                        label="Dust",
                                        max=10,
                                        min=0,
                                        id="dust-guage",
                                        showCurrentValue=True,
                                        value=4,
                                        units="%",
                                    ),
                                    className="col",
                                ),
                            ],
                            className="row",
                        ),
                        html.Div(
                            daq.Thermometer(
                                id="my-thermometer",
                                label="Room Temperature",
                                value=22,
                                min=15,
                                max=35,
                                showCurrentValue=True,
                                units="°C",
                                style={"margin-bottom": "5%"},
                                className="temp-widget",
                                color="#599900",
                            )
                        ),
                    ],
                    className="col",
                ),
                html.Div(
                    children=[
                        html.H2("Solar Panel",style={'color': 'white', 'fontSize': 40}),
                        html.Div(
                            children=[
                                html.H6("Voltage in V",style={'color': 'white', 'fontSize': 25}),
                                daq.LEDDisplay(
                                    id="my-Voltage",
                                    value="0.00",
                                    backgroundColor="#000000",
                                    color="#FF5E5E",
                                ),
                                html.H6("\n\n"),
                            ],
                            className="row",
                        ),
                        html.Div(
                            children=[
                                html.H6("Current in Amps",style={'color': 'white', 'fontSize': 25}),
                                daq.LEDDisplay(
                                    id="my-Current",
                                    value="0.00",
                                    backgroundColor="#000000",
                                    color="#FF5E5E",
                                ),
                            ],
                            className="row",
                        ),
                    ],
                    className="col-md-4 right-box",
                ),
            ],
            className="row",
        ),
    ]
)

# ------------------------------------------------------------------------------------------------------------------
# Temperature Actuator

@app.callback(Output("temp-act", "children"), Input("my-interval", "n_intervals"))
def update_humidity_act_card(n_intervals):

    data = pd.read_csv(
        "E:\VS_codes\IoT-MainFinal/IOT-yashwanth/dataBase/room01DB.csv"
    )
    sensorID = "ARA0100"
    temp_mask = pd.notna(data[sensorID])

    return [html.Span("Temperature Actuator: " + data[sensorID][temp_mask].iloc[-1])]


# ------------------------------------------------------------------------------------------------------------------
# Dust Actuator


@app.callback(Output("moist-act", "children"), Input("my-interval", "n_intervals"))
def update_temp_act_card(n_intervals):

    data = pd.read_csv(
        "E:\VS_codes\IoT-MainFinal/IOT-yashwanth/dataBase/room01DB.csv"
    )
    sensorID = "ADA0100"
    temp_mask = pd.notna(data[sensorID])

    return [html.Span("Dust Actuator: " + data[sensorID][temp_mask].iloc[-1])]


# ------------------------------------------------------------------------------------------------------------------
# Test Bench Equipment


@app.callback(
    Output("my-Voltage", component_property="value"),
    Input("my-interval", "n_intervals"),
)
def update_voltage(n_intervals):
    sensorID = "ETB0100"
    data = pd.read_csv(
        "E:\VS_codes\IoT-MainFinal/IOT-yashwanth/dataBase/room01DB.csv"
    )

    tb_mask = pd.notna(data[sensorID])
    print("//////", tb_mask)
    print("*******", data[sensorID][tb_mask].iloc[-1])
    test_bench_dict = ast.literal_eval(data[sensorID][tb_mask].iloc[-1])
    print("*******", test_bench_dict["ValueVolt"])
    return str(round(test_bench_dict["ValueVolt"], 2))


@app.callback(
    Output("my-Current", component_property="value"),
    Input("my-interval", "n_intervals"),
)
def update_current(n_intervals):
    sensorID = "ETB0100"
    data = pd.read_csv(
        "E:\VS_codes\IoT-MainFinal/IOT-yashwanth/dataBase/room01DB.csv"
    )

    tb_mask = pd.notna(data[sensorID])
    print("//////", tb_mask)
    # print("*******", data[sensorID][tb_mask].iloc[-1])
    test_bench_dict = ast.literal_eval(data[sensorID][tb_mask].iloc[-1])
    print("*******", test_bench_dict["ValueCurr"])
    return str(round(test_bench_dict["ValueCurr"], 2))

# ------------------------------------------------------------------------------------------------------------------
# Temperature Sensor


@app.callback(Output("my-thermometer", "value"), [Input("my-interval", "n_intervals")])
def update_thermometer(value):

    data = pd.read_csv(
        "E:\VS_codes\IoT-MainFinal/IOT-yashwanth/dataBase/room01DB.csv"
    )
    temp_mask = pd.notna(data["SRT0100"])

    return data["SRT0100"][temp_mask].iloc[-1]


# ------------------------------------------------------------------------------------------------------------------
# Humidity Sensor


@app.callback(Output("humidity-guage", "value"), [Input("my-interval", "n_intervals")])
def update_gauge(value):

    data = pd.read_csv(
        "E:\VS_codes\IoT-MainFinal/IOT-yashwanth/dataBase/room01DB.csv"
    )
    humidity_mask = pd.notna(data["SHS0100"])

    return data["SHS0100"][humidity_mask].iloc[-1]

# ------------------------------------------------------------------------------------------------------------------
# Humidity Sensor


@app.callback(Output("dust-guage", "value"), [Input("my-interval", "n_intervals")])
def update_gauge(value):

    data = pd.read_csv(
        "E:\VS_codes\IoT-MainFinal/IOT-yashwanth/dataBase/room01DB.csv"
    )
    dust_mask = pd.notna(data["SDS0100"])

    return data["SDS0100"][dust_mask].iloc[-1]



if __name__ == "__main__":
    app.run_server(debug=False, port=5055)
