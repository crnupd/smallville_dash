# Usual Dash dependencies
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.exceptions import PreventUpdate

# Let us import the app object in case we need to define callbacks here
from app import app

# Define a default style for nav links
navlink_style = {'margin-left': '1em', 'color': '#000'}  # Adjust margin and color as needed

HEADER_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "right": 0,
    "height": '70px',
    "padding": "10px",
    "z-index": '1000',
}

# Create a horizontal navbar using dbc.Navbar
navbar = dbc.Navbar(
    [
        # Add an image at the top of the navbar
        html.Img(
            src=app.get_asset_url('logo.png'),  # Replace 'logo.png' with your actual image filename
            style={
                'height': '50px',  # Set height for uniformity
                'margin-right': '10px'  # Add some margin to the right of the image
            }
        ),
        dbc.NavbarBrand("Smallville Montessori", href="/home"),  # Brand name with link

        dbc.Nav(
            [
                dbc.NavLink("Home", href="/home", active="exact", style=navlink_style),
                dbc.NavLink("Student Registration", href="/student/student_profile", active="exact", style=navlink_style),
                dbc.NavLink("Class Assignment", href="/student/student_sched", active="exact", style=navlink_style),
                dbc.NavLink("Payment", href="/student/payment", active="exact", style=navlink_style),
                dbc.NavLink("Sign Out", href="/logout", active="exact", style=navlink_style),
                dbc.NavLink("Admin", href="/admin", active="exact", style=navlink_style),
            ],
            className="ml-auto",  # Aligns nav links to the right
            pills=True,  # Optional: adds pill styling to links
        )
    ],
    color="light",  # Background color of the navbar
    dark=False,     # Set to True for dark mode styling,
    style=HEADER_STYLE,  # Padding for the navbar 
)

# Example layout using the navbar (this would be part of your main layout)
layout = html.Div(
    [
        navbar,  # Include the navbar at the top of your layout
        html.Div(
            style={'margin-top': '70px'},  # Adjust margin to avoid overlap with navbar
            children=[
                html.H2('Students'),
                html.Hr(),
                # Other content goes here...
            ]
        )
    ]
)
