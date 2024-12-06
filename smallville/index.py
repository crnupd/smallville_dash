import webbrowser
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

# Importing your app variable from app.py so we can use it
from app import app
from apps import commonmodules as cm  # Assuming you have a common module for navbar etc.
from apps import home, login, signup  # Import the home layout
from apps.student import student_profile, student_profile_edit
from apps.schedule import student_sched, sched_edit, sched_form, sched_management, sched_assign
from apps.payment import payment, payment_upload



# Define the main layout of the app
app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=True),  # URL location for navigation

        # LOGIN DATA
        # 1) logout indicator, storage_type='session' means that data will be retained
        #  until browser/tab is closed (vs clearing data upon refresh)
        dcc.Store(id='sessionlogout', data=True, storage_type='session'),
        
        # 2) current_user_id -- stores user_id
        dcc.Store(id='currentuserid', data=-1, storage_type='session'),
        
        # 3) currentrole -- stores the role
        # we will not use them but if you have roles, you can use it
        dcc.Store(id='currentrole', data=-1, storage_type='session'),

        html.Div(cm.navbar, id='navbar_div'),  

        # Page Content
        html.Div(id='page_content', className='m-2 p-2'),   
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
        
        elif pathname == '/login':
            return login.layout
        
        elif pathname == '/signup':
            return signup.layout

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
        
        elif pathname == '/student/sched_assign':
            return sched_assign.layout
        
        else:
            return '404 Error: Page Not Found'  # Handle unknown routes
    
    raise PreventUpdate  # Prevent updates if no valid event is triggered


if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8050/', new=0, autoraise=True)
    app.run_server(debug=True)  # Set debug=True for development