import json
import pickle
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import matplotlib.pyplot as plt


""" Example logistic regression dataset
https://sushtend.com/machine-learning/datasets-for-practicing-logistic-regression/
"""

# Global variables
myheading1 = 'Predicting Mortgage Loan Approval'
image1 = 'assets/rocauc.html'
tabtitle = 'Loan Prediction'
sourceurl = 'https://datahack.analyticsvidhya.com/contest/practice-problem-loan-prediction-iii/'
githublink = 'https://github.com/cahn1/503-log-reg-loans-simple/tree/cahn_update1'
approve_color = 'green'

# Load json preformatted graph object
with open('assets/rocauc.json', 'r') as f:
    fig_orig_roocauc = json.load(f)
with open('assets/rocauc_updated.json', 'r') as f:
    fig_updated_rocauc = json.load(f)

# Load correlation pkl heatmap
with open('analysis/feature_importance.pkl', 'rb') as f:
    feature_importance = pickle.load(f)

# Load pkl file
# with open('analysis/loan_approval_logistic_model.pkl', 'rb') as f:
#     orig_model = pickle.load(f)
with open('analysis/loan_approval_logistic_model_update1.pkl', 'rb') as f:
    updated_model = pickle.load(f)


# app server config
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

# Set up Dash layout
app.layout = html.Div([
    html.H1('Logistic Regression', style={
        'textAlign': 'center', 'margin': '48px 0', 'fontFamily': 'system-ui'}),
    dcc.Tabs(id="tabs", children=[
        dcc.Tab(label='Predicting Mortgage Loan Approval', children=[
            html.Div(
                className='six columns',
                children=[
                    dcc.Graph(figure=fig_orig_roocauc, id='fig_orig_roocauc'),
                    html.Hr(),
                    dcc.Graph(figure=fig_updated_rocauc, id='fig_updated_rocauc'),
                    html.Div('Correlation Heatmap'),
                    html.Img(
                        src=app.get_asset_url('corr_loan_heatmap.png'),
                        style={'width': '500px'}
                    ),
                    html.Div([
                        dcc.Graph(figure=feature_importance, id='feature_imp')]),
                ]
            ),
            html.Div(
                className='six columns',
                children=[
                    html.Li('Feature Update'),
                    html.Ul(children=[
                        html.Li('Added Education_map'),
                        html.Li('Replaced ApplicantIncome to CoapplicantIncome'),
                    ]),
                    html.Li('Changed text color based on the approval status.'),
                    html.Hr(),
                    html.Div(
                        className='six columns',
                        children=[
                            html.H3("Features"),
                            html.Div('Credit History:'),
                            dcc.Input(id='Credit_History', value=1, type='number', min=0, max=1, step=1),
                            html.Div('Education:'),
                            dcc.Input(id='Education_map', value=1, type='number', min=0, max=1, step=1),
                            html.Div('Loan Amount (in thousands):'),
                            dcc.Input(id='LoanAmount', value=130, type='number', min=10, max=800, step=10),
                            html.Div('Term (in months)'),
                            dcc.Input(id='Loan_Amount_Term', value=360, type='number', min=120, max=480, step=10),
                            html.Div('CoapplicantIncome Income (in dollars)'),
                            dcc.Input(id='CoapplicantIncome', value=5000, type='number', min=0, max=100000, step=500),
                            html.Div('Probability Threshold for Loan Approval'),
                            dcc.Input(id='Threshold', value=50, type='number', min=0, max=100, step=1),
                        ]
                    ),
                    html.Div(
                        className='three columns',
                        children=[
                            html.H3('Predictions'),
                            html.Div('Predicted Status:'),
                            html.B(children=[
                                html.Div(
                                    id='PredResults',
                                    style={'color': approve_color}),
                            ]),
                            html.Br(),
                            html.Div('Probability of Approval:'),
                            html.Div(id='ApprovalProb'),
                            html.Br(),
                            html.Div('Probability of Denial:'),
                            html.Div(id='DenialProb')
                        ]
                    )
                ]
            ),
        ]),
        dcc.Tab(label='Tab two', children=[
        ]),
    ],
    style={'fontFamily': 'system-ui'},
    content_style={
        'borderLeft': '1px solid #d6d6d6',
        'borderRight': '1px solid #d6d6d6',
        'borderBottom': '1px solid #d6d6d6',
        'padding': '0px'
    },
    parent_style={
        'maxWidth': '1600px',
        'margin': '0 auto'
    })
])


# # evaluate approval status
# def evaluate(rawprob, threshold):
#     return 'Approved', 'green' if int(rawprob) > threshold else 'Denied', 'red'

# callback
@app.callback(
    [
        Output(component_id='PredResults', component_property='children'),
        Output(component_id='PredResults', component_property='style'),
        Output(component_id='ApprovalProb', component_property='children'),
        Output(component_id='DenialProb', component_property='children'),
    ],
    [
        Input(component_id='Credit_History', component_property='value'),
        Input(component_id='Education_map', component_property='value'),
        Input(component_id='LoanAmount', component_property='value'),
        Input(component_id='Loan_Amount_Term', component_property='value'),
        Input(component_id='CoapplicantIncome', component_property='value'),
        Input(component_id='Threshold', component_property='value')
    ])
def prediction_function(
        Credit_History,
        Education_map,
        LoanAmount,
        Loan_Amount_Term,
        CoapplicantIncome,
        Threshold):
    data = [[Credit_History, Education_map, LoanAmount, Loan_Amount_Term,
             CoapplicantIncome]]
    try:
        rawprob = 100 * updated_model.predict_proba(data)[0][1]
        func = lambda y: 'Approved' if int(rawprob) > Threshold else 'Denied'
        formatted_y = func(rawprob)
        approve_color = {'color': '#1abc9c'} if formatted_y == 'Approved' \
            else {'color': '#cb4335'}
        deny_prob = updated_model.predict_proba(data)[0][0] * 100
        formatted_deny_prob = "{:,.2f}%".format(deny_prob)
        app_prob=updated_model.predict_proba(data)[0][1] * 100
        formatted_app_prob = '{:,.2f}%'.format(app_prob)
    except Exception as e:
        print(f'error={e}')
        return "inadequate inputs", "inadequate inputs"
    return formatted_y, approve_color, formatted_app_prob, formatted_deny_prob


if __name__ == '__main__':
    app.run_server(debug=True)