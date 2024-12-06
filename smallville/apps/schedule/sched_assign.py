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
            style={'margin-top': '15px'}
        ),
        
        dbc.Card(  # Card Container
            [
                dbc.CardHeader([  # Define Card Header
                    html.H3('Student List'),
                    html.P("View the list of assigned students for the selected schedule below.")
                ]),
                dbc.CardBody(  # Define Card Contents
                    [
                        html.Div(
                            id='sched_assignment'
                        ),
                    ]
                )
            ]
        ),
    ]
)

@app.callback(
    Output('sched_assignment', 'children'),
    [
        Input('url', 'search'),  # Use search to access the query string
    ],
)
def update_records_table(search):
    if not search:  # Ensure the query string exists
        raise PreventUpdate

    # Parse the query string to extract grade_level
    query_params = parse_qs(search.lstrip('?'))  # Strip the leading "?" before parsing
    grade_level = query_params.get('grade_level', [None])[0]

    if not grade_level:  # If grade_level is not provided, don't fetch data
        return html.Div("No grade level specified.")

    # SQL query to fetch filtered student data
    sql = """ 
        SELECT 
            stud_id, stud_fname, stud_lname, stud_gradelvl
        FROM student 
        WHERE stud_gradelvl = %s AND stud_delete_ind = False
    """
    val = [grade_level]  # Use grade_level to filter data

    col = ["Student ID", "First Name", "Last Name", "Grade Level"]

    # Fetch data from the database
    df = getDataFromDB(sql, val, col)
    
    if df.empty:
        return [html.Div("No data available")]
    
    # Exclude 'Student ID' column from display
    df = df[["Grade Level", "First Name", "Last Name"]]

    # Create the table to display the filtered data
    sched_table = dbc.Table.from_dataframe(
        df, striped=True, bordered=True, hover=True, size='sm',
        style={'textAlign': 'center'}
    )

    return [sched_table]

