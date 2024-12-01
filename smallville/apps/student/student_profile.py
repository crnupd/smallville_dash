import dash
import dash_bootstrap_components as dbc
from dash import Output, Input, html
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
                                dbc.Button(
                                    "Add Student",
                                    href='/students/student_profile_edit?mode=add'
                                )
                            ]
                        ),
                        html.Hr(),
                        html.Div(  # Create section to show list of students
                            [
                                html.H4('Find Students'),
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
                                ),
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
    [Input('url', 'pathname'), Input('student_fnamefilter', 'value')]
)
def updateRecordsTable(pathname, fnamefilter):
    if pathname != '/students/student_profile':  # Corrected pathname check
        raise PreventUpdate

    sql = """ 
        SELECT stud_id, stud_fname, stud_lname, stud_city, 
               stud_address, stud_gradelvl 
        FROM student 
        WHERE NOT stud_delete_ind
    """
    val = []

    if fnamefilter:
        sql += " AND stud_fname ILIKE %s"
        val.append(f'%{fnamefilter}%')

    col = ["Student ID", "First Name", "Last Name", "City", "Address", "Grade Level"]

    df = getDataFromDB(sql, val, col)

    if df.empty:
        return html.Div("No records found.")  # Provide feedback if no records exist

    df['Action'] = [
        html.Div(
            dbc.Button("Edit", color='warning', size='sm', 
                        href=f'/students/student_profile_edit?mode=edit&id={row["stud_id"]}'),
            className='text-center'
        ) for idx, row in df.iterrows()
    ]

    # Exclude 'stud_id' from display
    df = df[['stud_fname', 'stud_lname', 'stud_city', 'stud_address', 'stud_gradelvl', 'Action']]

    student_table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
                                              hover=True, size='sm')

    return [student_table]  # Return the generated table directly
