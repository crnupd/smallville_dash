import dash
import dash_bootstrap_components as dbc
from dash import Output, Input, State, dcc, html
from dash.exceptions import PreventUpdate
import pandas as pd
import dash_table

from app import app
# from apps.dbconnect import getDataFromDB

# Sample DataFrame (Replace this with your actual data)
data = {
    "Grade Level": ["Grade 1", "Grade 1", "Grade 2", "Grade 2"],
    "Subject": ["Subject 1", "Subject 2", "Subject 3", "Subject 4"],
    "Teacher": ["Teacher 1", "Teacher 2", "Teacher 3", "Teacher 4"],
    "Schedule": ["MWF 10:00-11:00", "MWF 11:00-12:00", "TTh 12:00-1:00", "TTh 1:00-2:00"],
}
df = pd.DataFrame(data)


layout = html.Div(
    [
        dbc.Card( # Card Container
            [
                dbc.CardHeader( # Define Card Header
                    [
                        html.H2("Teacher's Class Schedule", style={"textAlign": "center"}),
                        html.Div("Use this page to view the class schedules. You may also utilize the links to pages for assigning students and editing schedules.", style={"textAlign": "center"}),
                    ]
                ),
                dbc.CardBody( # Define Card Contents
                    [
                        html.Div( # Add Movie Btn
                            [
                                dcc.Dropdown(
                                    id="grade-dropdown",
                                    options=[{"label": grade, "value": grade} for grade in df["Grade Level"].unique()],
                                    placeholder="Select Grade Level",
                                    style={"width": "300px"}
                                ),
                                
                                html.Div([
                                    dbc.Button("Add Class",
                                        color='primary',
                                        style={"margin-right": "10px", "margin-top":"10px"},
                                        href=f'/teacher/teacher_sched_add',
                                    ),
                                    ], style={'display': 'flex', 'justify-content': 'flex-end'}
                                ),  
                                
                                html.H3(id="student-schedule-header", style={"marginTop": "20px"}),
                                
                                html.H5("Class 1", style={"textAlign": "left"}),
                                
                                dash_table.DataTable(
                                    id="schedule-table",
                                    columns=[
                                        {"name": "Subject", "id": "Subject"},
                                        {"name": "Teacher", "id": "Teacher"},
                                        {"name": "Schedule", "id": "Schedule"}
                                    ],
                                    data=df.to_dict("records"),
                                    style_table={"margin": "auto"},
                                    style_header={"backgroundColor": "#003366", "color": "white", "fontWeight": "bold"},
                                    style_cell={"textAlign": "left", "padding": "10px"}
                                ),
                               
                                html.Div([
                                    dbc.Button("Edit",
                                        color='primary',
                                        style={"margin-right": "10px", "margin-top":"10px"},
                                        href=f'/teacher/teacher_sched_edit',
                                    ),
                                    dbc.Button("Add Students",
                                        color='primary',
                                        style={"margin-top":"10px"},
                                        href=f'/teacher/teacher_sched_add',
                                    ),
                                    ], style={'display': 'flex', 'justify-content': 'flex-end'}
                                )   
                                ]
                            )
                        ]       
                    )   
                ]
            )
        ]
    )
   


@app.callback(
    Output("teach-schedule-table", "data"),
    [Input("grade-dropdown", "value")]
)

def update_table(selected_grade):
    if selected_grade:
        filtered_df = df[df["Grade Level"] == selected_grade]
    else:
        filtered_df = df
    return filtered_df.to_dict("records")