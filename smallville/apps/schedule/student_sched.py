import dash
import dash_bootstrap_components as dbc
from dash import Output, Input, State, dcc, html
from dash.exceptions import PreventUpdate
import pandas as pd
from constants import ADMIN_USER_ID
from app import app
from apps.dbconnect import getDataFromDB, modifyDB

sql = """
SELECT 
    grade_level AS "Grade Level",
    subject AS "Subject",
    teacher AS "Teacher",
    schedule AS "Schedule",
    id
FROM class_sched
WHERE sched_delete_ind = False  -- Only show non-deleted records
"""

layout = html.Div(
    [
        html.Div(
            [
                html.H2('View Schedules'),
                html.Hr(),
            ],
            style={'margin-top': '70px'}
        ),
        
        dcc.Store(id='schedule-data', storage_type='memory'),

        dbc.Card(
            [
                dbc.CardHeader(
                    [
                        html.H2("Class Schedule", style={"textAlign": "center"}),
                        html.Div("View the class schedules for each grade level below.", style={"textAlign": "center"}),
                    ]
                ),
                dbc.CardBody(
                    [
                        html.Div(id="schedules-tables"),
                    ]
                ),
            ]
        ),
    ]
)

# fetch and store the data from DB
@app.callback(
    Output('schedule-data', 'data'),
    Input('url', 'pathname'),
)
def fetch_data_on_load(pathname):
    val = []
    col = ["Grade Level", "Subject", "Teacher", "Schedule", "id"]
    df = getDataFromDB(sql, val, col)
    return df.to_dict(orient='records')

# display tables based on dcc.Store
@app.callback(
    Output('schedules-tables', 'children'),
    Input('schedule-data', 'data'),
    State('currentuserid', 'data')
)
def display_table(data, currentuserid):
    
    if data is None:
        raise PreventUpdate

    df = pd.DataFrame(data)
    
    # group by grade level
    df_grouped = df.groupby('Grade Level').agg({
        'Subject': list, 
        'Teacher': list, 
        'Schedule': list
    }).reset_index()

    # generate the tables dynamically based on the data
    tables = []
    for _, grade_data in df_grouped.iterrows():
        tables.append(
            html.Div(
                [
                    html.H3(f"{grade_data['Grade Level']}", style={"marginTop": "20px", 'textAlign':'center'}),
                    
                    html.Div(
                        dbc.Button(
                            "View Assigned Students", 
                            href=f"/student/sched_assign?grade_level={grade_data['Grade Level']}", 
                            color="primary", 
                            className="mb-2" 
                        ) if currentuserid == ADMIN_USER_ID else None,
                        style={'textAlign': 'center', 'margin-bottom':'10px'}
                    ),
                    
                    dbc.Table(
                        id=f"schedule-table-{grade_data['Grade Level']}", 
                        children=[
                            html.Thead(
                                html.Tr(
                                    [
                                        html.Th("Subject", style={'textAlign': 'center'}),
                                        html.Th("Teacher", style={'textAlign': 'center'}),
                                        html.Th("Schedule", style={'textAlign': 'center'}),
                                    ]
                                )
                            ),
                            html.Tbody(
                                [
                                    html.Tr(
                                        [
                                            html.Td(subject),
                                            html.Td(teacher),
                                            html.Td(schedule),
                                        ]
                                    )
                                    for subject, teacher, schedule in zip(
                                        grade_data['Subject'], 
                                        grade_data['Teacher'], 
                                        grade_data['Schedule']
                                    )
                                ]
                            ),
                        ],
                        style={'tableLayout': 'fixed', 'width': '100%'},
                        bordered=True, striped=True, hover=True, className="table-info"
                    ),
                    html.Hr(style={'borderTop':'5px solid'})
                ],
                style={"marginBottom": "50px"} 
            )
        )
    
    return tables

# manually update the data after a database change
@app.callback(
    Output('schedule1-data', 'data'),
    Input('sched_submit', 'n_clicks'),
    State('sched_grade_level', 'value'),
    State('sched_subject', 'value'),
    State('sched_teacher', 'value'),
    State('sched_schedule', 'value'),
    State('sched_delete', 'value'),
    State('sched_id', 'data'), 
    prevent_initial_call=True
)
def update_schedule_data(n_clicks, grade_level, subject, teacher, schedule, delete_value, id):
    if n_clicks == 0:
        raise PreventUpdate

    if delete_value:
        sql = '''
            UPDATE class_sched
            SET sched_delete_ind = %s
            WHERE id = %s
        '''
        modifyDB(sql, [True, id])
    else:
        if id == 0: 
            sql = '''
                INSERT INTO class_sched (grade_level, subject, teacher, schedule, sched_delete_ind)
                VALUES (%s, %s, %s, %s, %s)
            '''
            modifyDB(sql, [grade_level, subject, teacher, schedule, False])
        else: 
            sql = '''
                UPDATE class_sched
                SET grade_level = %s, subject = %s, teacher = %s, schedule = %s
                WHERE id = %s
            '''
            modifyDB(sql, [grade_level, subject, teacher, schedule, id])

    # re-fetch data
    val = []
    col = ["Grade Level", "Subject", "Teacher", "Schedule", "id"]
    df = getDataFromDB(sql, val, col)
    
    # return the updated data for `dcc.Store`
    return df.to_dict(orient='records') 

