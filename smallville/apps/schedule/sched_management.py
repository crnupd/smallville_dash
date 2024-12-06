import dash
import dash_bootstrap_components as dbc
from dash import Output, Input, State, dcc, html
from dash.exceptions import PreventUpdate
import pandas as pd
from dash import dash_table

from app import app
from apps.dbconnect import getDataFromDB

layout = html.Div(
    [
        html.Div(
            [
                html.H2('Schedule Management'), # Page Header
                html.Hr(),
            ],
            style={'margin-top': '15px'}
        ),
        
        dbc.Card( # Card Container
            [
                dbc.CardHeader(  # Define Card Header
                    dbc.Row(  # Use Row to align text and button
                        [
                            dbc.Col(
                                [
                                html.H3('Manage Schedules'),
                                html.P("Use this page to view and manage the class schedules.")
                                ],
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
    if pathname != '/student/sched_management':
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
    WHERE TRUE
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