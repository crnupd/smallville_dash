from urllib.parse import parse_qs, urlparse
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html
from dash.exceptions import PreventUpdate

from datetime import date

from app import app
from apps.dbconnect import getDataFromDB, modifyDB


layout = html.Div(
    [
        dcc.Store(id='studentprofile_studid', storage_type='memory', data=0),

        # Header and Return Button
        dbc.Row(
            [
                dbc.Col(
                    html.H2(
                        'Student and Parent Details', 
                        style={'width': "100%", 'color': '#000'}
                    ),
                    width=10
                ),  # Page Header
                dbc.Col(
                    dbc.Button(
                        "Return",
                        color='primary',
                        href=f'/student/student_profile',
                        # style={'background-color': '#004085', 'color': '#fff', 'font-weight': 'bold'}
                    ),
                    width=2,
                    className="text-end"  # Aligns the button to the right
                )
            ],
            align="center",
            style={'margin-bottom': '20px'}
        ),

        html.Hr(style={'border-top': '3px solid #343a40'}),  # Darker and thicker separator
        dbc.Alert(id='studentprofile_alert', is_open=False),  # For feedback purposes

        dbc.Row(
            [
                # Left Column: Student Details
                dbc.Col(
                    [
                        html.H3(
                            'Student Details',
                            style={'color': '#004085', 'margin-bottom': '15px'}
                        ),
                        dbc.Form(
                            dbc.Table(
                                [
                                    # First Name Row
                                    html.Tr([
                                        html.Td(
                                            html.Div([
                                                dbc.Label(
                                                    "First Name",
                                                    style={'display': 'block', 'margin-bottom': '5px', 'color': '#000'}
                                                ),
                                                dbc.Input(
                                                    type='text',
                                                    id='studentprofile_fname',
                                                    placeholder="First Name",
                                                    style={'width': '100%', 'border': '2px solid #CCCECF'}
                                                ),
                                            ]),
                                        ),
                                    ]),

                                    # Last Name Row
                                    html.Tr([
                                        html.Td(
                                            html.Div([
                                                dbc.Label(
                                                    "Last Name",
                                                    style={'display': 'block', 'margin-bottom': '5px', 'color': '#000'}
                                                ),
                                                dbc.Input(
                                                    type='text',
                                                    id='studentprofile_lname',
                                                    placeholder="Last Name",
                                                    style={'width': '100%', 'border': '2px solid #CCCECF'}
                                                ),
                                            ]),
                                        ),
                                    ]),

                                    # Age Row
                                  html.Tr([
        html.Td(
            html.Div([
                dbc.Label(
                    "Date of Birth",
                    style={'display': 'block', 'margin-bottom': '5px', 'color': '#000'}
                ),
                dbc.Input(
                    type='date',
                    id='studentprofile_bdate',
                    placeholder="Date of Birth",
                    style={'width': '100%', 'border': '2px solid #CCCECF'}
                ),
            ])
        )
    ]),
    html.Tr([
        html.Td(
            html.Div([
                dbc.Label(
                    "Age",
                    style={'display': 'block', 'margin-bottom': '5px', 'color': '#000'}
                ),
                dbc.Input(
                    type='number',
                    id='studentprofile_age',
                    placeholder="Age",
                    style={'width': '100%', 'border': '2px solid #CCCECF'},
                    readonly=True  # Make age field read-only
                ),
            ]),
        ),
    ]),
                                    # Gender Row
                                    html.Tr([
                                        html.Td(
                                            html.Div([
                                                dbc.Label(
                                                    "Gender",
                                                    style={'display': 'block', 'margin-bottom': '5px', 'color': '#000'}
                                                ),
                                                dbc.RadioItems(
                                                    id='studentprofile_gender',
                                                    options=[
                                                        {'label': 'Prefer not to say', 'value': 'Prefer not to say'},
                                                        {'label': 'Male', 'value': 'Male'},
                                                        {'label': 'Female', 'value': 'Female'},
                                                    ],
                                                    value='Prefer not to say',
                                                    style={'color': '#000'}
                                                ),
                                            ]),
                                        ),
                                    ]),

                                    # City Row
                                    html.Tr([
                                        html.Td(
                                            html.Div([
                                                dbc.Label(
                                                    "City",
                                                    style={'display': 'block', 'margin-bottom': '5px', 'color': '#000'}
                                                ),
                                                dbc.Input(
                                                    type='text',
                                                    id='studentprofile_city',
                                                    placeholder="City",
                                                    style={'width': '100%', 'border': '2px solid #CCCECF'}
                                                ),
                                            ]),
                                        ),
                                    ]),

                                    # Address Row
                                    html.Tr([
                                        html.Td(
                                            html.Div([
                                                dbc.Label(
                                                    "Address",
                                                    style={'display': 'block', 'margin-bottom': '5px', 'color': '#000'}
                                                ),
                                                dbc.Input(
                                                    type='text',
                                                    id='studentprofile_address',
                                                    placeholder="Address",
                                                    style={'width': '100%', 'border': '2px solid #CCCECF'}
                                                ),
                                            ]),
                                        ),
                                    ]),

                                    # Grade Level Row
                                    html.Tr([
                                        html.Td(
                                            html.Div([
                                                dbc.Label(
                                                    "Grade Level",
                                                    style={'display': 'block', 'margin-bottom': '5px', 'color': '#000'}
                                                ),
                                                dbc.Select(
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
                                                    value='Kindergarten',
                                                    style={'width': '100%', 'border': '2px solid #CCCECF'}
                                                ),
                                            ]),
                                        ),
                                    ]),
                                ],
                                style={'table-layout': 'fixed', 'width': '100%', 'background-color': '#e9ecef'}
                            )
                        ),
                    ],
                    width=6,
                    style={
                        'border-right': '3px solid #CCCECF',
                        'padding-right': '15px',
                        'margin-bottom': '20px'
                    }
                ),

                # Right Column: Parent Details
                dbc.Col(
                    [
                        html.H3(
                            'Parent Details',
                            style={'color': '#004085',  'margin-bottom': '15px'}
                        ),
                        dbc.Form(
                            dbc.Table(
                                [
                                    # Parent Full Name Row
                                    html.Tr([
                                        html.Td(
                                            html.Div([
                                                dbc.Label(
                                                    "Parent Full Name",
                                                    style={'display': 'block', 'margin-bottom': '5px', 'color': '#000'}
                                                ),
                                                dbc.Input(
                                                    type='text',
                                                    id='studentprofile_parent_fname',
                                                    placeholder="Parent Full Name",
                                                    style={'width': '100%', 'border': '2px solid #CCCECF'}
                                                ),
                                            ]),
                                        ),
                                    ]),

                                    # Contact Number Row
                                    html.Tr([
                                        html.Td(
                                            html.Div([
                                                dbc.Label(
                                                    "Contact Number",
                                                    style={'display': 'block', 'margin-bottom': '5px', 'color': '#000'}
                                                ),
                                                dbc.Input(
                                                    type='text',
                                                    id='studentprofile_parent_contact',
                                                    placeholder="Contact Number",
                                                    style={'width': '100%', 'border': '2px solid #CCCECF'}
                                                ),
                                            ]),
                                        ),
                                    ]),

                                    # Parent Email Row
                                    html.Tr([
                                        html.Td(
                                            html.Div([
                                                dbc.Label(
                                                    "Parent Email",
                                                    style={'display': 'block', 'margin-bottom': '5px', 'color': '#000'}
                                                ),
                                                dbc.Input(
                                                    type='text',
                                                    id='studentprofile_parent_email',
                                                    placeholder="Parent Email",
                                                    style={'width': '100%', 'border': '2px solid #CCCECF'}
                                                ),
                                            ]),
                                        ),
                                    ]),

                                    # Parent Job Row
                                    html.Tr([
                                        html.Td(
                                            html.Div([
                                                dbc.Label(
                                                    "Parent Job",
                                                    style={'display': 'block', 'margin-bottom': '5px', 'color': '#000'}
                                                ),
                                                dbc.Input(
                                                    type='text',
                                                    id='studentprofile_parent_job',
                                                    placeholder="Parent Job",
                                                    style={'width': '100%', 'border': '2px solid #CCCECF'}
                                                ),
                                            ]),
                                        ),
                                    ]),

                                    # Relationship Row
                                    html.Tr([
                                        html.Td(
                                            html.Div([
                                                dbc.Label(
                                                    "Relationship",
                                                    style={'display': 'block', 'margin-bottom': '5px', 'color': '#000'}
                                                ),
                                                dbc.RadioItems(
                                                    id='studentprofile_relationship',
                                                    options=[
                                                        {'label': 'Mother', 'value': 'Mother'},
                                                        {'label': 'Father', 'value': 'Father'},
                                                        {'label': 'Guardian', 'value': 'Guardian'},
                                                    ],
                                                    value='Guardian',
                                                    style={'color': '#000'}
                                                ),
                                            ]),
                                        ),
                                    ]),
                                ],
                                style={'table-layout': 'fixed', 'width': '100%', 'background-color': '#e9ecef'}
                            )
                        ),
                    ],
                    width=6,
                    style={'padding-left': '15px'}
                ),
            ],
            style={'margin-bottom': '20px'}
        ),

        # Mark as Deleted Outside
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        dbc.Label(
                            "Mark as deleted?", 
                            html_for='studentprofile_deleteind',
                            style={'margin-right': '20px', 'color': '#000', 'margin-left': '20px'}
                        ),
                        dbc.Checklist(
                            id='studentprofile_deleteind',
                            options=[dict(value=1, label="")],
                            value=[],
                            style={'display': 'inline-block'}
                        ),
                    ],
                    style={
                        'display': 'flex',
                        'align-items': 'center',
                        'background-color': '#f8d7da',
                        'padding': '10px',
                        'border-radius': '5px',
                        'border': '2px solid #CCCECF'
                    }
                ),
                 width=2
            )
        ),

        html.Div(
            id='studentprofile_deletediv',
            className='d-none',
            style={'margin-bottom': '7px'}
        ),

        dbc.Button(
            'Submit',
            id='studentprofile_submit',
            n_clicks=0,
            style={
                'background-color': '#218838',
                'color': '#fff',
                'border': '2px solid #155724',
                'margin-top': '15px',
                'font-weight': 'bold'
            }
        ),

        dbc.Modal(
            [
                dbc.ModalHeader(html.H4('Save Success')),
                dbc.ModalBody('Student details have been saved successfully!'),
                dbc.ModalFooter(
                    dbc.Button(
                        "Proceed",
                        href='/student/student_profile',
                        style={'background-color': '#004085', 'color': '#fff', 'font-weight': 'bold'}
                    )
                )
            ],
            centered=True,
            id='studentprofile_successmodal',
            backdrop='static'
        )
    ],
    style={
        'background-color': '#ffffff',
        'color': '#212529',
        'padding': '20px',
        'border-radius': '10px',
        'box-shadow': '0px 4px 6px rgba(0, 0, 0, 0.2)'
    }
)



# The rest of the code remains unchanged


@app.callback(
    [
        Output('studentprofile_deletediv', 'className'),  # Adjust visibility of delete option
        Output('studentprofile_studid', 'data'),
        Output('studentprofile_fname', 'value'),
        Output('studentprofile_lname', 'value'),
        Output('studentprofile_bdate', 'value'),
        Output('studentprofile_age', 'value'),
        Output('studentprofile_gender', 'value'),
        Output('studentprofile_city', 'value'),
        Output('studentprofile_address', 'value'),
        Output('studentprofile_gradelvl', 'value'),
        Output('studentprofile_parent_fname', 'value'),
        Output('studentprofile_parent_email', 'value'),
        Output('studentprofile_parent_job', 'value'),
        Output('studentprofile_relationship', 'value'),
        Output('studentprofile_parent_contact', 'value'),
    ],
    [Input('url', 'pathname')],
    [
        State('url', 'search'),
        State('currentuserid', 'data')]
)
def studentprofile_populate(pathname, urlsearch, currentuserid):
    print(currentuserid)
    if pathname == '/student/student_profile_edit':
        parsed = urlparse(urlsearch)
        create_mode = parse_qs(parsed.query).get('mode', [None])[0]
        
        if create_mode == 'add':
            studid = 0
            deletediv = 'd-none'  # Hide delete option when adding a new student
            
            # Return default values for a new student, ensuring all 13 fields are accounted for
            return deletediv, studid, '', '', '', '', 'Prefer not to say', '', '', 'Kindergarten', '', '', 'Mother', ''
        
        else:
            studid = int(parse_qs(parsed.query).get('id', [0])[0])
            deletediv = ''  # Show delete option when editing an existing student
            
            sql = """
                SELECT stud_fname AS fname,
                       stud_lname AS lname,
                       stud_bdate as bdate,
                       stud_age AS age,
                       stud_gender AS gender,
                       stud_city AS city,
                       stud_address AS address,
                       stud_gradelvl AS gradelvl,
                       parent_fname AS parent_fname,
                       parent_email AS parent_email,
                       parent_job AS parent_job,
                       relationship AS relationship,
                       parent_contact AS parent_contact                       
                FROM student WHERE stud_id = %s;
            """
            
            values = [studid]
            col = ['fname', 'lname', 'bdate', 'age', 'gender', 'city', 'address', 'gradelvl', 
                   'parent_fname', 'parent_email', 'parent_job', 'relationship', 'parent_contact']
            
            df = getDataFromDB(sql, values, col)

            # Ensure all 13 fields are returned even when editing an existing student
            return deletediv, studid, df['fname'][0], df['lname'][0], df['bdate'][0], df['age'][0], df['gender'][0], df['city'][0], df['address'][0], df['gradelvl'][0], df['parent_fname'][0], df['parent_email'][0], df['parent_job'][0], df['relationship'][0], df['parent_contact'][0]
    
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
        State('studentprofile_bdate', 'value'),
        State('studentprofile_age', 'value'),
        State('studentprofile_gender', 'value'),
        State('studentprofile_city', 'value'),
        State('studentprofile_address', 'value'),
        State('studentprofile_gradelvl', 'value'),
        State('studentprofile_parent_fname', 'value'),
        State('studentprofile_parent_email', 'value'),
        State('studentprofile_parent_job', 'value'),
        State('studentprofile_relationship', 'value'),
        State('studentprofile_parent_contact', 'value'),
        State('url', 'search'),
        State('studentprofile_studid', 'data'),
        State('studentprofile_deleteind', 'value'),
        State('currentuserid', 'data')
    ]
)
def studentprofile_saveprofile(submitbtn, fname, lname, bdate, age, gender, city, address, gradelvl, parent_fname, parent_email, parent_job, relationship, parent_contact, urlsearch, studid, deleteind, currentuserid):
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
                    INSERT INTO student (stud_fname, stud_lname, stud_bdate, stud_age, stud_gender, stud_city,
                                         stud_address, stud_gradelvl, parent_fname, parent_email,
                                         parent_job, relationship, parent_contact, stud_delete_ind, user_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )
                '''
                values = [fname, lname, bdate, age, gender, city, address, gradelvl, parent_fname, parent_email, parent_job, relationship, parent_contact, False, currentuserid]

            elif create_mode == 'edit':
                sql = '''
                    UPDATE student
                    SET 
                        stud_fname = %s,
                        stud_lname = %s,
                        stud_bdate = %s,
                        stud_age = %s,
                        stud_gender = %s,
                        stud_city = %s,
                        stud_address = %s,
                        stud_gradelvl = %s,
                        parent_fname = %s,
                        parent_email = %s,
                        parent_job = %s,
                        relationship = %s,
                        parent_contact = %s,
                        stud_delete_ind = %s
                    WHERE
                        stud_id = %s
                '''
                values = [fname, lname, bdate, age, gender, city, address, gradelvl, parent_fname, parent_email, parent_job, relationship, parent_contact, 
                          bool(deleteind), studid]

            else:
                raise PreventUpdate

            modifyDB(sql, values)

            # If this is successful, we want the success modal to show
            modal_open = True

        return [alert_color, alert_text, alert_open, modal_open]

    else: 
        raise PreventUpdate
    
@app.callback(
     Output('studentprofile_age', 'value', allow_duplicate=True),  # Allow duplicate outputs
    [Input('studentprofile_bdate', 'value')],
    prevent_initial_call=True  # Prevent the callback from firing when the app loads
)
def update_age(bdate):
    if bdate:
        bdate_date = date.fromisoformat(bdate)
        today = date.today()
        age = today.year - bdate_date.year - ((today.month, today.day) < (bdate_date.month, bdate_date.day))
        return age
    return None
