import dash
import dash_bootstrap_components as dbc
from dash import Output, Input, State, dcc, html
from dash.exceptions import PreventUpdate
import pandas as pd
from app import app
from apps.dbconnect import getDataFromDB  # Assuming the database connection functions are implemented here

email_input = html.Div(
    [
        dbc.Label("Email", html_for="example-email"),
        dbc.Input(type="email", id="example-email", placeholder="Enter email"),
        dbc.FormText(
            "Are you on email? You simply have to be these days",
            color="secondary",
        ),
    ],
    className="mb-3",
)

password_input = html.Div(
    [
        dbc.Label("Password", html_for="example-password"),
        dbc.Input(
            type="password",
            id="example-password",
            placeholder="Enter password",
        ),
        dbc.FormText(
            "A password stops mean people taking your stuff", color="secondary"
        ),
    ],
    className="mb-3",
)

button = html.Div(
    [
        dbc.Button("Submit", color="primary"),
    ]
)

form = dbc.Form([email_input, password_input, button])


layout = html.Div(
    [
#         # Page Header
#         html.Div(
#             [
#                 html.H2('Login Page'),
#                 html.Hr(),
#             ],
#             style={'margin-top': '15px'}  # Adjust margin to avoid overlap with navbar
#         ),

#         form,
#     ]
# )

html.Div(
    className="d-flex justify-content-center align-items-center",
    style={"height": "100vh", "background-color": "#f8f9fa"},  # Light background for aesthetics
    children=[
        dbc.Card(
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            # Left side for logo
                            dbc.Col(
                                html.Img(src="path_to_your_logo.png", style={"width": "100%", "max-width": "200px"}),
                                width=5,
                            ),
                            # Right side for form inputs
                            dbc.Col(
                                [
                                    html.H4("Login", className="text-center"),
                                    dbc.CardGroup([
                                        dbc.Label("Email", html_for="email-input"),
                                        dbc.Input(type="email", id="email-input", placeholder="Enter your email"),
                                    ]),
                                    dbc.CardGroup([
                                        dbc.Label("Password", html_for="password-input"),
                                        dbc.Input(type="password", id="password-input", placeholder="Enter your password"),
                                    ]),
                                    dbc.CardGroup([
                                        dbc.Label("Role"),
                                        dbc.RadioItems(
                                            options=[
                                                {"label": "Student", "value": "student"},
                                                {"label": "Teacher", "value": "teacher"},
                                            ],
                                            value="student",
                                            id="role-radio",
                                            inline=True,
                                        ),
                                    ]),
                                    dbc.Button("Submit", id="submit-button", color="primary"),
                                    html.Div(className="text-center mt-3",
                                             children=[html.A("Sign Up", href="/signup")])
                                ],
                                width=7,
                            ),
                        ],
                        align="center",
                    )
                ]
            ),
            style={"width": "80%", "max-width": "600px"},  # Card width settings
        )
    ]
)
    ]
)


# Run the app in debug mode
if __name__ == '__main__':
    app.run_server(debug=True)