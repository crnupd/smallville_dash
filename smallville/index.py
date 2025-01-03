import webbrowser
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from apps import commonmodules as cm  
from apps import home, login, signup, admin  
from apps.student import student_profile, student_profile_edit
from apps.schedule import student_sched, sched_assign, sched_edit, sched_form
from apps.payment import payment, payment_upload
from apps.teacher import teacher_stud_list_edit
from constants import ADMIN_USER_ID

if __name__ == '__main__':

    app.layout = html.Div(
        [
            dcc.Location(id='url', refresh=True),  
        
            dcc.Store(id='sessionlogout', data=True, storage_type='session'),

            dcc.Store(id='currentuserid', data=-1, storage_type='session'),
        
            dcc.Store(id='currentrole', data=-1, storage_type='session'),

            html.Div(cm.navbar, id='navbar_div'),  

            html.Div(style={'margin-top': '70px'},id='page-content', className='m-2 p-2')
        ]
    )

    @app.callback(
        [
            Output('page-content', 'children'),
            Output('sessionlogout', 'data'),
            Output('navbar_div', 'className'),
        ],
        [
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
                        returnlayout = login.layout, True, ''
                    
                    elif pathname == '/home':
                        returnlayout = home.layout
                    
                    elif pathname == '/admin':
                        if userid == ADMIN_USER_ID: 
                            returnlayout = admin.layout
                        else:
                            returnlayout = '403: Access Denied - Admins Only'
                
                    elif pathname == '/student/student_profile':
                        returnlayout = student_profile.layout
        
                    elif pathname == '/student/student_profile_edit':
                        returnlayout = student_profile_edit.layout
        
                    elif pathname == '/student/student_sched':
                        returnlayout = student_sched.layout

                    elif pathname == '/student/payment':
                        returnlayout = payment.layout

                    elif pathname == '/student/payment_upload':
                        returnlayout = payment_upload.layout
        
                    elif pathname == '/student/sched_assign':
                        returnlayout = sched_assign.layout
        
                    elif pathname == '/student/sched_form':
                        returnlayout = sched_form.layout 
        
                    elif pathname == '/student/sched_edit':
                        returnlayout = sched_edit.layout
                    
                    elif pathname == '/teacher/teacher_stud_list_edit':
                        returnlayout = teacher_stud_list_edit.layout

                    else:
                        returnlayout = '404: request not found after login'
                    
                # decide sessionlogout value
                logout_conditions = [
                    pathname in ['/', '/logout'],
                    userid == -1,
                    not userid
                ]
                sessionlogout = any(logout_conditions)
                navbar_classname = 'd-none' if sessionlogout else ''
        
            else:
                raise PreventUpdate
            
            return [returnlayout, sessionlogout, navbar_classname]
        else:
            raise PreventUpdate

    app.run_server(debug=False) 
