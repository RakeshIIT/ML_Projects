# -*- coding: utf-8 -*-
"""Breast Cancer Detection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Zvwkx6-M_4vQ_gXc2q1SNWFIdbmZTm9T
"""

import sys
import scipy
import numpy
import matplotlib
import pandas
import sklearn
import os
import seaborn as sns
os.getcwd()
#print('Python: {}'.format(sys.version))
#print('scipy: {}'.format(scipy.__version__))
#print('numpy: {}'.format(numpy.__version__))
#print('matplotlib: {}'.format(matplotlib.__version__))
#print('pandas: {}'.format(pandas.__version__))
#print('sklearn: {}'.format(sklearn.__version__))

import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import cross_validate
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
import pandas as pd

url = "https://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer-wisconsin/breast-cancer-wisconsin.data"
names = ['id', 'clump_thickness', 'uniform_cell_size', 'uniform_cell_shape',
       'marginal_adhesion', 'single_epithelial_size', 'bare_nuclei',
       'bland_chromatin', 'normal_nucleoli', 'mitoses', 'class']
df = pd.read_csv(url, names=names)
df.head(11)

df.isnull().sum() #no null values found

df.replace('?',-99999, inplace=True)
df.drop(['id'], axis=1, inplace=True) #dropping the ID column
print(df.axes)

df['class'].value_counts() #We have two classes 2 and 4. Here 2 refers to non-malign cells and 4 refers to malign cells
sns.countplot(df['class'])

#Now we have an imabalanced dataset. The dataset have to be balanced for the model to perform better

# Put all the fraud class in a separate dataset.
malign_df = df.loc[df['class'] == 4] 

#Randomly select 492 observations from the non-fraud (majority class)
non_malign_df = df.loc[df['class'] == 2].sample(n=malign_df.shape[0],random_state=42)

# Concatenate both dataframes again
final_df = pd.concat([malign_df, non_malign_df])

"""## Now we have a balanced dataset"""

sns.countplot(final_df['class'])

# Describe the dataset
print(final_df.describe())

final_df.hist(figsize = (10, 10))
plt.show()

scatter_matrix(final_df, figsize = (18,18))
plt.show()

X = np.array(final_df.drop(['class'], 1)) #depended variables
y = np.array(final_df['class']) #predictor variable

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test=train_test_split(X,y,test_size=0.2)

seed = 42
scoring = 'accuracy'

from sklearn.linear_model import LogisticRegression

models = []
models.append(('KNN', KNeighborsClassifier(n_neighbors = 5)))
models.append(('SVM', SVC(kernel='linear')))
models.append(('Logistic Regression',LogisticRegression()))
results = {}
names = []

for name, model in models:
    model.fit(X_train, y_train)
    predictions = model.predict(X_train)
    accuracy=accuracy_score(y_train, predictions)*100
    results[name]=accuracy
    print(name)
    print("{0:0.2f}%".format(accuracy))
    print(classification_report(y_train, predictions))

results

results_df=pd.DataFrame(list(results.items()),columns=['Model','Accuracy']).sort_values(by='Accuracy',ascending=False)
results_df



"""##Note this is a very simple model and a very small dataset is considered. This notebook is created to learn and implement the basics of data scienct project. In real life datasets achieve these high accracies are very difficult and needs lot of data preprocessing and hyperparameter tuning.

Thank you....
"""