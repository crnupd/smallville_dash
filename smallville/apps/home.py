import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.exceptions import PreventUpdate

from app import app

# Define the layout variable instead of modifying app.layout directly
layout = html.Div(  # Wrap everything in a Div
    [
        html.Main(
            style={'margin-left': '15%', 'padding': '10px'},
            children=[
                html.Header(
                    style={'background-color': '#003093', 'padding': '10px 20px'},
                    children=[
                        html.H1('Smallville Montessori - Katipunan', style={'color': '#f1f1f1'}),
                        html.H3('Welcome User!', style={'color': '#f1f1f1'})
                    ]
                ),
                
                # Introduction Section
                html.Div(
                    style={'margin-left': '15px'},
                    children=[
                        html.H4('/this will display user number and type of user (student or teacher)/'),
                        html.P("In Smallville Montessori, we believe in Montessori curriculum the way Maria Montessori herself practiced her teaching."),
                        html.P(style={'font-weight': 'bold'}, children="Why choose Smallville Montessori?"),
                        html.P("Child-Centered Learning: Our Montessori approach nurtures independence, curiosity, and a passion for discovery."),
                        html.P("Inclusive Community: We celebrate every child's unique journey and learning style."),
                        html.P("Holistic Development: Focusing on academics, social skills, and emotional growth.")
                    ]
                ),

                # Tabs Section
                html.Div(
                    className='tab',
                    children=[
                        html.H2('Enroll Now!'),
                        html.Div(
                            className='btab',
                            children=[
                                html.Button('Announcements', id='announcements-tab', n_clicks=0, className='tablink w3-red'),
                                html.Button('Schedules', id='schedules-tab', n_clicks=0, className='tablink'),
                                html.Button('Grade', id='grade-tab', n_clicks=0, className='tablink')
                            ]
                        ),
                        
                        # Announcements Tab Content
                        html.Div(id='announcements-content', style={'display': 'block'}, children=[
                            html.Table([
                                html.Thead(html.Tr([html.Th("Announcements")])),
                                html.Tbody([
                                    html.Tr([html.Td("Announcement 1")]),
                                    html.Tr([html.Td("Announcement 2")]),
                                    html.Tr([html.Td("Announcement 3")]),
                                    html.Tr([html.Td("Announcement 4")])
                                ])
                            ])
                        ]),

                        # Schedules Tab Content
                        html.Div(id='schedules-content', style={'display': 'none'}, children=[
                            html.Table([
                                html.Thead(html.Tr([html.Th("Schedule")])),
                                html.Tbody([
                                    html.Tr([html.Td("Schedule 1")]),
                                    html.Tr([html.Td("Schedule 2")]),
                                    html.Tr([html.Td("Schedule 3")]),
                                    html.Tr([html.Td("Schedule 4")])
                                ])
                            ])
                        ]),

                        # Grade Tab Content
                        html.Div(id='grade-content', style={'display': 'none'}, children=[
                            html.Table([
                                html.Thead(html.Tr([html.Th("Grade")])),
                                html.Tbody([
                                    html.Tr([html.Td("Grade A")]),
                                    html.Tr([html.Td("Grade B")]),
                                    html.Tr([html.Td("Grade C")]),
                                    html.Tr([html.Td("Grade D")])
                                ])
                            ])
                        ])
                    ]
                ),

                # Footer
                html.Footer(
                    style={
                        'text-align': 'center',
                        'padding': '6px',
                        'background-color': '#003093',
                        'position': 'fixed',
                        'bottom': 0,
                        'width': "calc(100% - 15%)"
                    },
                    children=[
                        html.P(style={'color': '#f1f1f1'}, children="© 2024 Smallville Montessori")
                    ]
                )
            ]
        )
    ]
)