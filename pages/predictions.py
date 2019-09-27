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

# Dicitonarys for the values

background_dict = {
    'Outlander': 'Outlander',
    'Acolyte': 'Acolyte',
    'Criminal': 'Criminal',
    'Soldier': 'Soldier'
}

data_column = dbc.Col(
    [
         dcc.Markdown(
            """
        
            ## Predictions
            Use the input menus below to input your character statistics.


            """
        ),
    
    dcc.Markdown('#### Background'),
    dcc.Dropdown(
        id='Background',
        options = [{'label': background_dict[key], 'value': key} for key in background_dict],
        # options = [
        #     {'label': 'Outlander', 'value': 'Outlander'},
        #     {'label': 'Acolyte', 'value': 'Acolyte'},
        #     {'label': 'Criminal', 'value': 'Criminal'},
        #     {'label': 'Soldier', 'value': 'Soldier'},
        # ],
        value = 'Outlander',
        className = 'mb-5',
    )
    ],
)

layout = dbc.Row([data_column, output_column])