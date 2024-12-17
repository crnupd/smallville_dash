import dash
import dash_bootstrap_components as dbc
from dash import Output, Input, State, dcc, html
from dash.exceptions import PreventUpdate
import pandas as pd
from constants import ADMIN_USER_ID

from app import app
from apps.dbconnect import getDataFromDB, modifyDB

# SQL query to fetch data (this should exclude deleted rows)
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

# Layout definition
layout = html.Div(
    [
        html.Div(
            [
                html.H2('View Schedules'),
                html.Hr(),
            ],
            style={'margin-top': '70px'}
        ),
        
        # Store the schedule data in memory
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
                        # This will hold the tables dynamically generated for each grade level
                        html.Div(id="schedules-tables"),
                    ]
                ),
            ]
        ),
    ]
)

# Callback to fetch and store the data from DB
@app.callback(
    Output('schedule-data', 'data'),
    Input('url', 'pathname'),  # Or any other event that triggers the update
)
def fetch_data_on_load(pathname):
    # Fetch the data from DB when page is loaded
    val = []
    col = ["Grade Level", "Subject", "Teacher", "Schedule", "id"]
    df = getDataFromDB(sql, val, col)
    return df.to_dict(orient='records')  # Store data as a dictionary in `dcc.Store`

# Callback to display tables based on the data in `dcc.Store`
@app.callback(
    Output('schedules-tables', 'children'),
    Input('schedule-data', 'data'),
    State('currentuserid', 'data')
)
def display_table(data, currentuserid):
    
    if data is None:
        raise PreventUpdate

    # Convert the stored data back into a DataFrame
    df = pd.DataFrame(data)
    
    # Group by Grade Level
    df_grouped = df.groupby('Grade Level').agg({
        'Subject': list, 
        'Teacher': list, 
        'Schedule': list
    }).reset_index()

    # Generate the tables dynamically based on the data
    tables = []
    for _, grade_data in df_grouped.iterrows():
        tables.append(
            html.Div(
                [
                    html.H3(f"{grade_data['Grade Level']}", style={"marginTop": "20px", 'textAlign':'center'}),
                    
                    html.Div(
                        dbc.Button(
                            "View Assigned Students",  # Button text
                            href=f"/student/sched_assign?grade_level={grade_data['Grade Level']}",  # URL for the button
                            color="primary",  # Button styling
                            className="mb-2"  # Add margin on bottom for spacing
                        ) if currentuserid == ADMIN_USER_ID else None,
                        style={'textAlign': 'center', 'margin-bottom':'10px'}
                    ),
                    
                    dbc.Table(
                        id=f"schedule-table-{grade_data['Grade Level']}",  # Unique id for each table
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
                style={"marginBottom": "50px"}  # Add spacing between tables
            )
        )
    
    return tables

# Callback to manually update the data after a database change (e.g., after adding or deleting a schedule)
@app.callback(
    Output('schedule1-data', 'data'),
    Input('sched_submit', 'n_clicks'),
    State('sched_grade_level', 'value'),
    State('sched_subject', 'value'),
    State('sched_teacher', 'value'),
    State('sched_schedule', 'value'),
    State('sched_delete', 'value'),
    State('sched_id', 'data'),  # Use the ID of the schedule being edited or deleted
    prevent_initial_call=True
)
def update_schedule_data(n_clicks, grade_level, subject, teacher, schedule, delete_value, id):
    if n_clicks == 0:
        raise PreventUpdate

    # Handle delete operation
    if delete_value:
        sql = '''
            UPDATE class_sched
            SET sched_delete_ind = %s
            WHERE id = %s
        '''
        modifyDB(sql, [True, id])  # Set delete indicator to True
    else:
        if id == 0:  # Create new schedule
            sql = '''
                INSERT INTO class_sched (grade_level, subject, teacher, schedule, sched_delete_ind)
                VALUES (%s, %s, %s, %s, %s)
            '''
            modifyDB(sql, [grade_level, subject, teacher, schedule, False])
        else:  # Update existing schedule
            sql = '''
                UPDATE class_sched
                SET grade_level = %s, subject = %s, teacher = %s, schedule = %s
                WHERE id = %s
            '''
            modifyDB(sql, [grade_level, subject, teacher, schedule, id])

    # Re-fetch the data after modification
    val = []
    col = ["Grade Level", "Subject", "Teacher", "Schedule", "id"]
    df = getDataFromDB(sql, val, col)
    
    # Return the updated data for `dcc.Store`
    return df.to_dict(orient='records')  # Store updated data as a dictionary

