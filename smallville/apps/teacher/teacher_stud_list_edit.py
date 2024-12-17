from urllib.parse import parse_qs, urlparse
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html
from dash.exceptions import PreventUpdate

from app import app
from apps.dbconnect import getDataFromDB, modifyDB

layout = html.Div(
    [
        dcc.Store(id='studentprofile_studid_store', storage_type='memory', data=0),  # Store student ID to prevent duplicate callbacks

        # Header with Return button
        dbc.Row(
            [
                dbc.Col(html.H2('Student Details', style={'width': "100%"}), width=10),
                dbc.Col(
                    dbc.Button(
                        "Return",
                        color='primary',
                        href=f'/admin',
                    ),
                    width=2,
                    className="text-end"
                )
            ],
            align="center"
        ),

        html.Hr(),
        dbc.Alert(id='studentprofile_alert_box', is_open=False),

        # Student details form (Now only enrollment status is editable)
        dbc.Form(
            dbc.Table(
                [
                    # First Name
                    html.Tr([
                        html.Td(dbc.Label("First Name"), style={'width': '10%'}),
                        html.Td(html.Div(id='studentprofile_input_fname', style={'width': '80%'}))
                    ]),
                    # Last Name
                    html.Tr([
                        html.Td(dbc.Label("Last Name"), style={'width': '10%'}),
                        html.Td(html.Div(id='studentprofile_input_lname', style={'width': '80%'}))
                    ]),
                    # Age
                    html.Tr([
                        html.Td(dbc.Label("Age"), style={'width': '10%'}),
                        html.Td(html.Div(id='studentprofile_input_age', style={'width': '80%'}))
                    ]),
                    # Gender
                    html.Tr([
                        html.Td(dbc.Label("Gender"), style={'width': '10%'}),
                        html.Td(html.Div(id='studentprofile_select_gender', style={'width': '100%'}))
                    ]),
                    # City
                    html.Tr([
                        html.Td(dbc.Label("City"), style={'width': '10%'}),
                        html.Td(html.Div(id='studentprofile_input_city', style={'width': '80%'}))
                    ]),
                    # Address
                    html.Tr([
                        html.Td(dbc.Label("Address"), style={'width': '10%'}),
                        html.Td(html.Div(id='studentprofile_input_address', style={'width': '80%'}))
                    ]),
                    # Grade Level
                    html.Tr([
                        html.Td(dbc.Label("Grade Level"), style={'width': '10%'}),
                        html.Td(html.Div(id='studentprofile_select_gradelvl', style={'width': '100%'}))
                    ]),
                ]
            )
        ),

        # Parent Details Section (Read-only)
        html.H2('Parent Details'),
        html.Hr(),
        dbc.Form(
            dbc.Table(
                [
                    html.Tr([
                        html.Td(dbc.Label("Parent Full Name"), style={'width': '10%'}),
                        html.Td(html.Div(id='studentprofile_input_parent_fname', style={'width': '80%'}))
                    ]),
                    html.Tr([
                        html.Td(dbc.Label("Parent Email"), style={'width': '10%'}),
                        html.Td(html.Div(id='studentprofile_input_parent_email', style={'width': '80%'}))
                    ]),
                    html.Tr([
                        html.Td(dbc.Label("Contact Number"), style={'width': '10%'}),
                        html.Td(html.Div(id='studentprofile_input_parent_contact', style={'width': '80%'}))
                    ]),
                    html.Tr([
                        html.Td(dbc.Label("Parent Job"), style={'width': '10%'}),
                        html.Td(html.Div(id='studentprofile_input_parent_job', style={'width': '80%'}))
                    ]),
                    html.Tr([
                        html.Td(dbc.Label("Relationship"), style={'width': '10%'}),
                        html.Td(html.Div(id='studentprofile_select_relationship', style={'width': '100%'}))
                    ]),
                ]
            )
        ),
        
        # Enrollment Details Section (Only enrollment status is editable)
        html.H2('Enrollment Details'),
        html.Hr(),
        dbc.Form(
            dbc.Table(
                [
                    html.Tr([
                        html.Td(dbc.Label("Enrollment Status"), style={'width': '10%'}),
                        html.Td(dbc.Select(
                            id='studentprofile_select_enrollmentstatus',
                            style={'width': '100%'},
                            options=[
                                {'label': 'Enrolled', 'value': 'TRUE'},
                                {'label': 'Not Enrolled', 'value': 'FALSE'}
                            ],
                            value='FALSE',  # Default value is "Not Enrolled"
                            placeholder="Not Enrolled",
                            disabled=False
                        ))
                    ]),
                    # html.Tr([
                    #     html.Td(dbc.Label("Mark as deleted?"), style={'width': '10%'}),
                    #     html.Td(html.Div(id='studentprofile_checklist_deleteind', style={'width': '80%'}))
                    # ]),
                ]
            )
        ),
        
        # Hidden Div for delete functionality
        html.Div(id='studentprofile_hidden_delete', className='d-none'),
        
        # Submit Button (Disabled as fields are read-only)
        dbc.Button('Submit', id='studentprofile_button_submit', n_clicks=0, disabled=False),
        
        # Success Modal
        dbc.Modal(
            [
                dbc.ModalHeader(html.H4('Save Success')),
                dbc.ModalBody('Student details have been saved successfully!'),
                dbc.ModalFooter(dbc.Button("Proceed", href='/admin'))  # Redirect to student list page
            ],
            centered=True,
            id='studentprofile_modal_success',
            backdrop='static'
        )
    ]
)

# Callback to populate the form when editing or adding a student
@app.callback(
    [
        Output('studentprofile_hidden_delete', 'className'),
        Output('studentprofile_studid_store', 'data'),
        Output('studentprofile_input_fname', 'children'),
        Output('studentprofile_input_lname', 'children'),
        Output('studentprofile_input_age', 'children'),
        Output('studentprofile_select_gender', 'children'),
        Output('studentprofile_input_city', 'children'),
        Output('studentprofile_input_address', 'children'),
        Output('studentprofile_select_gradelvl', 'children'),
        Output('studentprofile_input_parent_fname', 'children'),
        Output('studentprofile_input_parent_email', 'children'),
        Output('studentprofile_input_parent_contact', 'children'),
        Output('studentprofile_input_parent_job', 'children'),
        Output('studentprofile_select_relationship', 'children'),
        Output('studentprofile_select_enrollmentstatus', 'value'),
    ],
    [Input('url', 'pathname')],
    [State('url', 'search')]
)
def studentprofile_populate(pathname, urlsearch):
    if pathname == '/teacher/teacher_stud_list_edit':
        parsed = urlparse(urlsearch)
        create_mode = parse_qs(parsed.query).get('mode', [None])[0]

        if create_mode == 'add':
            studid = 0
            hidden_delete = 'd-none'  # Hide delete option for new students
            return hidden_delete, studid, '', '', '', 'Prefer not to say', '', '', 'Kindergarten', '', '', '', 'Mother', 'FALSE'

        else:
            studid = int(parse_qs(parsed.query).get('id', [0])[0])
            hidden_delete = ''  # Show delete option for editing students
            sql = """
                SELECT stud_fname AS fname, stud_lname AS lname, stud_age AS age, stud_gender AS gender, 
                       stud_city AS city, stud_address AS address, stud_gradelvl AS gradelvl, 
                       parent_fname AS parent_fname, parent_email AS parent_email, parent_contact as parent_contact, parent_job AS parent_job, 
                       relationship AS relationship, enroll_status as enroll_status
                FROM student WHERE stud_id = %s;
            """
            values = [studid]
            col = ['fname', 'lname', 'age', 'gender', 'city', 'address', 'gradelvl', 'parent_fname', 'parent_email', 'parent_contact',
                   'parent_job', 'relationship', 'enroll_status']
            record = getDataFromDB(sql, values, col)
            return hidden_delete, studid, record['fname'][0], record['lname'][0], record['age'][0], record['gender'][0], \
                   record['city'][0], record['address'][0], record['gradelvl'][0], record['parent_fname'][0], \
                   record['parent_email'][0], record['parent_contact'][0], record['parent_job'][0], record['relationship'][0], record['enroll_status'][0]
    raise PreventUpdate

# Callback to submit data
@app.callback(
    Output('studentprofile_modal_success', 'is_open'),
    Input('studentprofile_button_submit', 'n_clicks'),
    [State('studentprofile_studid_store', 'data'),
     State('studentprofile_select_enrollmentstatus', 'value')]
)
def studentprofile_submit(n_clicks, studid, enroll_status):
    if n_clicks > 0:
        # Handle data submission logic here
        if studid > 0:  # If it's an existing student, update enrollment status
            sql = "UPDATE student SET enroll_status = %s WHERE stud_id = %s"
            modifyDB(sql, [enroll_status, studid])
        
        return True
    raise PreventUpdate
