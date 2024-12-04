import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.exceptions import PreventUpdate

from app import app

tab1_content = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Spring Break", className="card-text"),
            html.P("Please note that Spring Break will take place from April 1st to April 5th. Classes will resume on April 8th.", className="card-text"),
            html.H5("Enrollment for Next Year", className="card-text"),
            html.P("Enrollment for the 2024-2025 school year is now open! Secure your child's spot by completing the registration forms available on our website.", className="card-text"),
            html.H5("Parent Workshops", className="card-text"),
            html.P("Join us for a series of workshops focused on Montessori education and parenting strategies, starting on March 25th. Details will be sent out via email.", className="card-text"),
        ]
    ),
    className="mt-3",
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("This is tab 2!", className="card-text"),
        ]
    ),
    className="mt-3",
)

tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Announcements"),
        dbc.Tab(tab2_content, label="Schedules"),
    ]
)


# Define the layout variable instead of modifying app.layout directly
layout = html.Div(  # Wrap everything in a Div
    [
        html.Div (style={
            'background-image':"home.png",
            'background-repeat':'no-repeat',
            'background-position': 'right top',
            'background-size': '150px 1000px'
        }
        ),

        # html.Main(
        #     children=[
        #         html.Header(
        #             style={'background-color': '#003093', 'padding': '10px 20px'},
        #             children=[
        #                 html.H1('Smallville Montessori - Katipunan', style={'color': '#f1f1f1'}),
        #                 html.H3('Welcome User!', style={'color': '#f1f1f1'})
        #             ]
        #         ),
        
        # dbc.Card()
                # Introduction Section
                html.Div(
                    style={'margin-left': '15px', 'margin-top': '7px'},
                    children=[
                        html.P("In Smallville Montessori, we believe in Montessori curriculum the way Maria Montessori herself practiced her teaching."),
                        html.P(style={'font-weight': 'bold'}, children="Why choose Smallville Montessori?"),
                        html.P("Child-Centered Learning: Our Montessori approach nurtures independence, curiosity, and a passion for discovery."),
                        html.P("Inclusive Community: We celebrate every child's unique journey and learning style."),
                        html.P("Holistic Development: Focusing on academics, social skills, and emotional growth.")
                    ]
                ),

        tabs,

                # Footer
                html.Footer(
                    style={
                        'text-align': 'center',
                        'padding': '6px',
                        'background-color': '#003093',
                        'position': 'fixed',
                        'bottom': 0,
                        'width': "100%"
                    },
                    children=[
                        html.P(style={'color': '#f1f1f1'}, children="© 2024 Smallville Montessori")
                    ]
                )
            ]
        )
#     ]
# )
