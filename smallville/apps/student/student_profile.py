import dash
import dash_bootstrap_components as dbc
from dash import Output, Input, State, dcc, html
from dash.exceptions import PreventUpdate
import pandas as pd
from app import app
from apps.dbconnect import getDataFromDB  # Assuming the database connection functions are implemented here

# Layout for the Students Registration Records page
layout = html.Div(
    [
        # Page Header
        html.Div(
            [
                html.H2('Students Registration Records'),
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
                                [
                                html.H3('Manage Records'),
                                html.P("You may manage your children's registration records using this page."),
                                ],
                                width=10  # Occupy 10 parts of the row
                            ),
                            dbc.Col(  # Wrap the button properly inside a column
                                dbc.Button(
                                    "Add Student",
                                    href='/student/student_profile_edit?mode=add',
                                    color='primary',
                                    style={'float': 'right'}
                                ),
                                width=2,  # Occupy 2 parts of the row
                                className="text-right"  # Align the button to the right
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
                                # Place dropdown and button side by side inside one column
                                dbc.Row([  # Sorting section first
                                    dbc.Col(  # One column for both the dropdown and the button
                                        dbc.Row([  # Use another Row to place them side by side inside this column
                                            dbc.Col(  # Column for the dropdown
                                                dcc.Dropdown(
                                                    id="sort_column",
                                                    options=[
                                                        {'label': 'Student ID', 'value': 'stud_id'},
                                                        {'label': 'First Name', 'value': 'stud_fname'},
                                                        {'label': 'Last Name', 'value': 'stud_lname'},
                                                        {'label': 'City', 'value': 'stud_city'},
                                                        {'label': 'Grade Level', 'value': 'stud_gradelvl'},
                                                        {'label': 'Enrollment Status', 'value': 'enroll_status'}  # Added Enrollment Status
                                                    ],
                                                    placeholder="Select Column to Sort",
                                                    value='stud_fname',  # Default column to sort
                                                    clearable=False,
                                                    style={'margin': '2px 0px'}  # 2px margin top and bottom, 0px margin right
                                                ),
                                            ),
                                            dbc.Col(  # Column for the button
                                                dbc.Button(
                                                    'Sort',
                                                    id='sort_button',
                                                    color='primary',
                                                    n_clicks=0,
                                                    style={'margin': '2px 0px'}  # 2px margin for the button
                                                ),
                                            ),
                                        ]), 
                                        width=12,  # Occupy full width for the parent column (12/12)
                                    ),
                                ]), 

                                html.Hr(),

                                html.H4('Find Students'),
                                dbc.Row([  # Row for the label and filter text box
                                    dbc.Col(
                                        dbc.Input(
                                            type='text',
                                            id='student_fnamefilter',
                                            placeholder='Search by Selected Column',
                                            value=''  # Set empty value for the filter textbox
                                        ),
                                        width=12  # Text box next to the label, occupies remaining space
                                    )
                                ]), 
                                html.Hr(),
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
    [
        Output('student_studentlist', 'children'),
        Output('student_fnamefilter', 'value')  # Update the filter textbox value
    ],
    [
        Input('url', 'pathname'),
        Input('sort_column', 'value'),  # The column to sort by
        Input('sort_button', 'n_clicks'),  # The button to trigger the sorting
        Input('student_fnamefilter', 'value')  # The filter value for the selected column
    ],
    State('sort_column', 'value')  # To keep track of the last selected column
)
def updateRecordsTable(pathname, sort_column, n_clicks, student_fnamefilter, prev_sort_column):
    print(f"Callback triggered. Pathname: {pathname}, Sort Column: {sort_column}, Filter: {student_fnamefilter}, Clicks: {n_clicks}")

    # Only trigger the callback if the correct path is matched
    if pathname != '/student/student_profile':
        print(f"Incorrect Path: {pathname}")
        return html.Div("This page doesn't exist."), ''

    # SQL query for fetching data
    sql = """ 
    SELECT 
        stud_id AS "Student ID",
        stud_fname AS "First Name",
        stud_lname AS "Last Name",
        stud_city AS "City",
        stud_address AS "Address",
        stud_gradelvl AS "Grade Level",
        enroll_status AS "Enrollment Status"  -- Add enroll_status column
    FROM student
    WHERE NOT stud_delete_ind
    """
    val = []

    # Apply filter based on the selected column and filter value
    if student_fnamefilter and sort_column:
        # If the selected sort column is 'enroll_status', treat the filter as specific to that column.
        if sort_column == "enroll_status":
            # We expect 'Enrolled' or 'Not Enrolled' as the filter value
            student_fnamefilter = student_fnamefilter.lower()
            if student_fnamefilter == 'enrolled':
                sql += " AND enroll_status = TRUE"
            elif student_fnamefilter == 'not enrolled':
                sql += " AND enroll_status = FALSE"
            else:
                # If the filter is not 'Enrolled' or 'Not Enrolled', don't filter by this column
                pass
        else:
            # For other columns, apply the filter normally (ILIKE for case-insensitive search)
            sql += f""" AND {sort_column} ILIKE %s"""
            val += [f'%{student_fnamefilter}%']

    # Handle sorting based on button clicks
    # Alternate sorting direction on each button click
    if n_clicks % 2 == 0:  # Even clicks -> ascending
        sort_direction = "ASC"
    else:  # Odd clicks -> descending
        sort_direction = "DESC"

    # Apply sorting to the selected column
    if sort_column:
        sql += f" ORDER BY {sort_column} {sort_direction}"

    # Columns for the DataFrame
    col = ["Student ID", "First Name", "Last Name", "City", "Address", "Grade Level", "Enrollment Status"]

    # Fetch data from the database
    df = getDataFromDB(sql, val, col)

    # If no data found, return a message
    if df.empty:
        return html.Div("No data available"), student_fnamefilter

    # Debug: Check the values in the 'Enrollment Status' column before applying the transformation
    print("Enrollment Status Values before transformation:", df['Enrollment Status'].unique())

    # Replace the enroll_status True/False values with 'Enrolled'/'Not Enrolled'
    df['Enrollment Status'] = df['Enrollment Status'].apply(lambda x: 'Enrolled' if x else 'Not Enrolled')

    # Debug: Check the values after applying the transformation
    print("Enrollment Status Values after transformation:", df['Enrollment Status'].unique())

    # Generate 'Action' button column with edit links
    df['Action'] = [
        html.Div(
            dbc.Button(
                "Edit", 
                style={'backgroundColor': 'Maroon', 'color': 'white'},  # Crimson red button with white text
                size='sm',
                href=f'/student/student_profile_edit?mode=edit&id={row["Student ID"]}'  # Using Student ID as the ID
            ),
            className='text-center'
        ) for _, row in df.iterrows()
    ]

    # Reorganize columns for display
    df = df[["Student ID", "First Name", "Last Name", "City", "Address", "Grade Level", "Enrollment Status", 'Action']]

    # Generate the table from DataFrame
    student_table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')

    # Return the table and reset the filter text box to an empty string
    return student_table, student_fnamefilter  # The filter textbox state remains the same

# Run the app in debug mode
if __name__ == '__main__':
    app.run_server(debug=True)
