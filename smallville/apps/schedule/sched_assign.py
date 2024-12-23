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
        
        dbc.Card( 
            [
                dbc.CardHeader([ 
                    html.H3('Student List'),
                    html.P("View the list of assigned students for the selected schedule below.")
                ]),
                dbc.CardBody( 
                    [
                        html.H5("Search for students:"),
                        
                        dbc.Row([  
                            dbc.Col(  
                                dbc.Input(
                                    id='first_name_filter', 
                                    placeholder="Enter first name to filter...", 
                                    type="text"
                                ),
                                width=6,  
                            ),
                            dbc.Col(  
                                dbc.Input(
                                    id='last_name_filter', 
                                    placeholder="Enter last name to filter...", 
                                    type="text"
                                ),
                                width=6,  
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
        Input('url', 'search'),  
        Input('first_name_filter', 'value'),  
        Input('last_name_filter', 'value'),   
    ],
)
def update_records_table(search, first_name_filter, last_name_filter):
    if not search:  
        raise PreventUpdate

    
    query_params = parse_qs(search.lstrip('?')) 
    grade_level = query_params.get('grade_level', [None])[0]

    if not grade_level:  
        return html.Div("No grade level specified.")
    
    sql = """ 
        SELECT 
            stud_id, stud_fname, stud_lname, stud_gradelvl
        FROM student 
        WHERE stud_gradelvl = %s AND stud_delete_ind = False AND enroll_status = True
    """
    val = [grade_level] 

    if first_name_filter:
        sql += """ AND stud_fname ILIKE %s"""
        val += [f'%{first_name_filter}%']
    
    if last_name_filter:
        sql += """ AND stud_lname ILIKE %s"""
        val += [f'%{last_name_filter}%']

    col = ["Student ID", "First Name", "Last Name", "Grade Level"]

    df = getDataFromDB(sql, val, col)
    
    if df.empty:
        return [html.Div("No data available")]
    
    df = df[["Grade Level", "First Name", "Last Name"]]

    # create the table to display the filtered data
    sched_table = dbc.Table.from_dataframe(
        df, striped=True, bordered=True, hover=True, size='sm',
        style={'textAlign': 'center'}
    )

    return [sched_table]