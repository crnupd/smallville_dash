import hashlib

import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from apps import dbconnect as db

layout = html.Div(
    className="d-flex justify-content-center align-items-center",
    style={"height": "100vh", "background-color": "#f0F8FF"},  
    children=[
        dbc.Row(
            [
                # Left side for signup details
                dbc.Col(
                    [
                        html.H3('Fill up the details to sign up', className="text-center"),
                        dbc.Alert('Please supply details.', color="danger", id='signup_alert', is_open=False),
                        dbc.Row(
                            [
                                dbc.Label("Username", width=5),
                                dbc.Col(
                                    dbc.Input(type="text", id="signup_username", placeholder="Enter a username"),
                                    width=6,
                                ),
                            ],
                            className="mb-3",
                            style={'margin-top': '30px'}
                        ),
                        dbc.Row(
                            [
                                dbc.Label("Password", width=5),
                                dbc.Col(
                                    dbc.Input(type="password", id="signup_password", placeholder="Enter a password"),
                                    width=6,
                                ),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Label("Confirm Password", width=5),
                                dbc.Col(
                                    dbc.Input(type="password", id="signup_passwordconf", placeholder="Re-type the password"),
                                    width=6,
                                ),
                            ],
                            className="mb-3",
                        ),
                        dbc.Button('Sign up', color="primary", id='singup_signupbtn'),
                        dbc.Modal(
                            [
                                dbc.ModalHeader(dbc.ModalTitle("User Saved")),
                                dbc.ModalBody("User has been saved", id='signup_confirmation'),
                                dbc.ModalFooter(
                                    dbc.Button("Okay", href=f'/login')
                                ),
                            ],
                            id="signup_modal",
                            is_open=False,
                        )
                    ],
                    width=6,  # Set width for the signup form column
                    align='center',
                ),
                # Right side for logo/image
                dbc.Col(
                    html.Img(src="/assets/signup.png", style={"width": "90%"}),
                    width=6,  # Set width for the image column
                    style={'padding-left': '20px'}  # Remove padding to ensure full use of column space
                ),
            ],
            align="center",
            className="g-0"  # Remove gutter spacing between columns
        )
    ]
)


# disable the signup button if passwords do not match
@app.callback(
    [
        Output('singup_signupbtn', 'disabled'),
    ],
    [
        Input('signup_password', 'value'),
        Input('signup_passwordconf', 'value'),
    ]
)
def deactivatesignup(password, passwordconf):
    
    # enable button if password exists and passwordconf exists 
    #  and password = passwordconf
    enablebtn = password and passwordconf and password == passwordconf

    return [not enablebtn]


# To save the user
@app.callback(
    [
        Output('signup_alert', 'is_open'),
        Output('signup_modal', 'is_open')   
    ],
    [
        Input('singup_signupbtn', 'n_clicks')
    ],
    [
        State('signup_username', 'value'),
        State('signup_password', 'value')
    ]
)
def saveuser(signup_sginbtn, username, password):
    openalert = openmodal = False
    if signup_sginbtn:
        if username and password:
            sql = """INSERT INTO users (user_name, user_password)
            VALUES (%s, %s)"""  
            
            # This lambda fcn encrypts the password before saving it
            # for security purposes, not even database admins should see
            # user passwords 
            encrypt_string = lambda string: hashlib.sha256(string.encode('utf-8')).hexdigest()  
            
            values = [username, encrypt_string(password)]
            db.modifyDB(sql, values)
            
            openmodal = True
        else:
            openalert = True
    else:
        raise PreventUpdate

    return [openalert, openmodal]