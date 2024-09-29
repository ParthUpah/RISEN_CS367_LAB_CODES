import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import CategoricalNB
from sklearn.metrics import accuracy_scorea
from pgmpy.models import BayesianNetwork
from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.inference import VariableElimination
# loading the data
dataset = pd.read_csv("2020_bn_nb_data.txt", delimiter="\t") 
print(dataset)
# define structure of the bayesian network
bayes_model = BayesianNetwork([
    ('EC100', 'EC160'), 
    ('IT101', 'IT161'), 
    ('MA101', 'PH100'), 
    ('PH100', 'PH160'), 
    ('MA101', 'HS101'), 
    ('IT101', 'HS101')
])
bayes_model.fit(dataset, estimator=MaximumLikelihoodEstimator)
for cpd in bayes_model.get_cpds():
    print(f"CPD of {cpd.variable}:\n{cpd}")

# create an inference object
inference_engine = VariableElimination(bayes_model)
query_result = inference_engine.map_query(['PH100'], evidence={'EC100': 'DD', 'IT101': 'CC', 'MA101': 'CD'})
print("Predicted grade for PH100:", query_result['PH100'])

# function to map categorical grades to numerical values
def map_grades(x):
    grade_mapping = {'AA': 0, 'AB': 1, 'BB': 2, 'BC': 3, 'CC': 4, 'CD': 5, 'DD': 6, 'F': 7, 'y': 1, 'n': 0}
    return grade_mapping.get(x, x)
# apply mapping function to the dataset
dataset = dataset.applymap(map_grades)
# split features and target
features = dataset.drop(columns=['QP'])  # assuming 'Internship' is the last column
target = dataset['QP']
print("Unique values in each column:")
for column in dataset.columns:
    print(f"{column}: {dataset[column].unique()}")
# conduct 20 iterations for accuracy calculation
accuracy_list = []
print(dataset.isnull().sum())
for iteration in range(20):
    # separate features and target
    X = dataset.drop(columns=['QP'])
    y = dataset['QP']
    # split into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # verify data types
    X_train = X_train.astype(int)
    X_test = X_test.astype(int)

    # initialize and fit the model
    naive_bayes_model = CategoricalNB(min_categories=8)
    naive_bayes_model.fit(X_train, y_train)

    # predict on the test data
    try:
        y_pred = naive_bayes_model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        accuracy_list.append(accuracy)
    except IndexError as error:
        print(f"IndexError encountered: {error}")
        print("Test Data:\n", X_test.head())
        accuracy = accuracy_score(y_test, y_pred)
        print(accuracy)

average_accuracy = np.mean(accuracy_list)
print(f"Average accuracy over 20 runs: {average_accuracy * 100:.2f}%")

#predict internship status for test data using Variable Elimination
dependent_accuracy_list = []

for iteration in range(20):
    X = dataset.drop(columns=['QP'])
    y = dataset['QP']

    #split into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    dependent_bayes_model = BayesianNetwork([
        ('EC100', 'QP'), 
        ('IT101', 'QP'), 
        ('MA101', 'QP'), 
        ('PH100', 'QP'), 
        ('MA101', 'QP'), 
        ('IT101', 'QP'),
        ('EC160', 'QP'),
        ('IT161', 'QP'),
        ('PH160', 'QP'),
        ('HS101', 'QP')
    ])

    print("yes")
    # fit the model with CPTs using Maximum Likelihood Estimation
    dependent_bayes_model.fit(pd.concat([X_train, y_train], axis=1), estimator=MaximumLikelihoodEstimator)
    
    # verify data types
    X_train = X_train.astype(int)
    X_test = X_test.astype(int)
    print(iteration)
    
    # fit model on training data
    dependent_bayes_model.fit(pd.concat([X_train, y_train], axis=1), estimator=MaximumLikelihoodEstimator)
    
    inference_engine = VariableElimination(dependent_bayes_model)
    y_pred = [inference_engine.map_query(['QP'], evidence=row.to_dict())['QP'] for _, row in X_test.iterrows()]
    
    accuracy = accuracy_score(y_test, y_pred)
    dependent_accuracy_list.append(accuracy)

average_dependent_accuracy = np.mean(dependent_accuracy_list)
print(f"Average accuracy over 20 runs (dependent model): {average_dependent_accuracy * 100:.2f}%")
