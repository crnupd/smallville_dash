import dash
import dash_bootstrap_components as dbc
from dash import Output, Input, State, dcc, html
from dash.exceptions import PreventUpdate
import pandas as pd
from dash import dash_table

from app import app
from apps.dbconnect import getDataFromDB


# Define the main layout variable
layout = html.Div(  # Wrap everything in a single Div
    [
        dcc.Location(id="url_admin", refresh=False), # Tracks the URL with unique ID
        # Header section with image and register button
        html.Div(style={'margin-top': '70px'},
            children=[
                html.H2("Admin Dashboard"),
                html.P("Welcome to the admin dashboard!"),
            ]
        ),

        html.Div([
            dcc.Tabs(id="tabs-styled-with-props", value='tab-1', children=[
            dcc.Tab(label='Manage Schedule', value='tab-1'),
            dcc.Tab(label='Enroll Students', value='tab-2'),
            ], colors={
        "border": "white",
        "primary": "#1e90ff",
        "background": "#cce7ff"
        }),

        html.Div(id='tabs-content-props')
        ])
    ]
)

#for tab selection
@app.callback(Output('tabs-content-props', 'children'),
              Input('tabs-styled-with-props', 'value'))
def render_content(tab):
    #for schedule management tab
    if tab == 'tab-1':
        return html.Div(
        [
            html.Div(
            [
                html.Hr(),
            ],
            style={'margin-top': '15px'}  # Adjust margin to avoid overlap with navbar
            ),

            dbc.Card( # Card Container
                [
                    dbc.CardHeader(  # Define Card Header
                        dbc.Row(  # Use Row to align text and button
                            [
                                dbc.Col(
                                    html.H3('Manage Schedules'),
                                    width=10  # Occupy 10 parts of the row
                                ),
                                dbc.Col(  # Wrap the button properly inside a column
                                    dbc.Button(
                                        "Add Schedule",
                                        href='/student/sched_form?mode=add',
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
                    
                    dbc.CardBody( # Define Card Contents
                        [
                            html.Hr(),
                            html.Div( 
                                [
                                    html.H4('Find Schedule'),
                                    html.Div(
                                        dbc.Form(
                                            dbc.Row(
                                                [
                                                    dbc.Label("Search by Grade Level", width=2),
                                                    dbc.Col(
                                                        dbc.Input(
                                                            type='text',
                                                            id='sched_filter'
                                                        ),
                                                        width=3
                                                    ),
                                                ],
                                            )
                                        )
                                    )
                                ]
                            ),
                            
                            html.Hr(),
                            html.H4('Sort Schedules'),
                            # Place dropdown and button side by side inside one column
                            dbc.Row([
                                dbc.Col(
                                    dbc.Row([  # Use another Row to place them side by side inside this column
                                        dbc.Col(# One column for both the dropdown and the button
                                            dcc.Dropdown(
                                                id="sort_column",
                                                options=[
                                                    {'label': 'Grade Level', 'value': 'grade_level'},
                                                    {'label': 'Subject', 'value': 'subject'},
                                                    {'label': 'Teacher', 'value': 'teacher'},
                                                    {'label': 'Schedule', 'value': 'schedule'}
                                                ],
                                                placeholder="Select Column to Sort",
                                                value='grade_level',  # Default column to sort
                                                clearable=False,
                                                style={'margin': '2px 0px', 'width':'300px'}
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
                                    width=4,
                                ),
                            ]),
                            html.Br(),
                            html.Div(
                                id='sched_list'
                            ),
                        ]
                    )
                ]
            )
        ]
        )
    
    #for teacher_student_list tab
    elif tab == 'tab-2':
        return html.Div(
        [
            html.Div(
            [
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
        ])

#Schedule Management Callback
@app.callback(
    [
        Output('sched_list', 'children'),
    ],
    [
        Input('url', 'pathname'),
        Input('sort_column', 'value'),
        Input('sort_button', 'n_clicks'),
        Input('sched_filter', 'value')
    ],
        State('sort_column', 'value')
)

def updateScheduleTable(pathname, sort_column, n_clicks, sched_filter, prev_sort):
    if pathname != '/admin':
        print(f"Incorrect Path: {pathname}")
        return [html.Div("This page doesn't exist.")]
    
    sql = """
    SELECT 
        grade_level AS "Grade Level",
        subject AS "Subject",
        teacher AS "Teacher",
        schedule AS "Schedule",
        id
    FROM class_sched
    WHERE sched_delete_ind = FALSE
    """
    val = []

    if sched_filter:
        sql += """ AND grade_level ILIKE %s"""
        val += [f'%{sched_filter}%']
        
    if n_clicks % 2 == 0:  # Even clicks -> ascending
        sort_direction = "ASC"
    else:  # Odd clicks -> descending
        sort_direction = "DESC"
        
    if sort_column:
        sql += f" ORDER BY {sort_column} {sort_direction}"
    
    col = ["Grade Level", "Subject", "Teacher", "Schedule", "id"]

    # Fetch data from database
    df = getDataFromDB(sql, val, col)
    
    if df.empty:
        return [html.Div("No data available")]

    df['Action'] = [
        html.Div(
            dbc.Button("Edit", color='warning', size='sm', 
                       href=f'/student/sched_edit?mode=edit&id={row["id"]}'),
            className='text-center'
        ) for _, row in df.iterrows()
    ]
    
    # Exclude 'id' column
    df = df[["Grade Level", "Subject", "Teacher", "Schedule","Action"]]

    # Create the table to display the filtered data
    sched_table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm',
                                           style={'textAlign':'center'})

    return [sched_table]




# Teacher Student List Callback
@app.callback(
    Output('student_studentlist_teacher', 'children'),
    [
        Input('url_admin', 'pathname'),
        Input('sort_column_teacher', 'value'),
        Input('sort_button_teacher', 'n_clicks'),
        Input('student_fnamefilter_teacher', 'value')
    ]
)
def updateRecordsTable(pathname, sort_column, n_clicks, student_fnamefilter):
    print(f"Callback triggered. Pathname: {pathname}, Sort Column: {sort_column}, Filter: {student_fnamefilter}, Clicks: {n_clicks}")

    # Only trigger the callback if the correct path is matched
    if pathname != '/admin':
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
    [Input('url_admin', 'pathname')],
)
def reset_filter(pathname):
    # Reset the filter value only if the correct path is matched
    if pathname == '/admin':
        return ''  # Reset filter to empty on page load or navigation
    raise PreventUpdate  # Prevent update when not on the correct page



if __name__ == '__main__':
    app.run(debug=True)
