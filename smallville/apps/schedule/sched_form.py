import dash
import dash_bootstrap_components as dbc
from dash import Output, Input, State, dcc, html
from dash.exceptions import PreventUpdate

import psycopg2
from psycopg2 import sql
from app import app
from apps.dbconnect import getDataFromDB, modifyDB

# Layout for the page
layout = html.Div(
    [
        dbc.Card(  # Card Container
            [
                dbc.Alert(id='movieprofile_alert', is_open=False), 
                dbc.CardHeader(  # Define Card Header
                    html.H2("Add a Schedule", style={"textAlign": "center"}),
                ),
                
                html.Br(),
                # Input fields
                html.Div([
                    dbc.Row(
                        [dbc.Label("Grade Level", width=1, style={"textAlign":"left", 'margin-left':'15px'}),
                            dbc.Col(
                                dbc.Input(id="grade_level", type="text", placeholder="Grade Level"),
                            width=3
                            ),
                        ]),
                    dbc.Row(
                        [dbc.Label("Subject", width=1, style={"textAlign":"left", 'margin-left':'15px'}),
                            dbc.Col(
                                dbc.Input(id="subject", type="text", placeholder="Subject"),
                            width=3
                            ),
                        ]),
                    dbc.Row(
                        [dbc.Label("Teacher", width=1, style={"textAlign":"left", 'margin-left':'15px'}),
                            dbc.Col(
                                dbc.Input(id="teacher", type="text", placeholder="Teacher"),
                            width=3
                            ),
                        ]),
                    dbc.Row(
                        [dbc.Label("Schedule", width=1, style={"textAlign":"left", 'margin-left':'15px'}),
                            dbc.Col(
                                dbc.Input(id="schedule", type="text", placeholder="Schedule"),
                            width=3
                            ),
                        ]),
                    
                    html.Div(
                        [
                        dbc.Button("Add", id="add_button", n_clicks=0, style={'margin-top':'10px'}),
                        dbc.Button("Back", href=f'/student/sched_management', id="back_button", n_clicks=0, style={'margin-top': '10px'}),
                        ],
                        style={'display': 'flex',
                            'justify-content': 'space-between',
                            'align-items': 'center',
                            'margin-left': '15px',
                            'margin-right': '15px'}  # Aligns the button on the right side
                    ),            

                    dbc.Modal(
                        [
                            dbc.ModalHeader(html.H4("Save Success!")
                            ),
                        dbc.ModalBody("Schedule successfully added to the database."),
                        dbc.ModalFooter(
                            dbc.Button(
                                "Proceed",
                                href = '/student/sched_management'
                            )
                        )
                        ],
                        centered=True,
                        id="sched_successmodal",
                        backdrop="static"
                    ),

                    # dcc.Input(id="search-bar", type="text", placeholder="Search schedules...", style={"margin": "10px", "width": "300px"}),

                    html.Div(id="alert", style={"marginTop": "10px", "color": "green", "fontWeight": "bold"}),
                ], style={"textAlign": "center"}),
            ]
        )
    ]
)

@app.callback(
    [
    Output('alert', 'color'),
    Output('alert', 'children'),
    Output('alert','is_open'),
    Output('sched_successmodal','is_open')
    ],
    [
    Input('add_button', 'n_clicks'),
    Input('back_button', 'n_clicks')
    ],
    [
    State('grade_level', 'value'),
    State('subject', 'value'),
    State('teacher','value'),
    State('schedule','value')
    ]
)

def sched_save(submitbtn, backbtn, grade_level, subject, teacher, schedule):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == "add_button" and submitbtn:
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''
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
                alert_text = 'Check your inputs. Please supply the teacher.'
            elif not schedule:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the schedule.'
            else:
                sql = '''
                        INSERT INTO class_sched (grade_level, subject, teacher, schedule, sched_edit)
                        VALUES (%s, %s, %s, %s, %s)
                    '''
                values = [grade_level, subject, teacher, subject, False]

                modifyDB(sql, values)

                    # If this is successful, we want the successmodal to show
                modal_open = True

                return [alert_color, alert_text, alert_open, modal_open]
        
        elif eventid == 'back_button' and backbtn:
            raise PreventUpdate
        else: 
            raise PreventUpdate
    
    else:
        raise PreventUpdate