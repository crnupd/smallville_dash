# Usual Dash dependencies
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.exceptions import PreventUpdate

# Let us import the app object in case we need to define callbacks here
from app import app

# Define a default style for nav links
navlink_style = {'margin-bottom': '1em'}

# Create a vertical navbar using dbc.Nav
navbar = html.Div(
    [
         # Add an image at the top of the navbar
        html.Img(
            src=app.get_asset_url('logo.png'),  # Replace 'logo.png' with your actual image filename
            style={
                'width': '100%',  # Set width to 100%
                'height': 'auto',  # Set height to auto for responsive scaling
                'margin-bottom': '10px'  # Add some margin below the image
            }
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/home", active="exact", style=navlink_style, className="nav-link"),
                dbc.NavLink("Student Registration", href="/student/student_profile", active="exact", style=navlink_style, className="nav-link"),
                dbc.NavLink("Class Schedule", href="/student/student_sched", active="exact", style=navlink_style, className="nav-link"),
                dbc.NavLink("Payment", href="/student/payment", active="exact", style=navlink_style, className="nav-link"),
            ],
            vertical=True,  # Set vertical layout for nav links
            pills=True,     # Optional: adds pill styling to links
        )
    ],
    style={
        "margin": 0,
        "padding": "20px 10px",
        "width": "15%",
        "background-color": "#f1f1f1",
        "position": "fixed",
        "height": "100%",
        "overflow": "auto",
    }
)