from urllib.parse import urlparse, parse_qs

import dash
import dash_bootstrap_components as dbc
from dash import Output, Input, State, dcc, html
from dash.exceptions import PreventUpdate

from app import app
from apps.dbconnect import getDataFromDB, modifyDB

layout = html.Div(
    [
        # Page Header
        html.Div(
            [
                html.H2('Payment Page'),
                html.Hr(),
            ],
            style={'margin-top': '15px'}  # Adjust margin to avoid overlap with navbar
        ),

        dcc.Store(id='sched_id', storage_type='memory', data=0),
        
        dbc.Alert(id='sched_alert', is_open=False), # For feedback purposes
        dbc.Form(
            [
                dbc.Row(
                    [
                        dbc.Label("Grade Level", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text', 
                                id='sched_grade_level',
                                placeholder="Grade Level"
                            ),
                            width=5
                        )
                    ],
                    className='mb-3'
                ),
                dbc.Row(
                    [
                        dbc.Label("Subject", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text', 
                                id='sched_subject',
                                placeholder="Subject"
                            ),
                            width=5
                        )
                    ],
                    className='mb-3'
                ),
                dbc.Row(
                    [
                        dbc.Label("Teacher", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text', 
                                id='sched_teacher',
                                placeholder="Teacher"
                            ),
                            width=5
                        )
                    ],
                    className='mb-3'
                ),
                dbc.Row(
                    [
                        dbc.Label("Schedule", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text', 
                                id='sched_schedule',
                                placeholder="Schedule"
                            ),
                            width=5
                        )
                    ],
                    className='mb-3'
                ),
            ]
        ),
        html.Div(
            [
                dbc.Checklist(
                    id='sched_delete',
                    style={'margin-top':'10px'},
                    options= [dict(value=1, label="Mark as Deleted")],
                    value=[] 
                )
            ], 
            id='sched_deletediv'
                ),
        dbc.Button(
            'Submit',
            id='sched_submit',
            n_clicks=0, # Initialize number of clicks
            style={'margin-top':'20px'}
            ),
        
        dbc.Modal( # Modal = dialog box; feedback for successful saving.
            [
                dbc.ModalHeader(
                    html.H4('Save Success!')
                ),
                dbc.ModalBody(
                    'Schedule successfully updated.'
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Proceed",
                        href='/student/sched_management' # Clicking this would lead to a change of pages
                    )
                )
            ],
            centered=True,
            id='sched2_successmodal',
            backdrop='static' # Dialog box does not go away if you click at the background
        )
    ]
)
    
@app.callback(
    [
        Output('sched_id', 'data'),
        Output('sched_deletediv', 'className')
    ],
    [
        Input('url', 'pathname'),
    ],
    [
        State('url', 'search'),
    ]
)
def sched_editprofile(pathname, urlsearch):
    if pathname == '/student/sched_edit':
        parsed = urlparse(urlsearch)
        create_mode = parse_qs(parsed.query)['mode'][0]
        
        # Determine movie id and delete div class based on the mode
        if create_mode == 'add':
            id = 0
            deletediv = 'd-none'
        else:
            id = int(parse_qs(parsed.query)['id'][0])
            deletediv = ''
        
        # Return movie ID and delete div class (no genre options here)
        return [id, deletediv]
    else:
        raise PreventUpdate

       
@app.callback(
    [
        # dbc.Alert Properties
        Output('sched_alert', 'color'),
        Output('sched_alert', 'children'),
        Output('sched_alert', 'is_open'),
        # dbc.Modal Properties
        Output('sched2_successmodal', 'is_open')
    ],
    [
        # For buttons, the property n_clicks 
        Input('sched_submit', 'n_clicks')
    ],
    [
        # The values of the fields are States 
        # They are required in this process but they 
        # do not trigger this callback
        State('sched_grade_level', 'value'),
        State('sched_subject', 'value'),
        State('sched_teacher', 'value'),
        State('sched_schedule', 'value'),

        State('url', 'search'),
        State('sched_id', 'data'),
        State('sched_delete', 'value'),
    ]
)
def sched_savesched(submitbtn, grade_level, subject, teacher, schedule, urlsearch, 
                             id, sched_delete_ind):
    ctx = dash.callback_context
    # The ctx filter -- ensures that only a change in url will activate this callback
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        parsed = urlparse(urlsearch)
        create_mode = parse_qs(parsed.query)['mode'][0]

    else:
        raise PreventUpdate

    if eventid == 'sched_submit' and submitbtn:

        alert_open = False
        modal_open = False
        alert_color = ''
        alert_text = ''

        # We need to check inputs
        if not grade_level: # If title is blank, not title = True
            alert_open = True
            alert_color = 'danger'
            alert_text = 'Check your inputs. Please supply the grade level.'
        elif not subject:
            alert_open = True
            alert_color = 'danger'
            alert_text = 'Check your inputs. Please supply the subject.'
        elif not teacher:
            alert_open = True
            alert_color = 'danger'
            alert_text = 'Check your inputs. Please supply the name of the teacher.'
        elif not schedule:
            alert_open = True
            alert_color = 'danger'
            alert_text = 'Check your inputs. Please supply the schedule.'
        else: # all inputs are valid
            # Add the data into the db

            if create_mode == 'add':
                sql = '''
                    INSERT INTO class_sched (grade_level, subject,
                        teacher, schedule, sched_delete_ind)
                    VALUES (%s, %s, %s, %s, %s)
                '''
                values = [grade_level, subject, teacher, schedule, False]

            elif create_mode == 'edit':
                sql = '''
                    UPDATE class_sched 
                    SET 
                        grade_level = %s,
                        subject = %s,
                        teacher = %s,
                        schedule = %s, 
                        sched_delete_ind = %s
                    WHERE
                        id = %s
                '''
                values = [grade_level, subject, teacher, schedule, 
                          bool(sched_delete_ind),
                          id]

            else:
                raise PreventUpdate

            modifyDB(sql, values)

            # If this is successful, we want the successmodal to show
            modal_open = True

        return [alert_color, alert_text, alert_open, modal_open]

    else: 
        raise PreventUpdate
