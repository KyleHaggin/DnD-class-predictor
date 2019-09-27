import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

output_column = dbc.Col(
    [

    ],
    md=4,
)

data_column = dbc.Col(
    [
         dcc.Markdown(
            """
        
            ## Predictions
            Use the input menus below to input your character statistics.


            """
        )
    ],
    dbc.Row(
        dbc.Col(
            html.Div([
                
            ])
        )
    )
)

layout = dbc.Row([data_column, output_column])