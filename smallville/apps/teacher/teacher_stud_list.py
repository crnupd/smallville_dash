import dash
import dash_bootstrap_components as dbc
from dash import Output, Input, State, dcc, html
from dash.exceptions import PreventUpdate
import pandas as pd
from app import app
from apps.dbconnect import getDataFromDB  # Assuming the database connection functions are implemented here

# Layout for the Students List page in the Teacher folder
layout = html.Div(
    [
        dcc.Location(id='url_teacher_stud_list', refresh=False),  # Tracks the URL with unique ID
        # Page Header
        html.Div(
            [
                html.H2('Students List'),
                html.Hr(),
            ],
            style={'margin-top': '15px'}  # Adjust margin to avoid overlap with navbar
        ),
        dbc.Card(  # Card Container
            [
                dbc.CardHeader(  # Define Card Header
                    dbc.Row(  # Use Row to align text and button
                        [
                            dbc.Col(
                                html.H3('Manage Records'),
                                width=10  # Occupy 10 parts of the row
                            ),
                        ],
                        justify="between",  # Spread the columns across the row
                        align="center",  # Vertically align items in the row to the center
                    ),
                ),
                dbc.CardBody(  # Define Card Contents
                    [
                        html.Hr(),
                        html.Div(  # Create section to show list of students
                            [
                                html.H4('Sort Students'),
                                dbc.Row([  # Sorting section first
                                    dbc.Col(
                                        dbc.Row([  # Use another Row to place them side by side inside this column
                                            dbc.Col(  # Column for the dropdown
                                                dcc.Dropdown(
                                                    id="sort_column_teacher",
                                                    options=[
                                                        {'label': 'Student ID', 'value': 'stud_id'},
                                                        {'label': 'First Name', 'value': 'stud_fname'},
                                                        {'label': 'Last Name', 'value': 'stud_lname'},
                                                        {'label': 'City', 'value': 'stud_city'},
                                                        {'label': 'Grade Level', 'value': 'stud_gradelvl'},
                                                        {'label': 'Enrollment Status', 'value': 'enroll_status'}
                                                    ],
                                                    placeholder="Select Column to Sort",
                                                    value='stud_fname',  # Default column to sort
                                                    clearable=False,
                                                    style={'margin': '2px 0px'}  # Margin adjustments
                                                ),
                                            ),
                                            dbc.Col(  # Column for the button
                                                dbc.Button(
                                                    'Sort',
                                                    id='sort_button_teacher',
                                                    color='primary',
                                                    n_clicks=0,
                                                    style={'margin': '2px 0px'}  # 2px margin for the button
                                                ),
                                            ),
                                        ]), 
                                        width=12,  # Occupy full width for the parent column (12/12)
                                    ),
                                ]),  # Sorting section end

                                html.Hr(),

                                html.H4('Find Students'),
                                dbc.Row([  # Row for the label and filter text box
                                    dbc.Col(
                                        dbc.Input(
                                            type='text',
                                            id='student_fnamefilter_teacher',
                                            placeholder='Search by Selected Column',
                                            value=''  # Set empty value for the filter textbox
                                        ),
                                        width=12  # Text box next to the label, occupies remaining space
                                    )
                                ]),  # Find students filter end
                                html.Hr(),
                                html.Div(id='student_studentlist_teacher')  # Placeholder for student table
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)

# Single callback to handle both the student table and the filter value
@app.callback(
    Output('student_studentlist_teacher', 'children'),
    [
        Input('url_teacher_stud_list', 'pathname'),
        Input('sort_column_teacher', 'value'),
        Input('sort_button_teacher', 'n_clicks'),
        Input('student_fnamefilter_teacher', 'value')
    ],
    prevent_initial_call=True  # Prevent the callback from triggering on initial page load
)
def updateRecordsTable(pathname, sort_column, n_clicks, student_fnamefilter):
    print(f"Callback triggered. Pathname: {pathname}, Sort Column: {sort_column}, Filter: {student_fnamefilter}, Clicks: {n_clicks}")

    # Only trigger the callback if the correct path is matched
    if pathname != '/teacher/teacher_stud_list':
        print(f"Incorrect Path: {pathname}")
        return html.Div("This page doesn't exist.")  # Return empty filter value if path doesn't match

    # SQL query for fetching data
    sql = """ 
    SELECT 
        stud_id AS "Student ID",
        stud_fname AS "First Name",
        stud_lname AS "Last Name",
        stud_city AS "City",
        stud_address AS "Address",
        stud_gradelvl AS "Grade Level",
        enroll_status AS "Enrollment Status"
    FROM student
    WHERE NOT stud_delete_ind
    """
    val = []

    # Apply filter based on the selected column and filter value
    if student_fnamefilter and sort_column:
        if sort_column == "enroll_status":
            student_fnamefilter = student_fnamefilter.lower()
            if student_fnamefilter == 'enrolled':
                sql += " AND enroll_status = TRUE"
            elif student_fnamefilter == 'not enrolled':
                sql += " AND enroll_status = FALSE"
        else:
            sql += f""" AND {sort_column} ILIKE %s"""
            val += [f'%{student_fnamefilter}%']

    # Handle sorting based on button clicks
    sort_direction = "ASC" if n_clicks % 2 == 0 else "DESC"
    if sort_column:
        sql += f" ORDER BY {sort_column} {sort_direction}"

    # Columns for the DataFrame
    col = ["Student ID", "First Name", "Last Name", "City", "Address", "Grade Level", "Enrollment Status"]

    # Fetch data from the database
    df = getDataFromDB(sql, val, col)

    # If no data found, return a message
    if df.empty:
        return html.Div("No data available")  # Return empty filter value if no data

    # Replace enroll_status True/False values with 'Enrolled'/'Not Enrolled'
    df['Enrollment Status'] = df['Enrollment Status'].apply(lambda x: 'Enrolled' if x else 'Not Enrolled')

    # Generate 'Action' button column with edit links
    df['Action'] = [
        html.Div(
            dbc.Button(
                "Edit",
                style={'backgroundColor': 'Maroon', 'color': 'white'},
                size='sm',
                href=f'/teacher/teacher_stud_list_edit?mode=edit&id={row["Student ID"]}'
            ),
            className='text-center'
        ) for _, row in df.iterrows()
    ]

    # Reorganize columns for display
    df = df[["Student ID", "First Name", "Last Name", "City", "Address", "Grade Level", "Enrollment Status", 'Action']]

    # Generate the table from DataFrame
    student_table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')

    # Return the updated table
    return student_table


# Separate callback to reset the filter value (used independently)
@app.callback(
    Output('student_fnamefilter_teacher', 'value'),
    [Input('url_teacher_stud_list', 'pathname')],
    prevent_initial_call=True
)
def reset_filter(pathname):
    # Reset the filter value only if the correct path is matched
    if pathname == '/teacher/teacher_stud_list':
        return ''  # Reset filter to empty on page load or navigation
    raise PreventUpdate  # Prevent update when not on the correct page
