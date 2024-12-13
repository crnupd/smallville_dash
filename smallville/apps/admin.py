import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.exceptions import PreventUpdate

from app import app


# Define the main layout variable
layout = html.Div(  # Wrap everything in a single Div
    [
        # Header section with image and register button
        html.Div(style={'margin-top': '70px'},
            children=[
                html.H2("Admin Dashboard"),
                html.P("Welcome to the admin dashboard!"),
            ]
        ),
    ]
)

