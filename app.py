import random
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table
import plotly.express as px
import pandas as pd
import numpy as np

from dash.dependencies import Input, Output

quick_tip = list(range(1, 13))
quick_tip_default = '3'
index_lottery = list(range(1,1001))
index_lottery_default = '6'

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

def generate_numbers(value, value_lottery):
    lottery = np.random.choice(np.arange(1, 50), size=(value_lottery, value))
    df = pd.DataFrame(lottery, columns=[f'lottery_{i}' for i in range(1, value+1)])
    df.index +=1
    return df

# ------------------------------------------------------------------------------
# App layout
app.layout = dbc.Container(
    [
        html.H1("Dashboard lottery numbers"),
        html.P("This application shows you the random numbers for the lottery. 3 quick tips and 6 random numbers are selected as default. You can set this as you like with the dropdowns."),
        html.Div([
            html.P('Please select your quick tip: 1-12'),   
            dcc.Dropdown(
                id = 'dropdown_quicktip',
                options = [{'label':i, 'value':i} for i in quick_tip],
                value = quick_tip_default, 
                style={'width': '50%'},
                clearable=False
            ),
        
            html.P('And your lucky numbers: 1-1000'),
            dcc.Dropdown(
                id = 'dropdown_index_lottery',
                options = [{'label':i, 'value':i} for i in index_lottery],
                value = index_lottery_default, 
                style={'width': '50%'},
            ),
        ]),
        html.Br(),
        html.Div(
            dbc.Alert(id='container-button-basic',
                    children='',
                    color='success'
            ),
        ),
        dcc.Graph(id='graph'),
        dash_table.DataTable(
            id='datatable',
            style_cell={'textAlign': 'center'},
            style_as_list_view=True,
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                }
            ],
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
            },
            sort_action='native',
            style_table={'overflowX': 'auto'},
        )
    ]
)

# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    Output('container-button-basic', 'children'),
    Output('graph', 'figure'),
    Output('datatable', 'data'),
    Output('datatable', 'columns'),
    [Input('dropdown_quicktip', 'value'),
    Input('dropdown_index_lottery', 'value')]
)

def update_output(value_quicktip, value_index_lottery):
    
    df_numbers = generate_numbers(int(value_quicktip), int(value_index_lottery))

    label = 'Here are your lucky numbers: ' + df_numbers.to_string(index=False, header=False)

    fig = px.scatter(df_numbers, title="Lottery numbers")

    data = df_numbers.to_dict('records')

    columns=[{"name": i, "id": i} for i in df_numbers.columns]

    return label, fig, data, columns

# ------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run_server(debug=True)