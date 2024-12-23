import dash
import dash_bootstrap_components as dbc
from dash import Output, Input, State, dcc, html
from dash.exceptions import PreventUpdate
import psycopg2
from psycopg2 import sql
from app import app
from apps.dbconnect import getDataFromDB, modifyDB

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.H2('Schedule Management', style={'width': "100%"}), width=10), 
                dbc.Col(
                    dbc.Button(
                        "Return",
                        color='primary',
                        href=f'/admin',
                    ),
                    width=2,
                    className="text-end"
                )
            ],
            align="center"
        ),
        html.Hr(),
        
        dbc.Card( 
            [
                dbc.Alert(id='sched_alert', is_open=False), 
                dbc.CardHeader( 
                    html.H2("Add a Schedule", style={"textAlign": "center"}),
                ),
                
                html.Br(),
            
                html.Div([
                    dbc.Row(
                    [
                        dbc.Label("Grade Level", width=1, style={"textAlign":"left", 'margin-left':'15px'}),
                        dbc.Col(
                        dbc.Select(
                            id='grade_level',
                            options=[
                                {'label': 'Kindergarten', 'value': 'Kindergarten'},
                                {'label': 'Pre-School', 'value': 'Pre-School'},
                                {'label': 'Grade 1', 'value': 'Grade 1'},
                                {'label': 'Grade 2', 'value': 'Grade 2'},
                                {'label': 'Grade 3', 'value': 'Grade 3'},
                                {'label': 'Grade 4', 'value': 'Grade 4'},
                                {'label': 'Grade 5', 'value': 'Grade 5'},
                                {'label': 'Grade 6', 'value': 'Grade 6'},
                            ],
                            value='Kindergarten',
                        ),
                        width=3,
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
                        dbc.Button("Add", id="add_button", n_clicks=0, style={'margin-top':'10px'}),
                        style={'display': 'flex',
                            'justify-content': 'space-between',
                            'align-items': 'center',
                            'margin-left': '15px',
                            'margin-right': '15px'} 
                    ),            

                    dbc.Modal(
                        [
                            dbc.ModalHeader(html.H4("Save Success!")
                            ),
                        dbc.ModalBody("Schedule successfully added to the database."),
                        dbc.ModalFooter(
                            dbc.Button(
                                "Proceed",
                                href = '/admin'
                            )
                        )
                        ],
                        centered=True,
                        id="sched_successmodal",
                        backdrop="static"
                    ),

                    html.Div(id="alert", style={"marginTop": "10px", "color": "green", "fontWeight": "bold"}),
                ], style={"textAlign": "center"}),
            ]
        )
    ],
    style={'margin-top': '70px'}
)

@app.callback(
    [
    Output('alert', 'color'),
    Output('alert', 'children'),
    Output('alert','is_open'),
    Output('sched_successmodal','is_open')
    ],
    Input('add_button', 'n_clicks'),
    [
    State('grade_level', 'value'),
    State('subject', 'value'),
    State('teacher','value'),
    State('schedule','value')
    ]
)

def sched_save(submitbtn, grade_level, subject, teacher, schedule):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == "add_button" and submitbtn:
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''
            if not grade_level: 
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
                        INSERT INTO class_sched (grade_level, subject, teacher, schedule, sched_delete_ind)
                        VALUES (%s, %s, %s, %s, %s)
                    '''
                values = [grade_level, subject, teacher, schedule, False]

                modifyDB(sql, values)

                modal_open = True

                return [alert_color, alert_text, alert_open, modal_open]
        
        else: 
            raise PreventUpdate
    
    else:
        raise PreventUpdate