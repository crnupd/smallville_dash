import dash
import dash_bootstrap_components as dbc
from dash import Output, Input, State, dcc, html, ALL, ctx
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
                dbc.CardHeader(
                    dbc.Row(
                        [
                            dbc.Col(html.H3('Manage Records'), width=10),
                            dbc.Col(
                                dbc.Button(
                                    "Add Student",
                                    href='/student/student_profile_edit?mode=add',
                                    color='primary',
                                    style={'float': 'right'}
                                ),
                                width=2,
                                className="text-right"
                            ),
                        ],
                        justify="between",
                        align="center",
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
                                            id='student_lnamefilter',
                                            placeholder='Filter by Last Name',
                                            value=''
                                        ),
                                        width=12
                                    )
                                ]),
                                html.Hr(),
                                html.Div(id='student_studentlist')
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)


@app.callback(
    Output('filter-rows-container', 'children'),
    [
        Input('add-filter-button', 'n_clicks'),
        Input({'type': 'remove-filter-button', 'index': ALL}, 'n_clicks')
    ],
    State('filter-rows-container', 'children'),
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
                            {'label': 'City', 'value': 'stud_city'},
                            {'label': 'Address', 'value': 'stud_address'},
                            {'label': 'Grade Level', 'value': 'stud_gradelvl'},
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
    [
        Output('student_studentlist', 'children'),
        Output('student_lnamefilter', 'value')
    ],
    [
        Input('url', 'pathname'),
        Input({'type': 'filter-column-dropdown', 'index': ALL}, 'value'),
        Input({'type': 'filter-value-input', 'index': ALL}, 'value'),
        Input('student_lnamefilter', 'value')
    ],
    [
        State('currentuserid', 'data')
    ]
)
def updateRecordsTable(pathname, filter_columns, filter_values, student_lnamefilter, currentuserid):
    if pathname != '/student/student_profile':
        return html.Div("This page doesn't exist."), ''
    
    if not currentuserid or currentuserid <= 0:
        return html.Div("Please log in to view this page."), ''


    sql = """
        SELECT
            stud_id::text AS "Student ID",
            stud_fname AS "First Name",
            stud_lname AS "Last Name",
            stud_city AS "City",
            stud_address AS "Address",
            stud_gradelvl AS "Grade Level",
            enroll_status AS "Enrollment Status"
        FROM student
        WHERE NOT stud_delete_ind
        AND user_id = %s
    """
    val = [currentuserid]


    for col, val_filter in zip(filter_columns or [], filter_values or []):
        if col and val_filter:
            if col == 'enroll_status':
                if val_filter == 'Enrolled':
                    sql += " AND enroll_status = TRUE"
                elif val_filter == 'Not Enrolled':
                    sql += " AND enroll_status = FALSE"
            elif col == 'stud_id':
                sql += " AND stud_id = %s"
                val.append(f'{val_filter}')
            else:
                sql += f" AND {col} ILIKE %s"
                val.append(f'%{val_filter}%')


    if student_lnamefilter:
        sql += " AND stud_lname ILIKE %s"
        val.append(f'%{student_lnamefilter}%')


    col = ["Student ID", "First Name", "Last Name", "City", "Address", "Grade Level", "Enrollment Status"]


    df = getDataFromDB(sql, val, col)


    if df.empty:
        return html.Div("No data available"), student_lnamefilter


    df['Enrollment Status'] = df['Enrollment Status'].apply(lambda x: 'Enrolled' if x else 'Not Enrolled')


    df['Action'] = [
        html.Div(
            dbc.Button(
                "Edit",
                style={'backgroundColor': 'Maroon', 'color': 'white'},
                size='sm',
                href=f'/student/student_profile_edit?mode=edit&id={row["Student ID"]}'
            ),
            className='text-center'
        ) for _, row in df.iterrows()
    ]


    df = df[["Student ID", "First Name", "Last Name", "City", "Address", "Grade Level", "Enrollment Status", 'Action']]
   
    student_table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')


    return student_table, student_lnamefilter
