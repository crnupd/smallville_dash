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
    "Grade": ["Grade 1", "Grade 2", "Grade 3"],
    "Class": [
        ["Subject 1", "Subject 2", "Subject 3", "Subject 4"],
        ["Subject 1", "Subject 2", "Subject 3", "Subject 4"],
        ["Subject 1", "Subject 2", "Subject 3", "Subject 4"],
    ],
    "Teacher": [
        ["Teacher 1", "Teacher 2", "Teacher 3", "Teacher 4"],
        ["Teacher A", "Teacher B", "Teacher C", "Teacher D"],
        ["Teacher 5", "Teacher 6", "Teacher 7", "Teacher 8"],
    ],
    "Schedule": [
        ["MWF 10:00 AM-11:00 AM", "MWF 11:00 AM-12:00 PM", "TTh 12:00 PM-1:00 PM", "TTh 1:00 PM-2:00 PM"],
        ["MWF 9:00 AM-10:00 AM", "MWF 10:00 AM-11:00 AM", "TTh 11:00 AM-12:00 PM", "TTh 12:00 PM-1:00 PM"],
        ["MWF 8:00 AM-9:00 AM", "MWF 9:00 AM-10:00 AM", "TTh 10:00 AM-11:00 AM", "TTh 11:00 AM-12:00 PM"],
    ],
}

# Convert data into a DataFrame for easier handling
schedule_data = pd.DataFrame(data)

layout = html.Div(
    [
        dbc.Card( # Card Container
            [
                dbc.CardHeader( # Define Card Header
                    [
                        html.H2("Class Schedule", style={"textAlign": "center"}),
                        html.Div("Use this page to view the class schedule for each grade level.", style={"textAlign": "center"}),
                    ]
                ),
                dbc.CardBody( # Define Card Contents
                    [
                        html.Div( # Add Movie Btn
                            [
                                html.Label("Select Grade Level:"),
                                dcc.Dropdown(
                                    id="student-dropdown",
                                    options=[{"label": grade, "value": grade} for grade in schedule_data["Grade"]],
                                    value="Grade 1",
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
    idx = schedule_data[schedule_data["Grade"] == selected_student].index[0]
    classes = schedule_data.loc[idx, "Class"]
    teachers = schedule_data.loc[idx, "Teacher"]
    schedules = schedule_data.loc[idx, "Schedule"]

    table_data = [
        {"Class": cls, "Teacher": teacher, "Schedule": schedule}
        for cls, teacher, schedule in zip(classes, teachers, schedules)
    ]

    header = f"{selected_student}'s Schedule"
    return header, table_data