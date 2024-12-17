import hashlib

import dash
import dash_bootstrap_components as dbc
from dash import callback_context, dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
from app import app
from apps import dbconnect as db


layout = html.Div(
    className="d-flex justify-content-center align-items-center",
    style={"height": "100vh", "background-color": "#f0F8FF"},  
    children=[
        dbc.Row(
            [
                # Left side for logo/image
                dbc.Col(
                    html.Img(src="/assets/login.png", style={"width": "90%"}),
                    width=7,
                    style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'padding-right': '20px'}  # Center the image vertically
                ),
                # Right side for login details
                dbc.Col(
                    [
                        html.H3("Login", className="text-center", style={'margin-top': '20px'}),
                        dbc.Alert('Username or password is incorrect.', color="danger", id='login_alert', is_open=False),
                        dbc.CardGroup([
                            dbc.Label("Username", width=5, html_for="uname-input", id="uname-box"),
                            dbc.Input(type="text", id="login_username", placeholder="Enter your username"),
                        ]),
                        dbc.CardGroup([
                            dbc.Label("Password", width=5, html_for="password-input", id="pwd-box", style={'margin-top': '10px'}),
                            dbc.Input(type="password", id="login_password", placeholder="Enter your password"),
                        ]),
                        dbc.Button("Login", color="primary", id='login_loginbtn', style={'margin-top': '10px'}),
                        html.A('Create an account', href='/signup', className="text-center", style={'display': 'block', 'margin-top': '15px'})
                    ],
                    width=5,
                    align='center',
                    style={'padding-right': '20px'}  # Add some padding to the right side
                ),
            ],
            align="center",
            className="g-0"  # Remove gutter spacing between columns
        )
    ]
)


@app.callback(
    [
        Output('login_alert', 'is_open'),
        Output('currentuserid', 'data'),
    ],
    [
        Input('login_loginbtn', 'n_clicks'), # begin login query via button click
        Input('sessionlogout', 'modified_timestamp'), # reset session userid to -1 if logged out
    ],
    [
        State('login_username', 'value'),
        State('login_password', 'value'),  
        State('sessionlogout', 'data'),
        State('currentuserid', 'data'),
        State('url', 'pathname'),
    ]
)
def loginprocess(loginbtn, sessionlogout_time,
                 
                 username, password,
                 sessionlogout, currentuserid,
                 pathname):
   
    ctx = callback_context
   
    if ctx.triggered:
        openalert = False
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    else:
        raise PreventUpdate
   
   
    if eventid == 'login_loginbtn': # trigger for login process
        if loginbtn and username and password:
            sql = """SELECT user_id
            FROM users
            WHERE
                user_name = %s AND
                user_password = %s AND
                NOT user_delete_ind"""
           
            # we match the encrypted input to the encrypted password in the db
            encrypt_string = lambda string: hashlib.sha256(string.encode('utf-8')).hexdigest()
           
            values = [username, encrypt_string(password)]
            cols = ['userid']
            df = db.getDataFromDB(sql, values, cols)
           
            if df.shape[0]: # if query returns rows
                currentuserid = df['userid'][0]
            else:
                currentuserid = -1
                openalert = True
               
    elif eventid == 'sessionlogout' and pathname == '/logout': # reset the userid if logged out
        currentuserid = -1
       
    else:
        raise PreventUpdate
   
    return [openalert, currentuserid]


@app.callback(
    [
        Output('url', 'pathname'),
    ],
    [
        Input('currentuserid', 'modified_timestamp'),
    ],
    [
        State('currentuserid', 'data'),
    ]
)
def routelogin(logintime, userid):
    ctx = callback_context
    if ctx.triggered:
        if userid > 0:
            url = '/home'
        else:
            url = '/'
    else:
        raise PreventUpdate
    return [url]