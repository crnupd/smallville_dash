import dash
import dash_bootstrap_components as dbc
from dash import Output, Input, State, dcc, html, ALL
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
                dbc.CardBody(
                    [
                        html.Hr(),
                        html.Div(
                            [
                                html.H4('Filter by Other Columns'),
                                html.Div(id='filter-rows-container'),
                                dbc.Button("Add Filter", id="add-filter-button", n_clicks=0, className="mt-2"),
                                html.Hr(),
                                html.H4('Filter by Last Name'),
                                dbc.Row([
                                    dbc.Col(
                                        dbc.Input(
                                            type='text',
                                            id='admin_student_lnamefilter',
                                            placeholder='Filter by Last Name',
                                            value=''
                                        ),
                                        width=12
                                    )
                                ]),
                                html.Hr(),
                                html.Div(id='admin_studentlist')  # Placeholder for student table
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
    Output('admin-filter-rows-container', 'children'),
    Input('add-filter-button', 'n_clicks'),
    State('admin-filter-rows-container', 'children'),
    prevent_initial_call=True
)
def add_filter_row(n_clicks, current_children):
    if n_clicks is None:
        raise PreventUpdate


    if current_children is None:
        current_children = []


    new_index = len(current_children) // 2


    # Check if any existing filter dropdown already selects 'enroll_status'
    enroll_status_filter_exists = any(
        isinstance(child, dbc.Row) and
        len(child.children) > 0 and
        isinstance(child.children[0], dbc.Col) and
        isinstance(child.children[0].children, dcc.Dropdown) and
        child.children[0].children.value == 'enroll_status'
        for child in current_children
    )


    # Dynamically decide input type for new row
    input_component = (
        dcc.Dropdown(
            id={"type": "filter-value-input", "index": new_index},
            options=[
                {'label': 'Enrolled', 'value': 'Enrolled'},
                {'label': 'Not Enrolled', 'value': 'Not Enrolled'}
            ],
            placeholder='Select filter value',
            style={'margin': '2px 0px'}
        ) if enroll_status_filter_exists else
        dbc.Input(
            type='text',
            id={"type": "filter-value-input", "index": new_index},
            placeholder='Enter filter value',
            value='',
            style={'margin': '2px 0px'}
        )
    )


    # Add the new row
    new_row = dbc.Row(
        [
            dbc.Col(
                dcc.Dropdown(
                    id={"type": "filter-column-dropdown", "index": new_index},
                    options=[
                        {'label': 'Student ID', 'value': 'stud_id'},
                        {'label': 'City', 'value': 'stud_city'},
                        {'label': 'Grade Level', 'value': 'stud_gradelvl'},
                        {'label': 'Enrollment Status', 'value': 'enroll_status'}
                    ],
                    placeholder="Select Column",
                    clearable=False,
                    style={'margin': '2px 0px'}
                ),
                width=6
            ),
            dbc.Col(
                input_component,
                width=6
            )
        ],
        className="mb-2"
    )


    current_children.append(new_row)
    return current_children



@app.callback(
    [
        Output('admin_studentlist', 'children'),
        Output('admin_student_lnamefilter', 'value')
    ],
    [
        Input('url', 'pathname'),
        Input({'type': 'filter-column-dropdown', 'index': ALL}, 'value'),
        Input({'type': 'filter-value-input', 'index': ALL}, 'value'),
        Input('admin_student_lnamefilter', 'value')
    ]
)
def updateRecordsTable(pathname, filter_columns, filter_values, admin_student_lnamefilter):
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
    for col, val_filter in zip(filter_columns or [], filter_values or []):
        if col and val_filter:
            if col == 'enroll_status':
                if val_filter == 'Enrolled':
                    sql += " AND enroll_status = TRUE"
                elif val_filter == 'Not Enrolled':
                    sql += " AND enroll_status = FALSE"
            else:
                sql += f" AND {col} ILIKE %s"
                val.append(f'%{val_filter}%')


    if admin_student_lnamefilter:
        sql += " AND stud_lname ILIKE %s"
        val.append(f'%{admin_student_lnamefilter}%')

    # Columns for the DataFrame
    col = ["Student ID", "First Name", "Last Name", "City", "Address", "Grade Level", "Enrollment Status"]

    # Fetch data from the database
    df = getDataFromDB(sql, val, col)

    # If no data found, return a message
    if df.empty:
        return html.Div("No data available"), admin_student_lnamefilter
    
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
    return student_table, admin_student_lnamefilter

if __name__ == '__main__':
    app.run(debug=True)
