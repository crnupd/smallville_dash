import dash
import dash_bootstrap_components as dbc
from dash import Output, Input, State, dcc, html, ALL, ctx
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
                            
                            # Filter Section
                            html.Div(
                                [
                                    html.H4('Filter by Columns'),
                                    html.Div(id='sched-filter-rows-container'),
                                    dbc.Button(
                                        "Add Filter",
                                        id="add-sched-filter-button",
                                        color='primary',
                                        n_clicks=0,
                                        className="mt-2"
                                    ),
                                    html.Hr(),
                                    html.Div(id="sched-list-2")
                                ]
                            ),
                            
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
                                html.H4('Filter by Columns'),
                                html.Div(id='admin-filter-rows-container'),
                                dbc.Button("Add Filter", id="add-filter-button", n_clicks=0, className="mt-2"),

                                html.Hr(),
                                html.Div(id='admin_studentlist')  # Placeholder for student table
                            ]
                        )
                    ]
                )
            ]
            )
        ])

#Schedule Management Sort Callback
@app.callback(
    Output('sched_list', 'children'),
    [
        Input('url', 'pathname'),
        Input('sort_column', 'value'),
        Input('sort_button', 'n_clicks'),
        Input({'type': 'sched-filter-column-dropdown', 'index': ALL}, 'value'),
        Input({'type': 'sched-filter-value-input', 'index': ALL}, 'value')
    ]
)
def updateScheduleTable(pathname, sort_column, sort_clicks, filter_columns, filter_values):
    if pathname != '/admin':
        return [html.Div("This page doesn't exist.")]

    # Start base SQL
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

    # Add filtering logic
    for col, val_filter in zip(filter_columns or [], filter_values or []):
        if col and val_filter:
            sql += f" AND {col} ILIKE %s"
            val.append(f"%{val_filter}%")

    # Determine sorting direction
    if sort_column:
        sort_direction = "ASC" if sort_clicks % 2 == 0 else "DESC"
        sql += f" ORDER BY {sort_column} {sort_direction}"

    # Fetch data from the database
    col_names = ["Grade Level", "Subject", "Teacher", "Schedule", "id"]
    df = getDataFromDB(sql, val, col_names)

    # If no data is found
    if df.empty:
        return [html.Div("No data available")]

    # Add action buttons for editing
    df['Action'] = [
        html.Div(
            dbc.Button(
                "Edit", color='warning', size='sm', 
                href=f'/student/sched_edit?mode=edit&id={row["id"]}'
            ),
            className='text-center'
        ) for _, row in df.iterrows()
    ]

    # Remove ID column
    df = df[["Grade Level", "Subject", "Teacher", "Schedule", "Action"]]

    # Convert DataFrame to a Dash table
    sched_table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')

    return [sched_table]


# Schedule Management Filter Callback
@app.callback(
    Output('sched-filter-rows-container', 'children'),
    [
        Input('add-sched-filter-button', 'n_clicks'),
        Input({'type': 'remove-sched-filter-button', 'index': ALL}, 'n_clicks')
    ],
    State('sched-filter-rows-container', 'children'),
    prevent_initial_call=True
)

def manage_filter_rows(add_clicks, remove_clicks, current_children):
    ctx = dash.callback_context

    # Initialize if None
    if current_children is None:
        current_children = []

    # Add a new filter row
    if ctx.triggered_id == 'add-sched-filter-button':
        new_index = len(current_children)
        
        # Dynamically decide input type for new row
        input_component = dbc.Input(
            type='text',
            id={"type": "sched-filter-value-input", "index": new_index},
            placeholder='Enter filter value',
            style={'margin': '2px 0px'}
        )
        
        # Add a new row
        new_row = dbc.Row(
            id={"type": "sched-filter-row", "index": new_index},
            children=[
                dbc.Col(
                    dcc.Dropdown(
                        id={"type": "sched-filter-column-dropdown", "index": new_index},
                        options=[
                            {'label': 'Grade', 'value': 'grade_level'},
                            {'label': 'Subject', 'value': 'subject'},
                            {'label': 'Teacher', 'value': 'teacher'},
                            {'label': 'Schedule', 'value': 'schedule'}
                        ],
                        placeholder="Select Column",
                        clearable=False,
                        style={'margin': '2px 0px'}
                    ),
                    width=5
                ),
                dbc.Col(input_component, width=5),
                dbc.Col(
                    dbc.Button(
                        "Remove",
                        id={"type": "remove-sched-filter-button", "index": new_index},
                        color="danger",
                        size="sm",
                        className="mt-1"
                    ),
                    width=2
                )
            ],
            className="mb-2"
        )
        
        current_children.append(new_row)
        
        # Handle Remove Filter button click
    elif any(remove_clicks):
        clicked_index = next(
            (i for i, n_clicks in enumerate(remove_clicks) if n_clicks),
            None
        )
        if clicked_index is not None:
            current_children = [
                child for i, child in enumerate(current_children) if i != clicked_index
            ]

    return current_children

def updateSchedTable(pathname, filter_columns, filter_values):
    if pathname != '/admin':
        return html.Div("This page doesn't exist."), ''  # Return empty filter value if path doesn't match

    # SQL query for fetching data
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

    # Apply filter based on the selected column and filter value
    for col, val_filter in zip(filter_columns or [], filter_values or []):
        if col and val_filter:
            sql += f" AND {col} ILIKE %s"
            val.append(f"%{val_filter}%")

    # Columns for the DataFrame
    col_names = ["Grade Level", "Subject", "Teacher", "Schedule", "id"]
    df = getDataFromDB(sql, val, col_names)

    # If no data found, return a message
    if df.empty:
        return html.Div("No data available"), ''
    
    # Add edit action
    df['Action'] = [
        html.Div(
            dbc.Button(
                "Edit",
                color='danger',
                size='sm',
                href=f'/schedule/edit?mode=edit&id={row["id"]}'
            ),
            className='text-center'
        ) for _, row in df.iterrows()
    ]

    # Remove id column from display
    df = df[["Grade Level", "Subject", "Teacher", "Schedule", "Action"]]

    # Convert DataFrame to Dash table
    sched_table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')

    return sched_table

# Teacher Student List Callback
@app.callback(
    Output('admin-filter-rows-container', 'children'),
    [
        Input('add-filter-button', 'n_clicks'),
        Input({'type': 'remove-filter-button', 'index': ALL}, 'n_clicks')
    ],
    State('admin-filter-rows-container', 'children'),
    prevent_initial_call=True
)

def manage_filter_rows(add_clicks, remove_clicks, current_children):
    ctx = dash.callback_context

    # Initialize current_children if None
    if current_children is None:
        current_children = []

    # Handle Add Filter button click
    if ctx.triggered_id == 'add-filter-button':
        new_index = len(current_children)

        # Dynamically decide input type for new row
        input_component = dbc.Input(
            type='text',
            id={"type": "filter-value-input", "index": new_index},
            placeholder='Enter filter value',
            style={'margin': '2px 0px'}
        )

        # Add a new row
        new_row = dbc.Row(
            id={"type": "filter-row", "index": new_index},
            children=[
                dbc.Col(
                    dcc.Dropdown(
                        id={"type": "filter-column-dropdown", "index": new_index},
                        options=[
                            {'label': 'Student ID', 'value': 'stud_id'},
                            {'label': 'Last Name', 'value': 'stud_lname'},
                            {'label': 'City', 'value': 'stud_city'},
                            {'label': 'Address', 'value': 'stud_address'},
                            {'label': 'Grade Level', 'value': 'stud_gradelvl'},
                            {'label': 'Payment Status', 'value': 'pay_status'},
                            {'label': 'Enrollment Status', 'value': 'enroll_status'}
                        ],
                        placeholder="Select Column",
                        clearable=False,
                        style={'margin': '2px 0px'}
                    ),
                    width=5
                ),
                dbc.Col(input_component, width=5),
                dbc.Col(
                    dbc.Button(
                        "Remove",
                        id={"type": "remove-filter-button", "index": new_index},
                        color="danger",
                        size="sm",
                        className="mt-1"
                    ),
                    width=2
                )
            ],
            className="mb-2"
        )

        current_children.append(new_row)

    # Handle Remove Filter button click
    elif any(remove_clicks):
        clicked_index = next(
            (i for i, n_clicks in enumerate(remove_clicks) if n_clicks),
            None
        )
        if clicked_index is not None:
            current_children = [
                child for i, child in enumerate(current_children) if i != clicked_index
            ]

    return current_children


@app.callback(
    Output('admin_studentlist', 'children'),
    [
        Input('url', 'pathname'),
        Input({'type': 'filter-column-dropdown', 'index': ALL}, 'value'),
        Input({'type': 'filter-value-input', 'index': ALL}, 'value')
    ]
)
def updateRecordsTable(pathname, filter_columns, filter_values):
    if pathname != '/admin':
        return html.Div("This page doesn't exist."), ''  # Return empty filter value if path doesn't match

    # SQL query for fetching data
    sql = """
        SELECT 
            student.stud_id AS "Student ID",
            student.stud_fname AS "First Name",
            student.stud_lname AS "Last Name",
            CONCAT(student.stud_city, ', ', student.stud_address) AS "City and Address",
            student.stud_gradelvl AS "Grade Level",
            CASE 
                WHEN SUM(payment.pay_amt) > 0 THEN 'Paid'
                ELSE 'Unpaid'
            END AS "Payment Status",
            COALESCE(SUM(payment.pay_amt), 0) AS "Amount Paid",
            student.enroll_status AS "Enrollment Status"
        FROM student
        LEFT JOIN payment
            ON student.stud_id = payment.stud_id
        WHERE NOT student.stud_delete_ind
        GROUP BY 
            student.stud_id, student.stud_fname, student.stud_lname, student.stud_city, student.stud_address, student.stud_gradelvl, student.enroll_status;
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
            elif col == 'pay_status':
                if val_filter == 'Paid':
                    sql += " AND pay_status = TRUE"
                elif val_filter == 'Unpaid':
                    sql += " AND pay_status = FALSE"
            elif col == 'stud_id':
                sql += " AND stud_id = %s"
                val.append(f'{val_filter}')
            else:
                sql += f" AND {col} ILIKE %s"
                val.append(f'%{val_filter}%')

    # Columns for the DataFrame
    col = ["Student ID", "First Name", "Last Name", "City and Address", "Grade Level", "Payment Status", "Amount Paid", "Enrollment Status"]

    # Fetch data from the database
    df = getDataFromDB(sql, val, col)

    # If no data found, return a message
    if df.empty:
        return html.Div("No data available"), ''
    
    # Replace enroll_status True/False values with 'Enrolled'/'Not Enrolled'
    df['Enrollment Status'] = df['Enrollment Status'].apply(lambda x: 'Enrolled' if x else 'Not Enrolled')

    #Format amount values with commas 
    df["Amount Paid"] = df["Amount Paid"].apply(lambda x: f"{x:,.2f}")

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
    df = df[["Student ID", "First Name", "Last Name", "City and Address", "Grade Level", "Payment Status", "Amount Paid", "Enrollment Status", 'Action']]

    # Generate the table from DataFrame
    student_table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')

    # Return the updated table
    return student_table

if __name__ == '__main__':
    app.run(debug=True)
