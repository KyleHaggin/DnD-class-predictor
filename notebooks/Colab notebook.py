# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'
#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
# ms-python.python added
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'notebooks'))
	print(os.getcwd())
except:
	pass
#%%
from IPython import get_ipython

#%% [markdown]
# <a href="https://colab.research.google.com/github/KyleHaggin/DnD-class-predictor/blob/master/Models_and_Work.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>
#%% [markdown]
# Lambda School Data Science, Unit 2: Predictive Modeling
# 
# # Applied Modeling, Module 2
# 
# You will use your portfolio project dataset for all assignments this sprint.
# 
# ## Assignment
# 
# Complete these tasks for your project, and document your work.
# 
# - [ ] Plot the distribution of your target. 
#     - Classification problem: Are your classes imbalanced? Then, don't use just accuracy.
#     - Regression problem: Is your target skewed? If so, let's discuss in Slack.
# - [ ] Continue to clean and explore your data. Make exploratory visualizations.
# - [ ] Fit a model. Does it beat your baseline?
# - [ ] Try xgboost.
# - [ ] Get your model's permutation importances.
# 
# You should try to complete an initial model today, because the rest of the week, we're making model interpretation visualizations.
# 
# 
# ## Reading
# 
# Top recommendations in _**bold italic:**_
# 
# #### Permutation Importances
# - _**[Kaggle / Dan Becker: Machine Learning Explainability](https://www.kaggle.com/dansbecker/permutation-importance)**_
# - [Christoph Molnar: Interpretable Machine Learning](https://christophm.github.io/interpretable-ml-book/feature-importance.html)
# 
# #### (Default) Feature Importances
#   - [Ando Saabas: Selecting good features, Part 3, Random Forests](https://blog.datadive.net/selecting-good-features-part-iii-random-forests/)
#   - [Terence Parr, et al: Beware Default Random Forest Importances](https://explained.ai/rf-importance/index.html)
# 
# #### Gradient Boosting
#   - [A Gentle Introduction to the Gradient Boosting Algorithm for Machine Learning](https://machinelearningmastery.com/gentle-introduction-gradient-boosting-algorithm-machine-learning/)
#   - _**[A Kaggle Master Explains Gradient Boosting](http://blog.kaggle.com/2017/01/23/a-kaggle-master-explains-gradient-boosting/)**_
#   - [_An Introduction to Statistical Learning_](http://www-bcf.usc.edu/~gareth/ISL/ISLR%20Seventh%20Printing.pdf) Chapter 8
#   - [Gradient Boosting Explained](http://arogozhnikov.github.io/2016/06/24/gradient_boosting_explained.html)
#   - _**[Boosting](https://www.youtube.com/watch?v=GM3CDQfQ4sw) (2.5 minute video)**_

#%%
import os, sys
in_colab = 'google.colab' in sys.modules

# If you're in Colab...
if in_colab:
    # Pull files from Github repo
    os.chdir('/content')
    get_ipython().system('git init .')
    get_ipython().system('git remote add origin https://github.com/LambdaSchool/DS-Unit-2-Applied-Modeling.git')
    get_ipython().system('git pull origin master')
    # Install packages in Colab
    get_ipython().system('pip install category_encoders==2.0.0')
    get_ipython().system('pip install eli5==0.10.1')
    get_ipython().system('pip install pandas-profiling==2.3.0')
    get_ipython().system('pip install pdpbox==0.2.0')
    get_ipython().system('pip install plotly==4.1.1')
    get_ipython().system('pip install shap==0.30.0')
    
    # Install required python packages
    get_ipython().system('pip install -r requirements.txt')
    
    # Change into directory for module
    os.chdir('module2')


#%%
# import important libraries
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import category_encoders as ce 
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score
import eli5
from eli5.sklearn import PermutationImportance


#%%
# import the dataset
df = pd.read_csv('https://raw.githubusercontent.com/oganm/dndstats/master/docs/uniqueTable.tsv',
                 sep='\t')


#%%
# double check the import worked correctly
df.head()


#%%
# create a has spells feature

# create a function that returns true if there is a spell or false if there is not
def check_spells(item):
  # check if the value is a float. This works because np.nan is a float value and the value will be a string if there are spells
  if isinstance(item, float):
    # if nan is found return false (no spells)
    return False
  else:
    # else return true (spell found)
    return True

# apply the function to the dataframe
df['has_spells'] = df['processedSpells'].apply(check_spells)


#%%
df.head()


#%%
# create a has feat feature

# create a function that returns true if it has a feat and false if there is not
def check_feats(item):
  if isinstance(item, float):
    return False
  else:
    return True

# apply the function to the dataframe
df['has_feats'] = df['feats'].apply(check_feats)


#%%
# create a HP per level feature
df['HP_per_level'] = df['HP'] / df['level']


#%%
df.head()


#%%
# drop uneeded columns due to high randomness or high variance
drop_columns_variance = ['name', 'date', 'day']
df = df.drop(columns = drop_columns_variance)

# drop columns due to leakage
drop_columns_leak = ['subclass', 'class']
df = df.drop(columns = drop_columns_leak)

# drop columns due to duplication
drop_columns_dup = ['race']
df = df.drop(columns = drop_columns_dup)

# check the head
df.head()


#%%
df['justClass'].value_counts()


#%%
# get our target
target = 'justClass'
targetAllowed = ['Fighter', 'Rogue', 'Cleric', 'Barbarian', 'Paladin', 'Ranger', 'Sorcerer', 'Wizard', 'Monk', 'Druid', 'Bard', 'Warlock']


#%%
# df = df[df[target] targetAllowed]
df = df.loc[df[target].isin(targetAllowed)]


#%%
df['justClass'].value_counts()


#%%
# get our features
train_features = df.drop(columns=target)
numeric_features = train_features.select_dtypes(include='number').columns.tolist()
cardinality = train_features.select_dtypes(exclude='number').nunique()
categorical_features = cardinality[cardinality <= 75].index.tolist()
features = numeric_features + categorical_features


#%%
features


#%%
# majority class check
majority_class = df[target].mode()
print('Majority class is', majority_class)
y_pred = [majority_class] * len(df)
accuracy_score(df[target], y_pred)


#%%
# train test split the data (80/20)
train, val = train_test_split(df, train_size=0.80, test_size=.20,
                               stratify=df[target], random_state=42)


#%%
X_train = train[features]
y_train = train[target]
X_val = val[features]
y_val = val[target]


#%%
# fit a pipeline (Decision Tree)
pipelineTree = make_pipeline(
    ce.OneHotEncoder(use_cat_names=True),
    SimpleImputer(strategy='mean'),
    StandardScaler(),
    DecisionTreeClassifier(max_depth=3)
)

pipelineTree.fit(X_train, y_train)


#%%
# validation accuracy (Decision Tree)
y_pred_tree = pipelineTree.predict(X_val)
print('Validation Accuracy', accuracy_score(y_val, y_pred_tree))


#%%
y_pred_tree


#%%
# fit a pipeline (Random Forest)
pipelineForest = make_pipeline(
    ce.OneHotEncoder(use_cat_names=True),
    SimpleImputer(strategy='mean'),
    StandardScaler(),
    RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=-1)
)

pipelineForest.fit(X_train, y_train)


#%%
y_pred_forest = pipelineForest.predict(X_val)
print('Validation Accuracy', accuracy_score(y_val, y_pred_forest))


#%%
y_pred_forest


#%%
transformers = make_pipeline(
    ce.OneHotEncoder(use_cat_names=True),
    SimpleImputer(strategy='mean'),
    StandardScaler()
)

# tranform the data
X_train_transformed = transformers.fit_transform(X_train)
X_val_transformed = transformers.transform(X_val)

eval_set = [(X_train_transformed, y_train),
            (X_val_transformed, y_val)]


#%%
# model = RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=-1)
# model.fit(X_train_transformed, y_train)


#%%



#%%
model = XGBClassifier(n_estimators=1000, n_jobs=-1)
model.fit(X_train_transformed, y_train, eval_set=eval_set, early_stopping_rounds=10)


#%%
# Validation accuracy
y_pred = model.predict(X_val_transformed)
print('Validation Accuracy', accuracy_score(y_val, y_pred))


#%%
y_pred


#%%
# permuter = PermutationImportance(
#     model, 
#     scoring='accuracy',
#     n_iter=3,
#     random_state=42
# )

# permuter.fit(X_val_transformed, y_val)
# feature_names = X_val.columns.tolist()

# eli5.show_weights(
#     permuter,
#     top=None, # show importance of all features
#     feature_names=feature_names
# )


#%%
# the row to anaylze in the shaply plot
# change the number in row to find the shaply value
row = 25
row = X_train.iloc[[row]]


#%%
# import shap

# explainer = shap.TreeExplainer(model)
# row_processed = transformers.transform(row)
# shap_values = explainer.shap_values(row_processed)

# shap.initjs()
# shap.force_plot(
#     base_value=explainer.expected_value,
#     shap_values=shap_values,
#     features=row
# )


#%%



#%%



