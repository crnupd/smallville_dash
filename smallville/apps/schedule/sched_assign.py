import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html
from dash.exceptions import PreventUpdate
from urllib.parse import parse_qs

from app import app
from apps.dbconnect import getDataFromDB

layout = html.Div(
    [
        html.Div(
            [
                html.H2('Student Assignment'),
                html.Hr(),
            ],
            style={'margin-top': '70px'}
        ),
        
        dbc.Card(  # Card Container
            [
                dbc.CardHeader([  # Define Card Header
                    html.H3('Student List'),
                    html.P("View the list of assigned students for the selected schedule below.")
                ]),
                dbc.CardBody(  # Define Card Contents
                    [
                        html.H5("Search for students:"),
                        
                        dbc.Row([  # Row to hold side-by-side filters
                            dbc.Col(  # Left Column for First Name filter
                                dbc.Input(
                                    id='first_name_filter', 
                                    placeholder="Enter first name to filter...", 
                                    type="text"
                                ),
                                width=6,  # Set column width
                            ),
                            dbc.Col(  # Right Column for Last Name filter
                                dbc.Input(
                                    id='last_name_filter', 
                                    placeholder="Enter last name to filter...", 
                                    type="text"
                                ),
                                width=6,  # Set column width
                            ),
                        ], style={'margin-top': '10px', 'margin-bottom':'10px'}),
                        
                        html.Div(
                            id='sched_assignment'
                        ),
                    ]
                ),
                dbc.Button(
                    "Back",
                    href = "/student/student_sched",
                    className="mb-2",
                    style={"width":"50%", "marginLeft":"auto", "marginRight":"auto", "textAlign":"center"},
                ),
                
                html.Br(),
            ]
        ),
    ]
)

@app.callback(
    Output('sched_assignment', 'children'),
    [
        Input('url', 'search'),  # Use search to access the query string
        Input('first_name_filter', 'value'),  # First Name filter
        Input('last_name_filter', 'value'),   # Last Name filter
    ],
)
def update_records_table(search, first_name_filter, last_name_filter):
    if not search:  # Ensure the query string exists
        raise PreventUpdate

    # Parse the query string to extract grade_level
    query_params = parse_qs(search.lstrip('?'))  # Strip the leading "?" before parsing
    grade_level = query_params.get('grade_level', [None])[0]

    if not grade_level:  # If grade_level is not provided, don't fetch data
        return html.Div("No grade level specified.")
    
    sql = """ 
        SELECT 
            stud_id, stud_fname, stud_lname, stud_gradelvl
        FROM student 
        WHERE stud_gradelvl = %s AND stud_delete_ind = False
    """
    val = [grade_level]  # Start with grade_level filter

    # Apply additional filters for first name if provided
    if first_name_filter:
        sql += """ AND stud_fname ILIKE %s"""
        val += [f'%{first_name_filter}%']
    
    # Apply additional filters for last name if provided
    if last_name_filter:
        sql += """ AND stud_lname ILIKE %s"""
        val += [f'%{last_name_filter}%']

    col = ["Student ID", "First Name", "Last Name", "Grade Level"]

    # Fetch data from the database
    df = getDataFromDB(sql, val, col)
    
    if df.empty:
        return [html.Div("No data available")]
    
    # Exclude 'Student ID' column from display
    df = df[["First Name", "Last Name"]]

    # Create the table to display the filtered data
    sched_table = dbc.Table.from_dataframe(
        df, striped=True, bordered=True, hover=True, size='sm',
        style={'textAlign': 'center'}
    )

    return [sched_table]