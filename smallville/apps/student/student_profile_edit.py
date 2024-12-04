from urllib.parse import parse_qs, urlparse
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html
from dash.exceptions import PreventUpdate

from app import app
from apps.dbconnect import getDataFromDB, modifyDB

layout = html.Div(
    [
        dcc.Store(id='studentprofile_studid', storage_type='memory', data=0),
        
        html.H2('Student Details'),  # Page Header
        html.Hr(),
        dbc.Alert(id='studentprofile_alert', is_open=False),  # For feedback purposes
        
        dbc.Form(
            dbc.Table(
                [
                    # First Name Row
                    html.Tr([
                        html.Td(dbc.Label("First Name"), style={'width': '10%'}),
                        html.Td(
                            dbc.Input(
                                type='text', 
                                id='studentprofile_fname',
                                placeholder="First Name"
                            ),
                            style={'width': '80%'}  # Set the width via style for better alignment
                        ),
                    ]),
                    # Last Name Row
                    html.Tr([
                        html.Td(dbc.Label("Last Name"), style={'width': '10%'}),
                        html.Td(
                            dbc.Input(
                                type='text', 
                                id='studentprofile_lname',
                                placeholder="Last Name"
                            ),
                            style={'width': '80%'}  # Set the width via style for better alignment
                        ),
                    ]),
                    # City Row
                    html.Tr([
                        html.Td(dbc.Label("City"), style={'width': '10%'}),
                        html.Td(
                            dbc.Input(
                                type='text', 
                                id='studentprofile_city',
                                placeholder="City"
                            ),
                            style={'width': '80%'}  # Set the width via style for better alignment
                        ),
                    ]),
                    # Address Row
                    html.Tr([
                        html.Td(dbc.Label("Address"), style={'width': '10%'}),
                        html.Td(
                            dbc.Input(
                                type='text', 
                                id='studentprofile_address',
                                placeholder="Address"
                            ),
                            style={'width': '80%'}  # Set the width via style for better alignment
                        ),
                    ]),
                    # Grade Level Row
                    html.Tr([
                        html.Td(dbc.Label("Grade Level"), style={'width': '10%'}),
                        html.Td(
                            dbc.Input(
                                type='text', 
                                id='studentprofile_gradelvl',
                                placeholder="Grade Level"
                            ),
                            style={'width': '80%'}  # Set the width via style for better alignment
                        ),
                    ]),
                    # Delete Option Row
                    html.Tr([
                        html.Td(dbc.Label("Mark as deleted?"), style={'width': '10%'}),
                        html.Td(
                            dbc.Checklist(
                                id='studentprofile_deleteind',
                                options=[dict(value=1, label="")],
                                value=[]
                            ),
                            style={'width': '80%'}  # Set the width via style for better alignment
                        ),
                    ]),
                ]
            )
        ),
        
        # Ensure the div for studentprofile_deletediv exists
        html.Div(
            id='studentprofile_deletediv',  # Ensure this div exists
            className='d-none'  # Initially hidden, will be shown when needed
        ),

        dbc.Button(
            'Submit',
            id='studentprofile_submit',
            n_clicks=0  # Initialize number of clicks
        ),
        
        dbc.Modal(  # Modal = dialog box; feedback for successful saving.
            [
                dbc.ModalHeader(html.H4('Save Success')),
                dbc.ModalBody('Student details have been saved successfully!'),
                dbc.ModalFooter(dbc.Button("Proceed", href='/student/student_profile'))  # Redirect after saving
            ],
            centered=True,
            id='studentprofile_successmodal',
            backdrop='static'  # Dialog box does not go away if you click at the background
        )
    ]
)

@app.callback(
    [
        Output('studentprofile_deletediv', 'className'),  # Adjust visibility of delete option
        Output('studentprofile_studid', 'data'),
        Output('studentprofile_fname', 'value'),
        Output('studentprofile_lname', 'value'),
        Output('studentprofile_city', 'value'),
        Output('studentprofile_address', 'value'),
        Output('studentprofile_gradelvl', 'value'),
    ],
    [Input('url', 'pathname')],
    [State('url', 'search')]
)
def studentprofile_populate(pathname, urlsearch):
    if pathname == '/student/student_profile_edit':
        parsed = urlparse(urlsearch)
        create_mode = parse_qs(parsed.query).get('mode', [None])[0]
        
        if create_mode == 'add':
            studid = 0
            deletediv = 'd-none'  # Hide delete option when adding a new student
            
            return deletediv, studid, '', '', '', '', ''  # Clear fields for new student
        
        else:
            studid = int(parse_qs(parsed.query).get('id', [0])[0])
            deletediv = ''  # Show delete option when editing an existing student
            
            sql = """
                SELECT stud_fname AS fname,
                       stud_lname AS lname,
                       stud_city AS city,
                       stud_address AS address,
                       stud_gradelvl AS gradelvl
                FROM student WHERE stud_id = %s;
            """
            
            values = [studid]
            col = ['fname', 'lname', 'city', 'address', 'gradelvl']
            
            df = getDataFromDB(sql, values, col)

            return deletediv, studid, df['fname'][0], df['lname'][0], df['city'][0], df['address'][0], df['gradelvl'][0]
    
    else:
        raise PreventUpdate


@app.callback(
    [
        Output('studentprofile_alert', 'color'),
        Output('studentprofile_alert', 'children'),
        Output('studentprofile_alert', 'is_open'),
        Output('studentprofile_successmodal', 'is_open')
    ],
    [Input('studentprofile_submit', 'n_clicks')],
    [
        State('studentprofile_fname', 'value'),
        State('studentprofile_lname', 'value'),
        State('studentprofile_city', 'value'),
        State('studentprofile_address', 'value'),
        State('studentprofile_gradelvl', 'value'),
        State('url', 'search'),
        State('studentprofile_studid', 'data'),
        State('studentprofile_deleteind', 'value'),
    ]
)
def studentprofile_saveprofile(submitbtn, fname, lname, city, address, gradelvl, urlsearch, 
                             studid, deleteind):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        parsed = urlparse(urlsearch)
        create_mode = parse_qs(parsed.query).get('mode', [None])[0]

    else:
        raise PreventUpdate

    if eventid == 'studentprofile_submit' and submitbtn:
        # Set default outputs
        alert_open = False
        modal_open = False
        alert_color = ''
        alert_text = ''

        # Check inputs
        if not fname:  # If first name is blank
            alert_open = True
            alert_color = 'danger'
            alert_text = 'Check your inputs. Please supply the first name.'
        elif not lname:
            alert_open = True
            alert_color = 'danger'
            alert_text = 'Check your inputs. Please supply the last name.'
        elif not city:
            alert_open = True
            alert_color = 'danger'
            alert_text = 'Check your inputs. Please supply the city.'
        elif not address:
            alert_open = True
            alert_color = 'danger'
            alert_text = 'Check your inputs. Please supply the address.'
        elif not gradelvl:
            alert_open = True
            alert_color = 'danger'
            alert_text = 'Check your inputs. Please supply the grade level.'
        
        else:  # All inputs are valid
            # Add or update the data in the db based on mode
            if create_mode == 'add':
                sql = '''
                    INSERT INTO student (stud_fname, stud_lname, stud_city,
                                         stud_address, stud_gradelvl, stud_delete_ind)
                    VALUES (%s, %s, %s, %s, %s, %s)
                '''
                values = [fname, lname, city, address, gradelvl, False]

            elif create_mode == 'edit':
                sql = '''
                    UPDATE student 
                    SET 
                        stud_fname = %s,
                        stud_lname = %s,
                        stud_city = %s,
                        stud_address = %s,
                        stud_gradelvl = %s,
                        stud_delete_ind = %s
                    WHERE
                        stud_id = %s
                '''
                values = [fname, lname, city, address, gradelvl,
                          bool(deleteind), studid]

            else:
                raise PreventUpdate

            modifyDB(sql, values)

            # If this is successful, we want the success modal to show
            modal_open = True

        return [alert_color, alert_text, alert_open, modal_open]

    else: 
        raise PreventUpdate
