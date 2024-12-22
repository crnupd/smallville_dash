import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html
from dash.exceptions import PreventUpdate
import base64
from app import app
from apps.dbconnect import modifyDB

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.H2('New Payment Form', style={'width': "100%"}), width=10),  # Page Header
                dbc.Col(
                    dbc.Button(
                        "Return",
                        color='primary',
                        href=f'/student/payment',
                    ),
                    width=2,
                    className="text-end"  # Aligns the button to the right
                )
            ],
            align="center"
        ),

        dbc.Alert(id='paymentupload_alert', is_open=False),
        html.Hr(style={'border-top': '3px solid #343a40'}),
        dbc.Form(
            dbc.Table(
                [
                    html.Br(),
                    html.Tr([
                        html.Td(
                            dbc.Label("Student ID"), 
                            style={'width': '20%'}
                        ),
                        html.Td(
                            dbc.Input(
                                type='text', 
                                id='student_id', 
                                placeholder="Student ID",
                                style={'width': '90%', 'border': '2px solid #CCCECF'}
                            ), 
                            style={'width': '80%'}
                        )
                        ], 
                        className='mb-3'
                    ),

                    html.Tr([
                        html.Td(
                            dbc.Label("Chosen Payment Plan"), 
                            style={'width': '20%'}
                        ),
                        html.Td(
                            dbc.Select(
                                id='payment_plan', 
                                options=[{"label": "Monthly", "value": "Monthly"}, 
                                         {"label": "Quarterly", "value": "Quarterly"},
                                         {"label": "Yearly", "value": "Yearly"}], 
                                placeholder="Select Payment Plan",
                                style={'width': '90%', 'border': '2px solid #CCCECF'}
                            ),  
                            style={'width': '80%'}
                        )
                    ], 
                    className='mb-3'
                    ),

                    html.Tr([
                        html.Td(
                            dbc.Label("Reference Number"), 
                            style={'width': '20%'}
                        ),
                        html.Td(
                            dbc.Input(
                                type='text', 
                                id='payment_num', 
                                placeholder="Reference Number",
                                style={'width': '90%', 'border': '2px solid #CCCECF'}
                            ),
                            style={'width': '80%'}
                        )
                    ], 
                    className='mb-3'
                    ),

                    html.Tr([
                        html.Td(
                            dbc.Label("Amount"), 
                            style={'width': '20%'}
                        ),
                        html.Td(
                            dbc.Input(
                                type='text', 
                                id='payment_amt', 
                                placeholder="Payment Amount",
                                style={'width': '90%', 'border': '2px solid #CCCECF'}
                            ),
                            style={'width': '80%'}
                        )
                    ], 
                    className='mb-3'
                    ),

                    html.Tr([
                        html.Td(
                            dbc.Label("Date"), 
                            style={'width': '20%'} 
                        ),
                        html.Td(
                            dbc.Input(
                                type='date', 
                                id='payment_date',
                                style={'width': '90%', 'border': '2px solid #CCCECF'}
                            ), 
                            style={'width': '80%'}
                        )
                    ], 
                    className='mb-3'
                    ),

                    html.Tr([
                        html.Td(
                            dbc.Label("Payment Method"), 
                            style={'width': '20%'}
                        ),
                        html.Td(
                            dbc.Select(
                                id='payment_method', 
                                options=[{"label": "BDO", "value": "BDO"}, 
                                         {"label": "BPI", "value": "BPI"}], 
                                placeholder="Select Payment Method",
                                style={'width': '90%', 'border': '2px solid #CCCECF'}
                            ), 
                            style={'width': '80%'}
                        )
                    ], 
                    className='mb-3'
                    ),

                    html.Tr([
                        html.Td(
                            dbc.Label("Upload Proof of Payment"), 
                            style={'width': '20%'}
                        ),
                        html.Td(
                            dcc.Upload(
                                id='paymentupload_proof', 
                                children=dbc.Button(
                                    'Upload Proof', 
                                    color='warning',  # Match with the 'Submit' button color
                                    style={'font-weight': 'bold'}
                                ), 
                                multiple=False,
                            ), 
                            style={'width': '80%'}
                        ),
                    ]),
                    html.Tr([
                        html.Td(
                            dbc.Label(" "), 
                            style={'width': '20%'}
                        ), 
                        html.Td(
                            html.Div(id='output-image-upload'), 
                            style={'width': '80%'}
                            )
                    ])
                ]
            )
        ),
        dbc.Button(
            'Submit', 
            id='submit_payment', 
            n_clicks=0,
            style={
                'background-color': '#218838',
                'color': '#fff',
                'border': '2px solid #155724',
                'margin-top': '15px',
                'font-weight': 'bold'
            }
        ),
        dbc.Modal([
            dbc.ModalHeader(html.H4('Upload Success')),
            dbc.ModalBody('Proof of payment has been uploaded successfully!'),
            dbc.ModalFooter(dbc.Button("Proceed", href='/student/payment'))
        ], centered=True, id='paymentupload_successmodal', backdrop='static')
    ],
    style={
        'margin-top': '70px',
        'background-color': '#ffffff',
        'color': '#212529',
        'padding': '20px',
        'border-radius': '10px',
        'box-shadow': '0px 4px 6px rgba(0, 0, 0, 0.2)'
    }
)

def parse_contents(contents, filename):
    if contents:
        return html.Div([
            html.H5(filename), 
            # HTML images accept base64 encoded strings in the same format
            # that is supplied by the upload
            html.Img(src=contents, style={'max-width': '60%', 'max-height': 'auto'})
        ])
    return html.Div(["No image uploaded."])

#callback for displaying file before submission
@app.callback(
    Output('output-image-upload', 'children'),
    [Input('paymentupload_proof', 'contents')],
    [State('paymentupload_proof', 'filename')]
)

def update_image_preview(contents, filename):
    if contents:
        return parse_contents(contents, filename)
    return html.Div(["No image uploaded."])

#callback for form fillup
@app.callback(
    [
        Output('paymentupload_alert', 'is_open'),
        Output('paymentupload_alert', 'color'),
        Output('paymentupload_alert', 'children'),
        Output('paymentupload_successmodal', 'is_open')
    ],
    Input('submit_payment', 'n_clicks'),
    [
        State('student_id', 'value'),
        State('payment_plan', 'value'),
        State('payment_num', 'value'),
        State('payment_amt', 'value'),
        State('payment_date', 'value'),
        State('payment_method', 'value'),
        State('paymentupload_proof', 'contents'),
        State('paymentupload_proof', 'filename'),
        State('currentuserid', 'data')
    ]
)

def paymentupload_populate(n_clicks, stud_id, pay_plan, pay_num, pay_amt, pay_date, pay_method, pay_proof, filename, currentuserid):
    if not n_clicks:
        raise PreventUpdate

    # Validate inputs
    if not stud_id:
        return True, 'danger', 'Please supply the student name.', False
    elif not pay_plan:
        return True, 'danger', 'Please supply the chosen payment plan.', False
    elif not pay_num:
        return True, 'danger', 'Please supply the payment number.', False
    elif not pay_amt:
        return True, 'danger', 'Please supply the payment number.', False
    elif not pay_date:
        return True, 'danger', 'Please supply the payment date.', False
    elif not pay_method:
        return True, 'danger', 'Please supply the payment method.', False
    elif not pay_proof:
        return True, 'danger', 'Please upload proof of payment.', False
    elif not currentuserid or currentuserid <= 0:  # Ensure currentuserid is valid
        return True, 'danger', 'You must be logged in to submit payment proof.', False

    try:
        # Decode the uploaded proof 
        if pay_proof:
            proof_data = base64.b64decode(pay_proof.split(',')[1])  # Remove base64 metadata
    
            # Insert into database
            sql = '''
                INSERT INTO payment (user_id, stud_id, pay_plan, pay_num, pay_amt, pay_date, pay_method, pay_proof)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            '''
            values = (currentuserid, stud_id, pay_plan, pay_num, pay_amt, pay_date, pay_method, proof_data)

            # Perform the database insert operation
            modifyDB(sql, values)

            return False, '', '', True  # Success modal will show
        else:
            return True, 'danger', 'Error processing payment proof.', False

    except Exception as e:
        print(e)
        return True, 'danger', 'Error saving payment. Please try again.', False  # Error feedback