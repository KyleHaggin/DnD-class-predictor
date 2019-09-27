import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

column = dbc.Col(
    [
    dcc.Markdown(
                """
            
                ## Process


                #### Data description
                *   The data was gotten through on online reddit poll asking people for the statistics of characters.
                *   For analysis I choose to drop duplicates and stay with only the 12 base DnD classes.


                ##### Features:

                This model uses 14 features to makes its predictions. The features were choosen by droping features with too high variance, duplicate columns, and features with leakage of data.
                The reaming features were analysed for cardinality and those with cardinality below 75 were kept for anaylsis.
                *   **level** - The level of the character.
                *   **HP** - The maximum HP of the character.
                *   **AC** - The Armour Class of the character.
                *   **Str** - The Strength score of the character.
                *   **Dex** - The Dexterity score of the character.
                *   **Con** - The Constitustion score of the character.
                *   **Int** - The Intelligence score of the character.
                *   **Wis** - The Wisdom score of the character.
                *   **Cha** - The Charisma score of the character.
                *   **background** - The mechanical background of the character.
                *   **processedAlignment** - The character's alignment on the RPG standard Good/Evil Lawful/Chaotic table.
                *   **processedRace** - The character's base race (subraces stripped from data due to consistancy/reliability of data concerning it being questionable).
                *   **has_spells** - Says wether or not the character has spells available to cast.
                *   **has_feats** - Says wether or not the character gained feats during play.


                ##### Target:
                This model uses the above data to attempt to predict the character class that someone is. The class given would not include subclasses due to a very large number of differnet options and not enough data to ensure that the model would accurate predict such targets.

                #### Beginning with baselines:

                The baseline of the data is first calculated to both give an initial prediction as well as give us a target to reach when determining the accuracy of our data.
                Due to the categorical and non-numeric nature of my target, a mode preditive function was used.

                **Results:** The accuracy of this baseline is: 13.7%
                """
    ),
    html.Img(src='assets/majority_class.png'),
    dcc.Markdown(
                """
                #### Model Selection:
                In this project, I used three models and choose the one with the highest accuracy to continue to improve.


                The first model attempted was a Descision Tree.
                The model achieved a impressive initial accuracy of 42.8%. Unfortunetly, as you will soon see, this fell short of the other models.
                """
    ),
    html.Img(src='assets/val_tree.png'),
    dcc.Markdown(
                """
                One possible reason that this model would've fallen short is its tendency to overpredict certain classes, such as the Cleric.
                """
    ),
    html.Img(src='assets/pred_tree.png'),
    dcc.Markdown(
                """
                The second model attempted was a Random Forest Classifier.
                The model achieved a very good initial accuracy of 67.1%. This is was very close to the top model, but was just barely beaten by our final model.
                """
    ),
    html.Img(src='assets/val_tree.png'),
    dcc.Markdown(
                """
                Our third and final model is the XGB Classifier.
                This best model just eeked out ahead of the Random Forest Classifier with an initial accuracy of 68.4%
                """
    ),
    html.Img(src='assets/val_xgb.png')
    ]
),

layout = dbc.Col(column)