import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
from dash.exceptions import PreventUpdate
from index import ADMIN_USER_ID
import base64

from app import app
from apps.dbconnect import getDataFromDB

table_header = [
    html.Thead(html.Tr([html.Th("PLAN", style={'width':'33%'}), html.Th("Amount per Payment (in pesos)", style={'width':'33%'}),  html.Th("Total to Pay (in pesos)", style={'width':'33%'})]))
]

row1 = html.Tr([html.Td("Monthly"), html.Td("6,125.00"), html.Td("73,500")])
row2 = html.Tr([html.Td("Quarterly"), html.Td("18,025.00"), html.Td("72,100")])
row3 = html.Tr([html.Td("Yearly"), html.Td("70,000"), html.Td("70,000")])

table_body = [html.Tbody([row1, row2, row3])]

table = dbc.Table(table_header + table_body, bordered=True, className='active')

layout = html.Div(
    [
        # Page Header
        html.Div(
            [
                html.H2('Payment Page'),
                html.Hr(),
            ],
            style={'margin-top': '15px'}  # Adjust margin to avoid overlap with navbar
        ),
        dbc.Card(  # Card Container
            [
                dbc.CardBody(  # Define Card Contents
                    [
                        html.Div(  
                            [
                                html.H5("Payment Plan Details"),
                                html.P("Total Tuition Fee: 70,000 pesos"),
                                table,
                                html.H6("Important Notice"),
                                html.P(["- Families are encouraged to select the payment plan that best fits their financial situation.", html.Br(), 
                                        "- All payments are due on the first of each month or quarter as applicable.", html.Br(),
                                        "- Please ensure that all payments are made before the due dates to avoid any late fees.", html.Br(),
                                        "- You may upload the transaction receipt at this website. Your Payment History is also shown below for your reference.",]),
                                html.H6("Payment Options for Enrollment at Smallville Montessori"),
                                html.P(["Bank Transfer via BDO", html.Br(), 
                                        "Account Name: Smallville Montessori School", html.Br(), 
                                        "Account Number: 1234-5678-9012", html.Br(),
                                        "Branch: Smallville Branch", html.Br(),
                                        "Payment Reference: Please include your child's name and grade level in the reference.", html.Br(),
                                        ]),
                                html.P(["Bank Transfer via BPI", html.Br(), 
                                        "Account Name: Smallville Montessori School", html.Br(), 
                                        "Account Number: 9876-5432-1098", html.Br(),
                                        "Branch: Main Branch", html.Br(),
                                        "Payment Reference: Please include your child's name and grade level in the reference.", html.Br(),
                                        ]),
                                
                            ]
                        ), 
                    ]       
                )
            ]
        ),
        html.Br(),
        html.Div(
            [
                dbc.Button(
                    "Upload",
                    color='primary',
                    href=f'/student/payment_upload',
                )
            ],
            style={'textAlign': 'right'}  # Aligns the button on the right side
        ),
        html.Br(),
        dbc.Card(  # Card Container
            [
                dbc.CardHeader(  # Define Card Header
                    html.H3('Payment History')
                ),
                dbc.CardBody(  # Define Card Contents
                    html.Div(id='payment_history') # payment history list
                )
            ]
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Proof of Payment")),
                dbc.ModalBody(html.Img(id='payment_image', src='', style={'width': '100%'})),
            ],
            id="payment-modal",
            size='lg',
            is_open=False,
        )
    ]
)

@app.callback(
    Output('payment_history', 'children'),
    [Input('url', 'pathname')],
    [State('currentuserid', 'data')]
)
def updateRecordsTable(pathname, currentuserid):
    if pathname != '/student/payment':  # Corrected pathname check
        raise PreventUpdate
    
    if not currentuserid or currentuserid <= 0:
        return html.Div("Please log in to view this page."), ''
    
    # Check if the user is admin (user_id = 1 for admin, tentative)
    if currentuserid == ADMIN_USER_ID:  # Admin user ID
        sql = """ 
            SELECT 
                pay_id, 
                stud_id, 
                pay_plan, 
                pay_num, 
                pay_amt, 
                pay_date, 
                pay_method, 
                pay_proof 
            FROM payment
        """
        val = []  # No specific condition since admin sees all payment history records
    else:
        sql = """ 
            SELECT 
                pay_id, 
                stud_id, 
                pay_plan, 
                pay_num, 
                pay_amt, 
                pay_date, 
                pay_method, 
                pay_proof 
            FROM payment
            WHERE user_id = %s 
        """
        val = [currentuserid] # Normal users see only their payment history
        
    col = ["Payment ID", "Student ID", "Plan", "Reference No.", "Amount", "Payment Date", "Payment Method", "Proof"]

    df = getDataFromDB(sql, val, col)

    if df.empty:
        return html.Div("No payment history found.")  # Provide feedback if no records exist

    df['Proofs'] = [
        html.Div(
            dbc.Button("View", color='warning', size='sm', 
                        id={'type': 'view-button', 'index': row["Payment ID"]}),
            className='text-center'
        ) for idx, row in df.iterrows()
    ]

    # Exclude 'proof' from display and replace with button
    df = df[["Student ID", "Plan", "Reference No.","Amount","Payment Date", "Payment Method", "Proofs"]]

    payment_table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
                                              hover=True, size='sm')

    return [payment_table]  # Return the generated table directly


#callback for viewing photo proofs
@app.callback(
    [Output("payment-modal", "is_open"), Output("payment_image", "src")],
    [Input({"type": "view-button", "index": dash.ALL}, "n_clicks"),],
    [State({"type": "view-button", "index": dash.ALL}, "id")]
)
def displayPaymentProof(n_clicks_list, button_id):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate

    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    button_id = eval(triggered_id) if isinstance(triggered_id, str) else triggered_id
    payment_id = button_id.get('index') if button_id else None

    # Check if clicked button exists and was clicked
    if payment_id is None or not any(n_clicks_list):
        raise PreventUpdate

    sql = "SELECT pay_proof FROM payment WHERE pay_id = %s"
    proof_data = getDataFromDB(sql, (payment_id,), ["pay_proof"])

    if proof_data.empty or proof_data.iloc[0]['pay_proof'] is None:
        return False, ''  # If no proof data, do not open the modal

    # Convert the binary bytea data to base64
    binary_data = proof_data.iloc[0]['pay_proof']
    base64_image = base64.b64encode(binary_data).decode('utf-8')
    image_src = f"data:image/png;base64,{base64_image}"

    return True, image_src
