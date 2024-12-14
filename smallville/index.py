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
from apps.schedule import student_sched, sched_assign, sched_edit, sched_form, sched_management
from apps.payment import payment, payment_upload
from apps.teacher import teacher_stud_list, teacher_stud_list_edit

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
        html.Div(id='page-content', className='m-2 p-2')
    ]
)

@app.callback(
    [
        Output('page-content', 'children'),
        Output('sessionlogout', 'data'),
        Output('navbar_div', 'className'),
    ],
    [
        # If the path (i.e. part after the website name;
        # in url = youtube.com/watch, path = '/watch') changes,
        # the callback is triggered
        Input('url', 'pathname')
    ],
    [
        State('sessionlogout', 'data'),
        State('currentuserid', 'data'),
    ]
)


def displaypage (pathname, sessionlogout, userid):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'url':
            if userid < 0: # if logged out
                if pathname == '/' or pathname == '/login':
                    returnlayout = login.layout
                elif pathname == '/signup':
                    returnlayout = signup.layout
                else:
                    returnlayout = '404: request not found before login'
           
            else:    
                if pathname == '/logout':
                    returnlayout = login.layout
                    sessionlogout = True
                   
                elif pathname == '/home':
                    #return student_profile.layout  # Assuming you have this layout defined
                    return home.layout, sessionlogout, ''
               
                elif pathname == '/student/student_profile':
                    #return student_profile.layout  # Assuming you have this layout defined
                    return student_profile.layout, sessionlogout, ''
       
                elif pathname == '/student/student_profile_edit':
                    return student_profile_edit.layout, sessionlogout, ''
       
                elif pathname == '/student/student_sched':
                    return student_sched.layout, sessionlogout, ''

                elif pathname == '/student/payment':
                    return payment.layout, sessionlogout, ''

                elif pathname == '/student/payment_upload':
                    return payment_upload.layout, sessionlogout, ''
       
                elif pathname == '/student/sched_management':
                    return sched_management.layout, sessionlogout, ''
       
                elif pathname == '/student/sched_form':
                    return sched_form.layout, sessionlogout, ''
       
                elif pathname == '/student/sched_edit':
                    return sched_edit.layout, sessionlogout, ''
                
                elif pathname == '/teacher/teacher_stud_list':
                    return teacher_stud_list.layout, sessionlogout, ''
                
                elif pathname == '/teacher/teacher_stud_list_edit':
                    return teacher_stud_list_edit, sessionlogout, ''

                else:
                    returnlayout = '404: request not found after login'
                   
            # decide sessionlogout value
            logout_conditions = [
                pathname in ['/', '/logout'],
                userid == -1,
                not userid
            ]
            sessionlogout = any(logout_conditions)
           
            # hide navbar if logged-out; else, set class/style to default
            navbar_classname = 'd-none' if sessionlogout else ''
       
        else:
            raise PreventUpdate
   
        return [returnlayout, sessionlogout, navbar_classname]
    else:
        raise PreventUpdate

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8050/', new=0, autoraise=True)
    app.run_server(debug=True)  # Set debug=True for development
