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
                            style={'width': '80%'}
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
                            style={'width': '80%'}
                        ),
                    ]),
                    # Age Row
                    html.Tr([
                        html.Td(dbc.Label("Age"), style={'width': '10%'}),
                        html.Td(
                            dbc.Input(
                                type='number', 
                                id='studentprofile_age',
                                placeholder="Age"
                            ),
                            style={'width': '80%'}
                        ),
                    ]),
                    # Gender Row
                    html.Tr([
                        html.Td(dbc.Label("Gender"), style={'width': '10%'}),
                        html.Td(
                            dcc.Dropdown(
                                id='studentprofile_gender',
                                options=[
                                    {'label': 'Male', 'value': 'Male'},
                                    {'label': 'Female', 'value': 'Female'},
                                    {'label': 'Prefer not to say', 'value': 'Prefer not to say'},
                                ],
                                value='Prefer not to say',  # Default value
                                style={'width': '80%'}
                            )
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
                            style={'width': '80%'}
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
                            style={'width': '80%'}
                        ),
                    ]),
                    # Grade Level Row
                    html.Tr([
                        html.Td(dbc.Label("Grade Level"), style={'width': '10%'}),
                        html.Td(
                            dcc.Dropdown(
                                id='studentprofile_gradelvl',
                                options=[
                                    {'label': 'Kindergarten', 'value': 'Kindergarten'},
                                    {'label': 'Pre-school', 'value': 'Pre-school'},
                                    {'label': 'Grade 1', 'value': 'Grade 1'},
                                    {'label': 'Grade 2', 'value': 'Grade 2'},
                                    {'label': 'Grade 3', 'value': 'Grade 3'},
                                    {'label': 'Grade 4', 'value': 'Grade 4'},
                                    {'label': 'Grade 5', 'value': 'Grade 5'},
                                    {'label': 'Grade 6', 'value': 'Grade 6'},
                                ],
                                value='Kindergarten',  # Default value
                                style={'width': '80%'}
                            )
                        ),
                    ]),
                    # Parent First Name Row
                    html.Tr([
                        html.Td(dbc.Label("Parent First Name"), style={'width': '10%'}),
                        html.Td(
                            dbc.Input(
                                type='text', 
                                id='studentprofile_parent_fname',
                                placeholder="Parent First Name"
                            ),
                            style={'width': '80%'}
                        ),
                    ]),
                    # Parent Email Row
                    html.Tr([
                        html.Td(dbc.Label("Parent Email"), style={'width': '10%'}),
                        html.Td(
                            dbc.Input(
                                type='email', 
                                id='studentprofile_parent_email',
                                placeholder="Parent Email"
                            ),
                            style={'width': '80%'}
                        ),
                    ]),
                    # Parent Job Row
                    html.Tr([
                        html.Td(dbc.Label("Parent Job"), style={'width': '10%'}),
                        html.Td(
                            dbc.Input(
                                type='text', 
                                id='studentprofile_parent_job',
                                placeholder="Parent Job"
                            ),
                            style={'width': '80%'}
                        ),
                    ]),
                    # Relationship Row
                    html.Tr([
                        html.Td(dbc.Label("Relationship"), style={'width': '10%'}),
                        html.Td(
                            dcc.Dropdown(
                                id='studentprofile_relationship',
                                options=[
                                    {'label': 'Mother', 'value': 'Mother'},
                                    {'label': 'Father', 'value': 'Father'},
                                    {'label': 'Guardian', 'value': 'Guardian'},
                                ],
                                value='Mother',  # Default value
                                style={'width': '80%'}
                            )
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
                            style={'width': '80%'}
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
        Output('studentprofile_age', 'value'),
        Output('studentprofile_gender', 'value'),
        Output('studentprofile_city', 'value'),
        Output('studentprofile_address', 'value'),
        Output('studentprofile_gradelvl', 'value'),
        Output('studentprofile_parent_fname', 'value'),
        Output('studentprofile_parent_email', 'value'),
        Output('studentprofile_parent_job', 'value'),
        Output('studentprofile_relationship', 'value'),
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
            
            # Return default values for a new student, ensuring all 13 fields are accounted for
            return deletediv, studid, '', '', '', 'Prefer not to say', '', '', 'Kindergarten', '', '', 'Mother'
        
        else:
            studid = int(parse_qs(parsed.query).get('id', [0])[0])
            deletediv = ''  # Show delete option when editing an existing student
            
            sql = """
                SELECT stud_fname AS fname,
                       stud_lname AS lname,
                       stud_age AS age,
                       stud_gender AS gender,
                       stud_city AS city,
                       stud_address AS address,
                       stud_gradelvl AS gradelvl,
                       parent_fname AS parent_fname,
                       parent_email AS parent_email,
                       parent_job AS parent_job,
                       relationship AS relationship
                FROM student WHERE stud_id = %s;
            """
            
            values = [studid]
            col = ['fname', 'lname', 'age', 'gender', 'city', 'address', 'gradelvl', 
                   'parent_fname', 'parent_email', 'parent_job', 'relationship']
            
            df = getDataFromDB(sql, values, col)

            # Ensure all 13 fields are returned even when editing an existing student
            return deletediv, studid, df['fname'][0], df['lname'][0], df['age'][0], df['gender'][0], df['city'][0], df['address'][0], df['gradelvl'][0], df['parent_fname'][0], df['parent_email'][0], df['parent_job'][0], df['relationship'][0]
    
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
        State('studentprofile_age', 'value'),
        State('studentprofile_gender', 'value'),
        State('studentprofile_city', 'value'),
        State('studentprofile_address', 'value'),
        State('studentprofile_gradelvl', 'value'),
        State('studentprofile_parent_fname', 'value'),
        State('studentprofile_parent_email', 'value'),
        State('studentprofile_parent_job', 'value'),
        State('studentprofile_relationship', 'value'),
        State('url', 'search'),
        State('studentprofile_studid', 'data'),
        State('studentprofile_deleteind', 'value'),
    ]
)
def studentprofile_saveprofile(submitbtn, fname, lname, age, gender, city, address, gradelvl, parent_fname, parent_email, parent_job, relationship, urlsearch, studid, deleteind):
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
                    INSERT INTO student (stud_fname, stud_lname, stud_age, stud_gender, stud_city,
                                         stud_address, stud_gradelvl, parent_fname, parent_email,
                                         parent_job, relationship, stud_delete_ind)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                '''
                values = [fname, lname, age, gender, city, address, gradelvl, parent_fname, parent_email, parent_job, relationship, False]

            elif create_mode == 'edit':
                sql = '''
                    UPDATE student 
                    SET 
                        stud_fname = %s,
                        stud_lname = %s,
                        stud_age = %s,
                        stud_gender = %s,
                        stud_city = %s,
                        stud_address = %s,
                        stud_gradelvl = %s,
                        parent_fname = %s,
                        parent_email = %s,
                        parent_job = %s,
                        relationship = %s,
                        stud_delete_ind = %s
                    WHERE
                        stud_id = %s
                '''
                values = [fname, lname, age, gender, city, address, gradelvl, parent_fname, parent_email, parent_job, relationship,
                          bool(deleteind), studid]

            else:
                raise PreventUpdate

            modifyDB(sql, values)

            # If this is successful, we want the success modal to show
            modal_open = True

        return [alert_color, alert_text, alert_open, modal_open]

    else: 
        raise PreventUpdate
