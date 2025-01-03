import logging

import os
from flask import Flask
from flask_login import login_user, LoginManager, UserMixin, current_user

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html,  Input, Output, State

# Create the application object (stored in app variable), along with CSS stylesheets
app = dash.Dash(__name__)

# Make sure that callbacks are not activated when input elements enter the layout; config is setting quality of app
app.config.suppress_callback_exceptions = True

# Get CSS from a local folder
app.css.config.serve_locally = True

# Enables your app to run offline -- optional
app.scripts.config.serve_locally = True

# Set app title that appears in your browser tab
app.title = 'Smallville Montessori'

# These 2 lines reduce the logs on your terminal so you could debug better
# when you encounter errors in app
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

