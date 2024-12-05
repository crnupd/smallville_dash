import webbrowser
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

# Importing your app variable from app.py so we can use it
from app import app
from apps import commonmodules as cm  # Assuming you have a common module for navbar etc.
from apps import home  # Import the home layout
from apps.student import student_profile, student_profile_edit
from apps.schedule import student_sched
from apps.payment import payment, payment_upload
from apps.teacher import teacher_sched
from apps import login
from apps import profile

# Define the main layout of the app
app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=True),  # URL location for navigation
        cm.navbar,  # Assuming you have a navbar defined in commonmodules

        # Page Content
        html.Div(id='page_content', className='m-2 p-2')
    ]
)

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
        
        elif pathname == '/teacher/teacher_sched':
            return teacher_sched.layout
        
        elif pathname == '/login':
            return login.layout
        
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