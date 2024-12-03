import dash
import dash_bootstrap_components as dbc
from dash import Output, Input, html
from dash.exceptions import PreventUpdate

from app import app
from apps.dbconnect import getDataFromDB

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
                        html.H3('Payment Plan Details')
                    ]
                ),
                dbc.CardBody(  # Define Card Contents
                    [
                        html.Div(  
                            [
                                html.P("/insert payment plan details"),
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
                    href=f'/payment/payment_upload?mode=add',
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
                    [
                        html.Div(  # payment history list
                                id='payment_history'
                        )
                    ]
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
    if pathname != '/students/payment':  # Corrected pathname check
        raise PreventUpdate

    sql = """ 
        SELECT payment_date, payment_num, student_name, payment_plan, invoice_num, proof_link 
        FROM payment 
        WHERE NOT payment_delete_ind
    """
    col = ["Payment Date", "Payment No.", "Student Name", "Plan", "Invoice No.", "Proof"]

    df = getDataFromDB(sql,[], col)

    if df.empty:
        return html.Div("No payment history found.")  # Provide feedback if no records exist

    df['Action'] = [
        html.Div(
            dbc.Button("View", color='warning', size='sm', 
                        href=row["proof_link"], target="_blank"),
            className='text-center'
        ) for idx, row in df.iterrows()
    ]

    # Exclude 'proof' from display and replace with button
    df = df[["Payment Date", "Payment No.", "Student Name", "Plan", "Invoice No.", "Action"]]

    payment_table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
                                              hover=True, size='sm')

    return [payment_table]  # Return the generated table directly
