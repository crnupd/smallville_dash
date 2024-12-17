import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc, ALL
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
            style={'margin-top': '70px'}  # Adjust margin to avoid overlap with navbar
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
                [   
                    html.Hr(),
                    html.Div(
                        [
                            html.H4('Filter by Columns'),
                            html.Div(id='pay-filter-rows-container'),
                            dbc.Button("Add Filter", id="add-filter-button", n_clicks=0, className="mt-2"),
                            html.Hr(),
                            html.Div(id='payment_history') # payment history list
                        ]
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
    ]
)

#callback for filters
@app.callback(
    Output('pay-filter-rows-container', 'children'),
    [
        Input('add-filter-button', 'n_clicks'),
        Input({'type': 'remove-filter-button', 'index': ALL}, 'n_clicks')
    ],
    State('pay-filter-rows-container', 'children'),
    prevent_initial_call=True
)
def manage_filter_rows(add_clicks, remove_clicks, current_children):
    ctx = dash.callback_context

    if current_children is None:
        current_children = []

    # Handle Add Filter button click
    if ctx.triggered_id == 'add-filter-button':
        new_index = len(current_children)

        # Dynamically decide input type for new row
        input_component = dbc.Input(
            type='text',
            id={"type": "filter-value-input", "index": new_index},
            placeholder='Enter filter value',
            style={'margin': '2px 0px'}
        )

        # Add a new row
        new_row = dbc.Row(
            id={"type": "filter-row", "index": new_index},
            children=[
                dbc.Col(
                    dcc.Dropdown(
                        id={"type": "filter-column-dropdown", "index": new_index},
                        options=[
                            {'label': 'Student ID', 'value': 'stud_id'},
                            {'label': 'Plan', 'value': 'pay_plan'},
                            {'label': 'Payment Date', 'value': 'pay_date'},
                            {'label': 'Payment Method', 'value': 'pay_method'}
                        ],
                        placeholder="Select Column",
                        clearable=False,
                        style={'margin': '2px 0px'}
                    ),
                    width=5
                ),
                dbc.Col(input_component, width=5),
                dbc.Col(
                    dbc.Button(
                        "Remove",
                        id={"type": "remove-filter-button", "index": new_index},
                        color="danger",
                        size="sm",
                        className="mt-1"
                    ),
                    width=2
                )
            ],
            className="mb-2"
        )

        current_children.append(new_row)

    # Handle Remove Filter button click
    elif any(remove_clicks):
        clicked_index = next(
            (i for i, n_clicks in enumerate(remove_clicks) if n_clicks),
            None
        )
        if clicked_index is not None:
            current_children = [
                child for i, child in enumerate(current_children) if i != clicked_index
            ]

    return current_children


@app.callback(
    Output('payment_history', 'children'),
    [
        Input('url', 'pathname'),
        Input({'type': 'filter-column-dropdown', 'index': ALL}, 'value'),
        Input({'type': 'filter-value-input', 'index': ALL}, 'value')
    ],
    [State('currentuserid', 'data')]
)
def updateRecordsTable(pathname, filter_columns, filter_values, currentuserid):
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
            WHERE 1=1 
        """
        # Always true to allow appending AND conditions dynamically

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

        # Apply filter based on the selected column and filter value
    for col, val_filter in zip(filter_columns or [], filter_values or []):
        if col and val_filter:
            if col == 'pay_date':  # Special handling for date columns
                sql += f" AND CAST({col} AS TEXT) ILIKE %s"
            else:
                sql += f" AND {col} ILIKE %s"
            val.append(f'%{val_filter}%')

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

    return payment_table # Return the generated table directly


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