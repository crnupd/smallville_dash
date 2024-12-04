import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html
from datetime import date
from dash.exceptions import PreventUpdate
import base64

from app import app
from apps.dbconnect import modifyDB

layout = html.Div(
    [
        html.H2('New Payment Form'),  # Page Header
        html.P('Fill out the form to submit your tuition fee proof of payment.'),
        html.Hr(),
        dbc.Alert(id='paymentupload_alert', is_open=False),  # For feedback purposes
        dbc.Form(
            [
                dbc.Row(
                    [
                        dbc.Label("Student Name", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text', 
                                id='stud_name',
                                placeholder="Student Name"
                            ),
                            width=5
                        )
                    ],
                    className='mb-3'
                ),
                dbc.Row(
                    [
                        dbc.Label("Chosen Payment Plan", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text', 
                                id='pay_plan',
                                placeholder="Plan"
                            ),
                            width=5
                        )
                    ],
                    className='mb-3'
                ),
                dbc.Row(
                    [
                        dbc.Label("Payment Number", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text', 
                                id='pay_num',
                                placeholder="Payment Number"
                            ),
                            width=5
                        )
                    ],
                    className='mb-3'
                ),
                dbc.Row(
                    [
                        dbc.Label("Date", width=1),
                        dbc.Col(
                            dcc.DatePickerSingle(
                                month_format='YYYY-MM-DD',
                                placeholder='YYYY-MM-DD',
                                id='pay_date',
                            ),
                            width=5
                        )
                    ],
                    className='mb-3'
                ),
                dbc.Row(
                    [
                        dbc.Label("Payment Method", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text', 
                                id='pay_method',
                                placeholder="Payment Method"
                            ),
                            width=5
                        )
                    ],
                    className='mb-3'
                ),
                dbc.Row(
                    [
                        dbc.Label("Upload Proof of Payment", width=1),
                        dbc.Col(
                            dcc.Upload(
                                id='pay_proof',
                                children=html.Div(
                                    ["Drag and Drop or ", html.A("Select Files")]
                                ),
                            ),
                            width=5
                        )
                    ],
                )
            ]
        ),
        dbc.Button(
            'Submit',
            id='submit_payment',
            n_clicks=0  # Initialize number of clicks
        ),
        dbc.Modal(  # Modal = dialog box; feedback for successful saving.
            [
                dbc.ModalHeader(html.H4('Upload Success')),
                dbc.ModalBody('Proof of payment have been uploaded successfully!'),
                dbc.ModalFooter(dbc.Button("Proceed", href='/student/payment'))  # Redirect after saving
            ],
            centered=True,
            id='paymentupload_successmodal',
            backdrop='static'  # Dialog box does not go away if you click at the background
        )
    ]
)

@app.callback(
    [
        Output('paymentupload_alert', 'is_open'),
        Output('paymentupload_alert', 'color'),
        Output('paymentupload_alert', 'children'),
        Output('paymentupload_successmodal', 'is_open'),
    ],
    Input('submit_payment', 'n_clicks'),
    [
        State('stud_name', 'value'),
        State('pay_plan', 'value'),
        State('pay_num', 'value'),
        State('pay_date', 'date'),
        State('pay_method', 'value'),
        State('pay_proof', 'contents'),
    ]
)
def paymentupload_populate(n_clicks, stud_name, pay_plan, pay_num, pay_date, pay_method, pay_proof):
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

    else:
    # Decode the uploaded proof
        proof_data = base64.b64decode(pay_proof.split(',')[1])

    # Insert into database
        sql = '''
            INSERT INTO payment (stud_name, pay_plan, pay_num, pay_date, pay_method, pay_proof)
            VALUES (%s, %s, %s, %s, %s, %s)
        '''
        values = (stud_name, pay_plan, pay_num, pay_date, pay_method, proof_data)

    try:
        modifyDB(sql, values)
        return False, '', '', True
    except Exception as e:
        print(e)
        return True, 'danger', 'Error saving payment. Please try again.', False