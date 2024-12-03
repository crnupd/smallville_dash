import dash
import dash_bootstrap_components as dbc
from dash import Output, Input, html
from dash.exceptions import PreventUpdate

import pandas as pd

from app import app
from apps.dbconnect import getDataFromDB  # Assuming the database connection functions are implemented here

layout = html.Div(
    [
        # Page Header
        html.Div(
            [
                html.H2('Students'),
                html.Hr(),
            ],
            style={'margin-top': '60px'}  # Adjust margin to avoid overlap with navbar
        ),
        dbc.Card(  # Card Container
            [
                dbc.CardHeader(  # Define Card Header
                    [
                        html.H3('Manage Records')
                    ]
                ),
                dbc.CardBody(  # Define Card Contents
                    [
                        html.Div(  # Add Student Btn
                            [
                                dbc.Button(
                                    "Add Student",
                                    href='/student/student_profile_edit?mode=add'
                                )
                            ]
                        ),
                        html.Hr(),
                        html.Div(  # Create section to show list of students
                            [
                                html.H4('Find Students'),
                                dbc.Form(
                                    dbc.Row(
                                        [
                                            dbc.Label("Search First Name", width=1.4),
                                            dbc.Col(
                                                dbc.Input(
                                                    type='text',
                                                    id='student_fnamefilter',
                                                    placeholder='First Name'
                                                ),
                                                width=5
                                            )
                                        ],
                                    )
                                ),
                                html.Div(id='student_studentlist')  # Placeholder for student table
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)

@app.callback(
    Output('student_studentlist', 'children'),
    [Input('url', 'pathname'),
     Input('student_fnamefilter', 'value')]  # Watch for changes to the URL and fnamefilter
)
def updateRecordsTable(pathname, student_fnamefilter):
    print(f"Callback triggered. Pathname: {pathname}")

    # Only trigger the callback if the correct path is matched
    if pathname != '/student/student_profile':
        print(f"Incorrect Path: {pathname}")
        return html.Div("This page doesn't exist.")
    
    # SQL query for fetching data
    sql = """ 
    SELECT 
        stud_id,
        stud_fname AS "First Name",
        stud_lname AS "Last Name",
        stud_city AS "City",
        stud_address AS "Address",
        stud_gradelvl AS "Grade Level"
    FROM student
    WHERE NOT stud_delete_ind
    """
    val = []

    # Add filter for first name if provided
    if student_fnamefilter:
        sql += """ AND stud_fname ILIKE %s"""
        val += [f'%{student_fnamefilter}%']

    # Columns for the DataFrame
    col = ["stud_id", "First Name", "Last Name", "City", "Address", "Grade Level"]

    # Fetch data from the database
    df = getDataFromDB(sql, val, col)

    # If no data found, return a message
    if df.empty:
        return html.Div("No data available")

    # Generate 'Action' button column with edit links
    df['Action'] = [
        html.Div(
            dbc.Button(
                "Edit", color='warning', size='sm', 
                href=f'/student/student_profile_edit?mode=edit&id={row["stud_id"]}'  # Using stud_id as the ID
            ),
            className='text-center'
        ) for _, row in df.iterrows()
    ]

    # Reorganize columns for display
    df = df[["First Name", "Last Name", "City", "Address", "Grade Level", 'Action']]

    # Generate the table from DataFrame
    student_table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')

    return student_table

# Run the app in debug mode
if __name__ == '__main__':
    app.run_server(debug=True)
