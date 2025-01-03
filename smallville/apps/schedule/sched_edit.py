from urllib.parse import urlparse, parse_qs
import dash
import dash_bootstrap_components as dbc
from dash import Output, Input, State, dcc, html
from dash.exceptions import PreventUpdate
from app import app
from apps.dbconnect import getDataFromDB, modifyDB
import pandas as pd

layout = html.Div(
    [
dbc.Row(
            [
                dbc.Col(html.H2('Update Schedule', style={'width': "100%"}), width=10),
                dbc.Col(
                    dbc.Button(
                        "Return",
                        color='primary',
                        href=f'/admin'
                    ),
                    width=2,
                    className="text-end"  
                )
            ],
            align="center",
            style={'margin-top': '70px'} 
        ),

        dcc.Store(id="sched_id", storage_type="memory", data=0),
        html.Hr(),
        dbc.Alert(id="sched_alert", is_open=False), 
        
        dbc.Form(
            [
                dbc.Row(
                    [
                        dbc.Label("Grade Level", width=1),
                        dbc.Col(
                        dbc.Select(
                            id='sched_grade_level',
                            options=[
                                {'label': 'Kindergarten', 'value': 'Kindergarten'},
                                {'label': 'Pre-school', 'value': 'Pre-school'},
                                {'label': 'Grade 1', 'value': 'Grade 1'},
                                {'label': 'Grade 2', 'value': 'Grade 2'},
                                {'label': 'Grade 3', 'value': 'Grade 3'},
                                {'label': 'Grade 4', 'value': 'Grade 4'},
                                {'label': 'Grade 5', 'value': 'Grade 5'},
                                {'label': 'Grade 6', 'value': 'Grade 6'},
                            ],
                        ),
                        width=5,
                        ),
                    ],
                    className="mb-3",
                ),
                dbc.Row(
                    [
                        dbc.Label("Subject", width=1),
                        dbc.Col(
                            dbc.Input(
                                type="text", id="sched_subject", placeholder="Subject"
                            ),
                            width=5,
                        ),
                    ],
                    className="mb-3",
                ),
                dbc.Row(
                    [
                        dbc.Label("Teacher", width=1),
                        dbc.Col(
                            dbc.Input(
                                type="text", id="sched_teacher", placeholder="Teacher"
                            ),
                            width=5,
                        ),
                    ],
                    className="mb-3",
                ),
                dbc.Row(
                    [
                        dbc.Label("Schedule", width=1),
                        dbc.Col(
                            dbc.Input(
                                type="text", id="sched_schedule", placeholder="Schedule"
                            ),
                            width=5,
                        ),
                    ],
                    className="mb-3",
                ),
            ]
        ),
        html.Div(
            [
                dbc.Checklist(
                    id="sched_delete",
                    style={"margin-top": "10px"},
                    options=[dict(value=1, label="Tick to Delete")],
                    value=[],
                )
            ],
            id="sched_deletediv",
        ),
        dbc.Button(
            "Submit",
            id="sched_submit",
            n_clicks=0, 
            style={"margin-top": "20px"},
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(html.H4("Save Success!")),
                dbc.ModalBody("Schedule successfully updated."),
                dbc.ModalFooter(
                    dbc.Button(
                        "Proceed", href="/admin" 
                    )
                ),
            ],
            centered=True,
            id="sched2_successmodal",
            backdrop="static", 
        ),
    ]
)

# parsing the URL and setting initial states
@app.callback(
    [
        Output("sched_id", "data"),
        Output("sched_deletediv", "className"),
        Output("sched_grade_level", "value"),
        Output("sched_subject", "value"),
        Output("sched_teacher", "value"),
        Output("sched_schedule", "value"),
    ],
    [
        Input("url", "pathname"),
    ],
    [
        State("url", "search"),
    ],
)
def sched_editprofile(pathname, urlsearch):
    if pathname == "/student/sched_edit":
        parsed = urlparse(urlsearch)
        create_mode = parse_qs(parsed.query)["mode"][0]

        # determine ID and delete div class based on mode
        if create_mode == "add":
            id = 0
            deletediv = "d-none" 
            return [id, deletediv, "", "", "", ""]
        else:
            id = int(parse_qs(parsed.query)["id"][0])
            deletediv = "" 

            sql = '''
                SELECT grade_level, subject, teacher, schedule
                FROM class_sched
                WHERE id = %s AND sched_delete_ind = False
            '''
            result = getDataFromDB(sql, [id], ["grade_level", "subject", "teacher", "schedule"])

            if not result.empty:
                # return current values as placeholders
                return [
                    id,
                    deletediv,
                    result["grade_level"].iloc[0],
                    result["subject"].iloc[0],
                    result["teacher"].iloc[0],
                    result["schedule"].iloc[0],
                ]
            else:
                return [id, deletediv, "", "", "", ""]

    else:
        raise PreventUpdate


# callback for saving or deleting schedule
@app.callback(
    [
        Output("sched_alert", "color"),
        Output("sched_alert", "children"),
        Output("sched_alert", "is_open"),
        Output("sched2_successmodal", "is_open"),
    ],
    [
        Input("sched_submit", "n_clicks"), 
    ],
    [
        State("sched_delete", "value"),
        State("sched_grade_level", "value"),
        State("sched_subject", "value"),
        State("sched_teacher", "value"),
        State("sched_schedule", "value"),
        State("url", "search"),
        State("sched_id", "data"),
    ],
)
def sched_submit_action(submitbtn, delete_value, grade_level, subject, teacher, schedule, urlsearch, id):
    ctx = dash.callback_context

    if not ctx.triggered or not submitbtn:
        raise PreventUpdate

    alert_open = False
    modal_open = False
    alert_color = ""
    alert_text = ""

    # parse the URL
    parsed = urlparse(urlsearch)
    create_mode = parse_qs(parsed.query)["mode"][0]

    if delete_value:
        sql = '''
            UPDATE class_sched
            SET sched_delete_ind = %s
            WHERE id = %s
        '''
        values = [True, id]
        modifyDB(sql, values)

        alert_open = True
        alert_color = "success"
        alert_text = f"Schedule has been deleted."
        modal_open = True

    else:
        # validate inputs for regular updates or additions
        if not grade_level:
            alert_open = True
            alert_color = "danger"
            alert_text = "Check your inputs. Please supply the grade level."
        elif not subject:
            alert_open = True
            alert_color = "danger"
            alert_text = "Check your inputs. Please supply the subject."
        elif not teacher:
            alert_open = True
            alert_color = "danger"
            alert_text = "Check your inputs. Please supply the name of the teacher."
        elif not schedule:
            alert_open = True
            alert_color = "danger"
            alert_text = "Check your inputs. Please supply the schedule."
        else:
            # insert or update the record in the database
            if create_mode == "add":
                sql = '''
                    INSERT INTO class_sched (grade_level, subject, teacher, schedule, sched_delete_ind)
                    VALUES (%s, %s, %s, %s, %s)
                '''
                values = [grade_level, subject, teacher, schedule, False]
            elif create_mode == "edit":
                sql = '''
                    UPDATE class_sched
                    SET grade_level = %s, subject = %s, teacher = %s, schedule = %s
                    WHERE id = %s
                '''
                values = [grade_level, subject, teacher, schedule, id]

            modifyDB(sql, values)

            alert_open = True
            alert_color = "success"
            alert_text = "Schedule successfully updated."
            modal_open = True

    return [alert_color, alert_text, alert_open, modal_open]
