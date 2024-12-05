import dash
import dash_bootstrap_components as dbc
from dash import Output, Input, State, dcc, html
from dash.exceptions import PreventUpdate
import pandas as pd
from app import app
from apps.dbconnect import getDataFromDB  # Assuming the database connection functions are implemented here

layout = html.Div(
    [
        # Page Header
        html.Div(
            [
                html.H2('User Profile'),
                html.Hr(),
            ],
            style={'margin-top': '15px'}  # Adjust margin to avoid overlap with navbar
        ),
    ]
)


# Run the app in debug mode
if __name__ == '__main__':
    app.run_server(debug=True)