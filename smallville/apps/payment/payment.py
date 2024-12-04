import dash
import dash_bootstrap_components as dbc
from dash import Output, Input,dcc, html
from dash.exceptions import PreventUpdate

from app import app
from apps.dbconnect import getDataFromDB

table_header = [
    html.Thead(html.Tr([html.Th("PLAN"), html.Th("Amount per Payment (in pesos)"),  html.Th("Total to Pay (in pesos)")]))
]

row1 = html.Tr([html.Td("Monthly"), html.Td("6,125.00"), html.Td("73,500")])
row2 = html.Tr([html.Td("Quarterly"), html.Td("18,025.00"), html.Td("72,100")])
row3 = html.Tr([html.Td("Yearly"), html.Td("70,000"), html.Td("70,000")])

table_body = [html.Tbody([row1, row2, row3])]

table = dbc.Table(table_header + table_body, bordered=True)

layout = html.Div(
    [
        # Page Header
        html.Div(
            [
                html.H2('Payment Page'),
                html.Hr(),
            ],
            style={'margin-top': '60px'}  # Adjust margin to avoid overlap with navbar
        ),
        dbc.Card(  # Card Container
            [
                dbc.CardHeader(  # Define Card Header
                    [
                        html.H3("Payment Plans")
                    ]
                ),
                dbc.CardBody(  # Define Card Contents
                    [
                        html.Div(  
                            [
                                table,
                                html.H5("Payment Plan Details"),
                                html.P("Total Tuition Fee: 70,000 pesos"),
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
                    [
                        html.H3('Payment History')
                    ]
                ),
                dbc.CardBody(  # Define Card Contents
                        html.Div(id='payment_history') # payment history list
                )
            ]
        )
    ]
)

@app.callback(
    Output('payment_history', 'children'),
    [Input('url', 'pathname')]
)
def updateRecordsTable(pathname):
    if pathname != '/student/payment':  # Corrected pathname check
        raise PreventUpdate

    sql = """ 
        SELECT stud_name, pay_plan, pay_num, pay_date, pay_method, pay_proof 
        FROM payment 
    """
    val = []
    col = ["Student Name", "Plan", "Reference No.","Payment Date", "Payment Method", "Proof"]

    df = getDataFromDB(sql, val, col)

    if df.empty:
        return html.Div("No payment history found.")  # Provide feedback if no records exist

    df['Action'] = [
        html.Div(
            dbc.Button("View", color='warning', size='sm', 
                        href=row["pay_proof"]),
            className='text-center'
        ) for idx, row in df.iterrows()
    ]

    # Exclude 'proof' from display and replace with button
    df = df[["Student Name", "Plan", "Reference No.","Payment Date", "Payment Method", "Action"]]

    payment_table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
                                              hover=True, size='sm')

    return [payment_table]  # Return the generated table directly



