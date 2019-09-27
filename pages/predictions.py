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
        id='Background',
        options = [{'label': background_dict[key], 'value': key} for key in background_dict],
        value = 'Outlander',
        className = 'mb-5',
    ),

    dcc.Markdown('#### Alignment'),
    dcc.Dropdown(
        id='Alignment',
        options = [{'label': alignment_dict[key], 'value': key} for key in alignment_dict],
        value = 'CN',
        className = 'mb-5'
    ),

    dcc.Markdown('#### Race'),
    dcc.Dropdown(
        id ='Background',
        options = [{'label': race_dict[key], 'value': key} for key in race_dict],
        value = 'Human',
        className = 'mb-5'
    ),

    dcc.Markdown('#### Level'),
    dcc.Slider(
        min = 1,
        max = 20,
        marks = {i: format(i) for i in range(1, 21)},
        value = 1,
        className = 'mb-6'
    ),

    dcc.Markdown('#### Hit Points'),
    dcc.Input(
        placeholder = 'Enter Your Maximum Hit Point Value',
        type = 'number',
        value ='10',
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
        options=[
            {'label': 'Your character does not have feat/s', 'value': False},
            {'label': 'Your character has feat/s', 'value': True}
        ],
        value=False
    ),

    dcc.Markdown('#### Spells'),
    dcc.RadioItems(
        options=[
            {'label': 'Your character does not have spells', 'value': False},
            {'label': 'Your character has spells', 'value': True}
        ],
        value=False
    )
    ],


)

layout = dbc.Row([data_column, output_column])