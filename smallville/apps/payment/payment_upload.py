import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html
from dash.exceptions import PreventUpdate
from app import app
from apps.dbconnect import modifyDB

layout = html.Div(
    [
        html.H2('New Payment Form'),
        html.P('Fill out the form to submit your tuition fee proof of payment.'),
        html.Hr(),
        dbc.Alert(id='paymentupload_alert', is_open=False),
        dbc.Form(
            dbc.Table(
                [
                    html.Tr([
                        html.Td(
                            dbc.Label("Student Name"), 
                            style={'width': '10%'}
                        ),
                        html.Td(
                            dbc.Input(
                                type='text', 
                                id='stud_name', 
                                placeholder="Student Name"
                            ), 
                            style={'width': '80%'}
                        )
                        ], 
                        className='mb-3'
                    ),

                    html.Tr([
                        html.Td(
                            dbc.Label("Chosen Payment Plan"), 
                            style={'width': '10%'}
                        ),
                        html.Td(
                            dbc.Input(
                                type='text', 
                                id='payment_plan', 
                                placeholder="Plan"
                            ), 
                            style={'width': '80%'}
                        )
                    ], 
                    className='mb-3'
                    ),

                    html.Tr([
                        html.Td(
                            dbc.Label("Reference Number"), 
                            style={'width': '10%'}
                        ),
                        html.Td(
                            dbc.Input(
                                type='text', 
                                id='payment_num', 
                                placeholder="Reference Number"
                            ),
                            style={'width': '80%'}
                        )
                    ], 
                    className='mb-3'
                    ),

                    html.Tr([
                        html.Td(
                            dbc.Label("Date"), 
                            style={'width': '10%'} 
                        ),
                        html.Td(
                            dbc.Input(
                                type='date', 
                                id='payment_date'
                            ), 
                            style={'width': '80%'}
                        )
                    ], 
                    className='mb-3'
                    ),

                    html.Tr([
                        html.Td(
                            dbc.Label("Payment Method"), 
                            style={'width': '10%'}
                        ),
                        html.Td(
                            dbc.Select(
                                id='payment_method', 
                                options=[{"label": "BDO", "value": "BDO"}, 
                                         {"label": "BPI", "value": "BPI"}], 
                                placeholder="Select Payment Method"
                            ), 
                            style={'width': '80%'}
                        )
                    ], 
                    className='mb-3'
                    ),

                    html.Tr([
                        html.Td(
                            dbc.Label("Upload Proof of Payment"), 
                            style={'width': '10%'}
                        ),
                        html.Td(
                            dcc.Upload(
                                id='paymentupload_proof', 
                                children=html.Button('Upload Proof'), 
                                multiple=False
                            ), 
                            style={'width': '80%'}
                        )
                    ]),
                    html.Tr([
                        html.Td(
                            dbc.Label(" "), 
                            style={'width': '10%'}
                        ), 
                        html.Td(
                            html.Div(id='output-image-upload'), 
                            style={'width': '80%'}
                            )
                    ])
                ]
            )
        ),
        dbc.Button('Submit', id='submit_payment', n_clicks=0),
        dbc.Modal([
            dbc.ModalHeader(html.H4('Upload Success')),
            dbc.ModalBody('Proof of payment has been uploaded successfully!'),
            dbc.ModalFooter(dbc.Button("Proceed", href='/student/payment'))
        ], centered=True, id='paymentupload_successmodal', backdrop='static')
    ]
)

def parse_contents(contents, filename):
    if contents:
        return html.Div([
            html.H5(filename), 
            # HTML images accept base64 encoded strings in the same format
            # that is supplied by the upload
            html.Img(src=contents, style={'width': '100%', 'height': 'auto'})
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
        State('stud_name', 'value'),
        State('payment_plan', 'value'),
        State('payment_num', 'value'),
        State('payment_date', 'value'),
        State('payment_method', 'value'),
        State('paymentupload_proof', 'contents'),
        State('paymentupload_proof', 'filename')
    ]
)

def paymentupload_populate(n_clicks, stud_name, pay_plan, pay_num, pay_date, pay_method, pay_proof, filename):
    if not n_clicks:
        raise PreventUpdate

    # Validate inputs
    if not stud_name:
        return True, 'danger', 'Please supply the student name.', False
    elif not pay_plan:
        return True, 'danger', 'Please supply the chosen payment plan.', False
    elif not pay_num:
        return True, 'danger', 'Please supply the payment number.', False
    elif not pay_date:
        return True, 'danger', 'Please supply the payment date.', False
    elif not pay_method:
        return True, 'danger', 'Please supply the payment method.', False
    elif not pay_proof:
        return True, 'danger', 'Please upload proof of payment.', False

    try:
        # Decode the uploaded proof 
        if pay_proof:
            proof_data = pay_proof.split(',')[1]  # Remove base64 metadata

            # Insert into database
            sql = '''
                INSERT INTO payment (stud_name, pay_plan, pay_num, pay_date, pay_method, pay_proof)
                VALUES (%s, %s, %s, %s, %s, %s)
            '''
            values = (stud_name, pay_plan, pay_num, pay_date, pay_method, proof_data)

            # Perform the database insert operation
            modifyDB(sql, values)

            return False, '', '', True  # Success modal will show
        else:
            return True, 'danger', 'Error processing payment proof.', False

    except Exception as e:
        print(e)
        return True, 'danger', 'Error saving payment. Please try again.', False  # Error feedback
