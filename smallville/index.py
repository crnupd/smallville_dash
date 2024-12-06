import webbrowser
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import os
from flask import Flask
from flask_login import login_user, LoginManager, UserMixin, current_user

# Importing your app variable from app.py so we can use it
from app import app, server
from apps import commonmodules as cm  # Assuming you have a common module for navbar etc.
from apps import home  # Import the home layout
from apps.student import student_profile, student_profile_edit
from apps.schedule import student_sched, sched_edit, sched_form, sched_management
from apps.payment import payment, payment_upload
from apps import login
from apps import profile

# Updating the Flask Server configuration with Secret Key to encrypt the user session cookie
server.config.update(SECRET_KEY=os.getenv("SECRET_KEY"))

login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = "/login"

class User(UserMixin):
    # User data model. It has to have at least self.id as a minimum
    def __init__(self, username, role):
        self.id = username
        self.role = role 

VALID_USERNAME_PASSWORD = {"test": "test", "hello": "world"}

VALID_USERS = {
    "teacher": User("teacher", "teacher"),
    "parent": User("parent", "parent")
}


@login_manager.user_loader
def load_user(username):
    """This function loads the user by user id. Typically this looks up the user from a user database.
    We won't be registering or looking up users in this example, since we'll just login using LDAP server.
    So we'll simply return a User object with the passed in username.
    """
    return User(username)

#to check if logged in:
# is_logged_in = False

# Define the main layout of the app
app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=True),  # URL location for navigation
        cm.navbar,  # Assuming you have a navbar defined in commonmodules
        # Page Content
        html.Div(id='page_content', className='m-2 p-2'),   
    ]
)

@app.callback(
    Output("output_state", "children"),
    Input("login-button", "n_clicks"),
    State("username", "value"),
    State("password", "value"),
    prevent_initial_call=True,
)
def login_button_click(n_clicks, username, password):
    # global is_logged_in  # Access the global variable
    if n_clicks > 0:
        if username not in VALID_USERNAME_PASSWORD:
            return "Invalid username"
        if VALID_USERNAME_PASSWORD[username] == password:
            user = User(username, "user")  # Create a user instance with role
            login_user(user)
            # is_logged_in = True
            return "Login Successful"
        return "Incorrect  password"


@app.callback(
    Output('page_content', 'children'),
    Input('url', 'pathname')
)

def displaypage(pathname):
    ctx = dash.callback_context
    
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]   
    else:
        raise PreventUpdate

    if eventid == 'url':
        if pathname == '/' or pathname == '/home':
            return home.layout  # Return the layout from home.py
        
        elif pathname == '/login':
            return login.layout

        # if not is_logged_in:
        #     return html.Div("Please sign in to access this page.")  # Redirect to login prompt
        
        elif pathname == '/student/student_profile':
            return student_profile.layout  # Assuming you have this layout defined
        
        elif pathname == '/student/student_profile_edit':
            return student_profile_edit.layout
        
        elif pathname == '/student/student_sched':
            return student_sched.layout

        elif pathname == '/student/payment':
            return payment.layout

        elif pathname == '/student/payment_upload':
            return payment_upload.layout
        
        elif pathname == '/student/sched_management':
            return sched_management.layout
        
        elif pathname == '/student/sched_form':
            return sched_form.layout
        
        elif pathname == '/student/sched_edit':
            return sched_edit.layout
        
        elif pathname == '/profile':
            return profile.layout
        
        else:
            return '404 Error: Page Not Found'  # Handle unknown routes
    
    raise PreventUpdate  # Prevent updates if no valid event is triggered


# Callback for tab functionality in home layout
# @app.callback(
#     Output('announcements-content', 'style'),
#     Output('schedules-content', 'style'),
#     Output('grade-content', 'style'),
#     Input('announcements-tab', 'n_clicks'),
#     Input('schedules-tab', 'n_clicks'),
#     Input('grade-tab', 'n_clicks')
# )
# def update_tab(announcements_clicks, schedules_clicks, grade_clicks):
#     ctx = dash.callback_context

#     if not ctx.triggered:
#         return {'display': 'block'}, {'display': 'none'}, {'display': 'none'}

#     button_id = ctx.triggered[0]['prop_id'].split('.')[0]

#     if button_id == "announcements-tab":
#         return {'display': 'block'}, {'display': 'none'}, {'display': 'none'}
#     elif button_id == "schedules-tab":
#         return {'display': 'none'}, {'display': 'block'}, {'display': 'none'}
#     elif button_id == "grade-tab":
#         return {'display': 'none'}, {'display': 'none'}, {'display': 'block'}

#     return {'display': 'block'}, {'display': 'none'}, {'display': 'none'}

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8050/', new=0, autoraise=True)
    app.run_server(debug=True)  # Set debug=True for development