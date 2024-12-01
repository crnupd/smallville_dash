import dash
import dash_bootstrap_components as dbc
from dash import Output, Input, State, dcc, html
from dash.exceptions import PreventUpdate

from app import app
from apps.dbconnect import getDataFromDB

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
                                # Add student button will work like a 
                                # hyperlink that leads to another page
                                dbc.Button(
                                    "Add Student",
                                    href='/students/student_management_profile?mode=add'
                                )
                            ]
                        ),
                        html.Hr(),
                        html.Div(  # Create section to show list of students
                            [
                                html.H4('Find Students'),
                                html.Div(
                                    dbc.Form(
                                        dbc.Row(
                                            [
                                                dbc.Label("Search First Name", width=1),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='student_fnamefilter',
                                                        placeholder='First Name'
                                                    ),
                                                    width=5
                                                )
                                            ],
                                        )
                                    )
                                ),
                                html.Div(
                                    "Table with students will go here.",
                                    id='student_studentlist'
                                )
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
    ],
    [
        Input('url', 'pathname'),
        Input('student_fnamefilter', 'value'),
    ],
)
def updateRecordsTable(pathname, fnamefilter):

    if pathname == '/students/student_management':
        pass
    else:
        raise PreventUpdate

    sql = """ SELECT stud_id, stud_fname, stud_lname, stud_city, 
                      stud_address, stud_gradelvl 
              FROM student 
              WHERE NOT stud_delete_ind
    """
    val = []

    if fnamefilter:
        sql += """ AND stud_fname ILIKE %s"""
        val += [f'%{fnamefilter}%']
    
    col = ["Student ID", "First Name", "Last Name", "City", "Address", "Grade Level"]

    df = getDataFromDB(sql, val, col)

    df['Action'] = [
        html.Div(
            dbc.Button("Edit", color='warning', size='sm', 
                        href=f'/students/student_management_profile?mode=edit&id={row["stud_id"]}'),
            className='text-center'
        ) for idx, row in df.iterrows()
    ]
    
    # we don't want to display the 'stud_id' column -- let's exclude it
    df = df[['First Name', 'Last Name', 'City', 'Address', 'Grade Level', 'Action']]

    student_table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
                                        hover=True, size='sm')

    
    return [student_table]