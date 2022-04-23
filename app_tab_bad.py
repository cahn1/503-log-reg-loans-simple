import json
import pickle
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go


""" Example logistic regression dataset
https://sushtend.com/machine-learning/datasets-for-practicing-logistic-regression/
"""

# Global variables
myheading1 = 'Predicting Mortgage Loan Approval'
image1 = 'assets/rocauc.html'
tabtitle = 'Loan Prediction'
sourceurl = 'https://datahack.analyticsvidhya.com/contest/practice-problem-loan-prediction-iii/'
githublink = 'https://github.com/cahn1/503-log-reg-loans-simple/tree/cahn_update1'

# Load json preformatted graph object
with open('assets/rocauc.json', 'r') as f:
    fig = json.load(f)

# Load pkl file
with open('analysis/loan_approval_logistic_model.pkl', 'rb') as f:
    unpickled_model = pickle.load(f)

# app server config
external_stylesheets = [
    'https://unpkg.com/antd@3.1.1/dist/antd.css',
    'https://rawgit.com/jimmybow/CSS/master/visdcc/DataTable/Filter.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

# Set up Dash layout
# app.layout = html.Div([
#     html.H1('Logistic Regression', style={
#         'textAlign': 'center', 'margin': '48px 0', 'fontFamily': 'system-ui'}),
#     dcc.Tabs(id="tabs", children=[
#         dcc.Tab(label='Predicting Mortgage Loan Approval', children=[
#             html.Div([
#                 html.Div([
#                     dcc.Graph(figure=fig, id='fig1', style={'width': '30%'})
#                 ], className='six columns'),
#                 # html.Div([
#                     html.Div([
#                         html.H3("Features"),
#                         html.Div('Credit History:'),
#                         dcc.Input(id='Credit_History', value=1, type='number', min=0, max=1, step=1),
#                         html.Div('Loan Amount (in thousands):'),
#                         dcc.Input(id='LoanAmount', value=130, type='number', min=10, max=800, step=10),
#                         html.Div('Term (in months)'),
#                         dcc.Input(id='Loan_Amount_Term', value=360, type='number', min=120, max=480, step=10),
#                         html.Div('Applicant Income (in dollars)'),
#                         dcc.Input(id='ApplicantIncome', value=5000, type='number', min=0, max=100000, step=500),
#                         html.Div('Probability Threshold for Loan Approval'),
#                         dcc.Input(id='Threshold', value=50, type='number', min=0, max=100, step=1),
#                     ], className='three columns'),
#                     html.Div([
#                         html.H3('Predictions'),
#                         html.Div('Predicted Status:'),
#                         html.Div(id='PredResults'),
#                         html.Br(),
#                         html.Div('Probability of Approval:'),
#                         html.Div(id='ApprovalProb'),
#                         html.Br(),
#                         html.Div('Probability of Denial:'),
#                         html.Div(id='DenialProb')
#                     ], className='three columns')
#                 # ], className='nine columns'),
#             ], className='twelve columns'),
#             html.Br(),
#             html.A('Code on Github', href=githublink),
#             html.Br(),
#             html.A("Data Source", href=sourceurl),
#         ]),
#         dcc.Tab(label='Tab two', children=[
#             html.Div([
#                 html.H1("This is the content in tab 2"),
#                 html.P("A graph here would be nice!"),
#                 dcc.Graph(
#                     id='example-graph1',
#                     figure={
#                         'data': [
#                             {'x': [1, 2, 3], 'y': [5, 2, 3],
#                              'type': 'barpolar', 'name': 'SF'},
#                             {'x': [1, 2, 3], 'y': [6, 8, 1],
#                              'type': 'barpolar', 'name': u'Montréal'},
#                         ],
#                         'layout': {
#                             'title': '2 Dash Data Visualization'
#                         }
#                     }
#                 )
#             ])
#         ]),
#     ],
#      style={'fontFamily': 'system-ui'},
#      content_style={
#          'borderLeft': '1px solid #d6d6d6',
#          'borderRight': '1px solid #d6d6d6',
#          'borderBottom': '1px solid #d6d6d6',
#          'padding': '20px'
#      },
#      parent_style={
#          'maxWidth': '1600px',
#          'margin': '0 auto'
#      })
# ])
#
#
#


# Set up Dash layout
app.layout = html.Div([
    html.H1('Logistic Regression', style={
        'textAlign': 'center', 'margin': '48px 0', 'fontFamily': 'system-ui'}),
    dcc.Tabs(id="tabs", children=[
        dcc.Tab(label='Predicting Mortgage Loan Approval', children=[
            html.Div(
                className='container',
                children=[
                    html.Div(
                        className='twelve columns',
                        style={'width': '100%'},
                        children=[
                            html.Div(
                                className='',
                                style={'width': '30%'},
                                children=[
                                    html.Div([
                                        dcc.Graph(figure=fig, id='fig1')
                                    ])
                                ]
                            ),
                            html.Div(
                                className='',
                                style={'width': '30%'},
                                children=[
                                    html.Div([
                                        html.H3("Features"),
                                        html.Div('Credit History:'),
                                        dcc.Input(id='Credit_History', value=1, type='number', min=0, max=1, step=1),
                                        html.Div('Loan Amount (in thousands):'),
                                        dcc.Input(id='LoanAmount', value=130, type='number', min=10, max=800, step=10),
                                        html.Div('Term (in months)'),
                                        dcc.Input(id='Loan_Amount_Term', value=360, type='number', min=120, max=480, step=10),
                                        html.Div('Applicant Income (in dollars)'),
                                        dcc.Input(id='ApplicantIncome', value=5000, type='number', min=0, max=100000, step=500),
                                        html.Div('Probability Threshold for Loan Approval'),
                                        dcc.Input(id='Threshold', value=50, type='number', min=0, max=100, step=1),
                                    ]),
                                ]
                            ),
                            html.Div(
                                className='nine columns',
                                children=[
                                    html.Div([
                                        html.H3('Predictions'),
                                        html.Div('Predicted Status:'),
                                        html.Div(id='PredResults'),
                                        html.Br(),
                                        html.Div('Probability of Approval:'),
                                        html.Div(id='ApprovalProb'),
                                        html.Br(),
                                        html.Div('Probability of Denial:'),
                                        html.Div(id='DenialProb')
                                    ])
                                ]
                            ),
                        ]
                    )
                ],
            ),
        ]),
        dcc.Tab(label='Tab two', children=[
            html.Div([
                html.H1("This is the content in tab 2"),
                html.P("A graph here would be nice!"),
                dcc.Graph(
                    id='example-graph1',
                    figure={
                        'data': [
                            {'x': [1, 2, 3], 'y': [5, 2, 3],
                             'type': 'barpolar', 'name': 'SF'},
                            {'x': [1, 2, 3], 'y': [6, 8, 1],
                             'type': 'barpolar', 'name': u'Montréal'},
                        ],
                        'layout': {
                            'title': '2 Dash Data Visualization'
                        }
                    }
                )
            ])
        ]),
    ],
    style={'fontFamily': 'system-ui'},
    content_style={
        'borderLeft': '1px solid #d6d6d6',
        'borderRight': '1px solid #d6d6d6',
        'borderBottom': '1px solid #d6d6d6',
        'padding': '20px'
    },
    parent_style={
        'maxWidth': '1600px',
        'margin': '0 auto'
    })
])


# callback
@app.callback(
    [
        Output(component_id='PredResults', component_property='children'),
        Output(component_id='ApprovalProb', component_property='children'),
        Output(component_id='DenialProb', component_property='children'),
    ],
    [
        Input(component_id='Credit_History', component_property='value'),
        Input(component_id='LoanAmount', component_property='value'),
        Input(component_id='Loan_Amount_Term', component_property='value'),
        Input(component_id='ApplicantIncome', component_property='value'),
        Input(component_id='Threshold', component_property='value')
    ])
def prediction_function(
        Credit_History,
        LoanAmount,
        Loan_Amount_Term,
        ApplicantIncome,
        Threshold):
    data = [[Credit_History, LoanAmount, Loan_Amount_Term, ApplicantIncome]]
    try:
        rawprob = 100 * unpickled_model.predict_proba(data)[0][1]
        func = lambda y: 'Approved' if int(rawprob)>Threshold else 'Denied'
        formatted_y = func(rawprob)
        deny_prob = unpickled_model.predict_proba(data)[0][0] * 100
        formatted_deny_prob = "{:,.2f}%".format(deny_prob)
        app_prob=unpickled_model.predict_proba(data)[0][1] * 100
        formatted_app_prob = '{:,.2f}%'.format(app_prob)
    except Exception as e:
        return "inadequate inputs", "inadequate inputs"
    return formatted_y, formatted_app_prob, formatted_deny_prob


if __name__ == '__main__':
    app.run_server(debug=True)