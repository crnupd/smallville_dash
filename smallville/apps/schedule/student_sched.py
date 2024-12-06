import dash
import dash_bootstrap_components as dbc
from dash import Output, Input, State, dcc, html
from dash.exceptions import PreventUpdate
import pandas as pd
import dash_table

from app import app
from apps.dbconnect import getDataFromDB

sql = """
SELECT 
    grade_level AS "Grade Level",
    subject AS "Subject",
    teacher AS "Teacher",
    schedule AS "Schedule",
    id
FROM class_sched
WHERE TRUE
"""

val = []

col = ["Grade Level", "Subject", "Teacher", "Schedule", "id"]

df = getDataFromDB(sql, val, col)

df_grouped = df.groupby('Grade Level').agg({
    'Subject': list, 
    'Teacher': list, 
    'Schedule': list
}).reset_index()

layout = html.Div(
    [
        html.Div(
            [
                html.H2('View Schedules'),
                html.Hr(),
            ],
            style={'margin-top': '15px'}
        ),

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
                        # Wrap dynamically generated elements in a list
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H3(f"Grade {grade_data['Grade Level']}", style={"marginTop": "20px", 'textAlign':'center'}),
                                        
                                        html.Div(
                                            dbc.Button(
                                                "Assign Students",  # Button text
                                                href=f"/student/sched_assign={grade_data['Grade Level']}",  # URL for the button
                                                color="primary",  # Button styling
                                                className="mb-2"  # Add margin on bottom for spacing
                                            ),
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
                                for _, grade_data in df_grouped.iterrows()  # Loop through each grade level
                            ]
                        )
                    ]
                ),
            ]
        ),
    ]
)