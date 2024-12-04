import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.exceptions import PreventUpdate

from app import app

tab1_content = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Spring Break", className="card-text"),
            html.P("Please note that Spring Break will take place from April 1st to April 5th. Classes will resume on April 8th.", className="card-text"),
            html.H5("Enrollment for Next Year", className="card-text"),
            html.P("Enrollment for the 2024-2025 school year is now open! Secure your child's spot by completing the registration forms available on our website.", className="card-text"),
            html.H5("Parent Workshops", className="card-text"),
            html.P("Join us for a series of workshops focused on Montessori education and parenting strategies, starting on March 25th. Details will be sent out via email.", className="card-text"),
        ]
    ),
    className="mt-3",
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Open House", className="card-text"),
            html.P("Join us for our Open House on Saturday, March 15th, from 10 AM to 1 PM. This is a great opportunity for prospective families to tour our classrooms and meet our dedicated staff.", className="card-text"),
            html.H5("January 15, 2024: Winter Parent-Teacher Conferences", className="card-text"),
            html.P("Time: 3:00 PM - 7:00 PM. Location will be at the School Gymnasium", className="card-text"),
            html.H5("February 5, 2024: Montessori Education Week", className="card-text"),
            html.P("A week-long celebration of Montessori education with special activities planned each day.", className="card-text"),
        ]
    ),
    className="mt-3",
)

tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Announcements"),
        dbc.Tab(tab2_content, label="Schedules"),
    ]
)

row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.Div(
                    style={'margin-left': '15px', 'margin-top': '20px', 'padding': '10px'},
                    children=[
                        html.H5(style={'font-weight': 'bold'}, children="Our Mission at Smallville Montessori"),
                        html.P("At Smallville Montessori, we are dedicated to fostering a nurturing and stimulating environment that embodies the principles of the Montessori curriculum as envisioned by Dr. Maria Montessori herself. We believe in self-directed, hands-on learning that empowers children to explore their interests and develop a lifelong love for education."),
                        html.H5(style={'font-weight': 'bold'}, children="Why choose Smallville Montessori?"),
                        html.P("Child-Centered Learning: Our Montessori approach prioritizes the individual needs and interests of each child. We create an environment where children can thrive by nurturing their independence, curiosity, and passion for discovery."),
                        html.P("Inclusive Community: At Smallville Montessori, we celebrate every child's unique journey and learning style. Our classrooms are designed to be inclusive, recognizing that each child brings their own strengths and perspectives."),
                        html.P("Holistic Development: We focus on the holistic development of each child, integrating academic learning with social-emotional growth. Our curriculum encompasses not only core subjects like mathematics and language but also emphasizes practical life skills, sensory experiences, and creative expression through art and music.")
                    ],
                    className='divBorder'
                )),
                dbc.Col(html.Div(tabs,style={'margin-top': '20px'})),
            ]
        ),
    ]
)


# Define the layout variable instead of modifying app.layout directly
layout = html.Div(  # Wrap everything in a Div
    [
        html.Div([
            html.Img(src='/assets/home.png', 
                     style={'width': '100%', 'height': 'auto','padding': '0px 0px'})  # Adjust size as needed
        ]),

                # # Introduction Section
                # html.Div(
                #     style={'margin-left': '15px', 'margin-top': '10px'},
                #     children=[
                #         html.P("In Smallville Montessori, we believe in Montessori curriculum the way Maria Montessori herself practiced her teaching."),
                #         html.P(style={'font-weight': 'bold'}, children="Why choose Smallville Montessori?"),
                #         html.P("Child-Centered Learning: Our Montessori approach nurtures independence, curiosity, and a passion for discovery."),
                #         html.P("Inclusive Community: We celebrate every child's unique journey and learning style."),
                #         html.P("Holistic Development: Focusing on academics, social skills, and emotional growth.")
                #     ]
                # ),

        row,
        #Button
        html.A(
                dbc.Button("Register", color="primary", className="me-1"), href="/student/student_profile",  # Specify the page to redirect to
            style={
                'position': 'absolute',
                'top': '280px',  # Distance from the top of the parent container
                'right': '1100px',  # Distance from the right of the parent container
                'z-index': 1000,  # Ensure it appears above other elements
            }
        ),

                # Footer
                html.Footer(
                    style={
                        'text-align': 'center',
                        'padding': '6px',
                        'background-color': '#003093',
                        # 'position': 'fixed',
                        'bottom': 0,
                        'width': "100%",
                        'margin-top': '500px'
                    },
                    children=[
                        html.P(style={'color': '#f1f1f1'}, children="© 2024 Smallville Montessori")
                    ]
                )
            ]
        )
