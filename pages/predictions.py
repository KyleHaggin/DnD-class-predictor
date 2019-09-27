import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
from joblib import load

from app import app

pipeline = load('assets/pipeline.joblib')

output_column = dbc.Col(
    [
        html.H2('Predicted Class'),
        html.Div(id='predicted-justClass', className='lead')
    ]
)

# Dicitonarys for the values

background_dict = {
    'Outlander': 'Outlander',
    'Acolyte': 'Acolyte',
    'Criminal': 'Criminal',
    'Soldier': 'Soldier',
    'Hermit': 'Hermit',
    'Sailor': 'Sailor',
    'Noble': 'Noble',
    'Folk Hero': 'Folk Hero',
    'Charlatan': 'Charlatan',
    'Far Traveler': 'Far Traveler',
    'Haunted One': 'Haunted One',
    'Sage': 'Sage',
    'Knight': 'Knight',
    'Urban Bounty Hunter': 'Urban Bounty Hunter',
    'Mercenary Veteran': 'Mercenary Veteran',
    'Entertainer': 'Entertainer',
    'Urchin': 'Urchin',
    'Cloistered Scholar': 'Cloistered Scholar',
    'Faction Agent': 'Faction Agent',
    'Barbarian Tribe Member': 'Barbarian Tribe Member',
    'City Watch': 'City Watch',
    'Clan Crafter': 'Clan Crafter',
    'Guild Artisan': 'Guild Artisan',
    'Pirate': 'Pirate',
    'Courtier': 'Courtier',
    'Inheritor': 'Inheritor',
    'Custom': 'Custom/Other'
}

alignment_dict = {
    'LG': 'Lawful Good',
    'NG': 'Neutral Good',
    'CG': 'Chaotic Good',
    'LN': 'Lawful Neutral',
    'NN': 'True Neutral',
    'CN': 'Chaotic Neutral',
    'LE': 'Lawful Evil',
    'NE': 'Neutral Evil',
    'CE': 'Chaotic Evil'
}

race_dict = {
    'Human': 'Human',
    'Elf': 'Elf',
    'Dwarf': 'Dwarf',
    'Half-Elf': 'Half-Elf',
    'Dragonborn': 'Dragonborn',
    'Half-Ork': 'Half-Ork',
    'Tiefling': 'Tiefling',
    'Halfling': 'Halfling',
    'Gnome': 'Gnome',
    'Aasimar': 'Aasimar',
    'Goliath': 'Goliath',
    'Turtle': 'Turtle',
    'Goblin': 'Goblin',
    'Tabaxi': 'Tabaxi',
    'Firbolg': 'Firbolg',
    'Genasi': 'Genasi',
    'Kenku': 'Kenku',
    'Aarakocra': 'Aarakocra',
    'Triton': 'Triton',
    'Lizardfolk': 'Lizardfolk',
    'Kobold': 'Kolbold',
    'Yaun-Ti': 'Yaun-Ti',
    'Ork': 'Ork',
    'Bugbear': 'Bugbear'
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
        id='background',
        options = [{'label': background_dict[key], 'value': key} for key in background_dict],
        value = 'Outlander',
        className = 'mb-5',
    ),

    dcc.Markdown('#### Alignment'),
    dcc.Dropdown(
        id='processedAlignment',
        options = [{'label': alignment_dict[key], 'value': key} for key in alignment_dict],
        value = 'CN',
        className = 'mb-5'
    ),

    dcc.Markdown('#### Race'),
    dcc.Dropdown(
        id ='processedRace',
        options = [{'label': race_dict[key], 'value': key} for key in race_dict],
        value = 'Human',
        className = 'mb-5'
    ),

    dcc.Markdown('#### Level'),
    dcc.Slider(
        id = 'level',
        min = 1,
        max = 20,
        marks = {i: format(i) for i in range(1, 21)},
        value = 1,
        className = 'mb-6'
    ),

    dcc.Markdown('#### Armour Class'),
    dcc.Input(
        id = 'AC',
        placeholder = 'Enter Your Armour Class',
        type = 'number',
        value = 10,
    ),

    dcc.Markdown('#### Hit Points'),
    dcc.Input(
        id = 'HP',
        placeholder = 'Enter Your Maximum Hit Point Value',
        type = 'number',
        value = 10,
        className = 'mb-7'
    ),

    dcc.Markdown('#### Characteristic Scores'),
    dcc.Input(id='Str', type='number', placeholder='Strength'),
    dcc.Input(id='Dex', type='number', placeholder='Dexterity'),
    dcc.Input(id='Con', type='number', placeholder='Constitution'),
    dcc.Input(id='Int', type='number', placeholder='Intelligence'),
    dcc.Input(id='Wis', type='number', placeholder='Wisdom'),
    dcc.Input(id='Cha', type='number', placeholder='Charisma'),

    dcc.Markdown('#### Feats'),
    dcc.RadioItems(
        id = 'has_feats',
        options=[
            {'label': 'Your character does not have feat/s', 'value': False},
            {'label': 'Your character has feat/s', 'value': True}
        ],
        value=False
    ),

    dcc.Markdown('#### Spells'),
    dcc.RadioItems(
        id = 'has_spells',
        options=[
            {'label': 'Your character does not have spells', 'value': False},
            {'label': 'Your character has spells', 'value': True}
        ],
        value=False
    )
    ]
)

@app.callback(
    Output('predicted-justClass', 'children'),
    [
        Input('background', 'value'),
        Input('processedAlignment', 'value'),
        Input('processedRace', 'value'),
        Input('level', 'value'),
        Input('AC', 'value'),
        Input('HP', 'value'),
        Input('Str', 'value'),
        Input('Dex', 'value'),
        Input('Con', 'value'),
        Input('Int', 'value'),
        Input('Wis', 'value'),
        Input('Cha', 'value'),
        Input('has_feats', 'value'),
        Input('has_spells', 'value')
    ],
)
def predict(level, HP, AC, Str, Dex, Con, Int, Wis, Cha, HP_per_level, background, processedAlignment, processedRace, has_spells, has_feats):
    df = pd.DataFrame(
        columns=['level', 'HP', 'AC', 'Str', 'Dex', 'Con', 'Int', 'Wis', 'Cha', 'HP_per_level', 'background', 'processedAlignment', 'processedRace', 'has_spells', 'has_feats'],
        data=[[level, HP, AC, Str, Dex, Con, Int, Wis, Cha, HP_per_level, background, processedAlignment, processedRace, has_spells, has_feats]]
    )
    y_pred = pipeline.predict(df)[0]
    return f'Expected class is {y_pred:10.0f}.'

layout = dbc.Row([data_column, output_column])