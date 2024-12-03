import dash
import dash_bootstrap_components as dbc
from dash import Output, Input, State, dcc, html
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
                                dbc.Row([
                                    dbc.Col(
                                        dbc.Label("Search by First Name", width=4),
                                        width=4
                                    ),
                                    dbc.Col(
                                        dbc.Input(
                                            type='text',
                                            id='student_fnamefilter',
                                            placeholder='Enter First Name to Filter'
                                        ),
                                        width=5
                                    )
                                ]),
                                html.Hr(),
                                html.H4('Sort Students'),
                                # Dropdown for selecting the column to sort by
                                dbc.Row([
                                    dbc.Col(
                                        dcc.Dropdown(
                                            id="sort_column",
                                            options=[
                                                {'label': 'First Name', 'value': 'stud_fname'},
                                                {'label': 'Last Name', 'value': 'stud_lname'},
                                                {'label': 'City', 'value': 'stud_city'},
                                                {'label': 'Grade Level', 'value': 'stud_gradelvl'}
                                            ],
                                            placeholder="Select Column to Sort",
                                            value='stud_fname',  # Default column to sort
                                            clearable=False
                                        )
                                    ),
                                    dbc.Col(
                                        dbc.Button(
                                            'Sort',
                                            id='sort_button',
                                            color='primary',
                                            n_clicks=0
                                        )
                                    ),
                                ]),
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
    [
        Input('url', 'pathname'),
        Input('sort_column', 'value'),  # The column to sort by
        Input('sort_button', 'n_clicks'),  # The button to trigger the sorting
        Input('student_fnamefilter', 'value')  # The filter value for First Name
    ],
    State('sort_column', 'value')  # To keep track of the last selected column
)
def updateRecordsTable(pathname, sort_column, n_clicks, student_fnamefilter, prev_sort_column):
    print(f"Callback triggered. Pathname: {pathname}, Sort Column: {sort_column}, Filter: {student_fnamefilter}, Clicks: {n_clicks}")

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
