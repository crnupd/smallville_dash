import dash
import dash_bootstrap_components as dbc
from dash import Output, Input, State, dcc, html
from dash.exceptions import PreventUpdate
import pandas as pd
import dash_table

from app import app
# from apps.dbconnect import getDataFromDB

# Sample data for the schedule
data = {
    "Student": ["Student 1", "Student 2"],
    "Class": [
        ["Subject 1", "Subject 2", "Subject 3", "Subject 4"],
        ["Subject 1", "Subject 2", "Subject 3", "Subject 4"],
    ],
    "Teacher": [
        ["Teacher 1", "Teacher 2", "Teacher 3", "Teacher 4"],
        ["Teacher A", "Teacher B", "Teacher C", "Teacher D"],
    ],
    "Schedule": [
        ["MWF 10:00 AM-11:00 AM", "MWF 11:00 AM-12:00 PM", "TTh 12:00 PM-1:00 PM", "TTh 1:00 PM-2:00 PM"],
        ["MWF 9:00 AM-10:00 AM", "MWF 10:00 AM-11:00 AM", "TTh 11:00 AM-12:00 PM", "TTh 12:00 PM-1:00 PM"],
    ],
}

# Convert data into a DataFrame for easier handling
students_data = pd.DataFrame(data)

layout = html.Div(
    [
        dbc.Card( # Card Container
            [
                dbc.CardHeader( # Define Card Header
                    [
                        html.H2("Class Schedule", style={"textAlign": "center"}),
                        html.Div("Use this page to view the class schedule assigned to your child.", style={"textAlign": "center"}),
                    ]
                ),
                dbc.CardBody( # Define Card Contents
                    [
                        html.Div( # Add Movie Btn
                            [
                                html.Label("Select Student:"),
                                dcc.Dropdown(
                                    id="student-dropdown",
                                    options=[{"label": student, "value": student} for student in students_data["Student"]],
                                    value="Student 1",
                                    clearable=False,
                                    style={"width": "300px"}
                                    ),
                                
                                html.H3(id="student-schedule-header", style={"marginTop": "20px"}),
                                
                                dash_table.DataTable(
                                    id="schedule-table",
                                    columns=[
                                        {"name": "Class", "id": "Class"},
                                        {"name": "Teacher", "id": "Teacher"},
                                        {"name": "Schedule", "id": "Schedule"},
                                    ],
                                    style_table={"width": "80%", "margin": "auto"},
                                    style_header={
                                        "backgroundColor": "blue",
                                        "color": "white",
                                        "fontWeight": "bold",
                                    },
                                    style_cell={
                                        "textAlign": "center",
                                        "padding": "10px",
                                        "border": "1px solid black",
                                    },
                                )
                            ]
                        ),
                    ],
                ),
            ]
        ),   
    ]
)


@app.callback(
    [Output("student-schedule-header", "children"),
     Output("schedule-table", "data")],
    [Input("student-dropdown", "value")]
)

def update_schedule(selected_student):
    idx = students_data[students_data["Student"] == selected_student].index[0]
    classes = students_data.loc[idx, "Class"]
    teachers = students_data.loc[idx, "Teacher"]
    schedules = students_data.loc[idx, "Schedule"]

    table_data = [
        {"Class": cls, "Teacher": teacher, "Schedule": schedule}
        for cls, teacher, schedule in zip(classes, teachers, schedules)
    ]

    header = f"{selected_student}'s Schedule"
    return header, table_data