import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import  metrics  
from sklearn.externals import joblib
from pandas import DataFrame


def onehot(predict_data):
    event_type = pd.read_csv('data/event_type.csv', index_col=0)
    severity_type = pd.read_csv('data/severity_type.csv', index_col=0)
    log_feature = pd.read_csv('data/log_feature.csv', index_col=0)
    resource_type = pd.read_csv('data/resource_type.csv', index_col=0)
    eventTypeVectorized = pd.get_dummies(event_type).groupby(event_type.index).sum()
    logFeatureVectorized = pd.get_dummies(log_feature).groupby(log_feature.index).sum()
    resourceTypeVectorized = pd.get_dummies(resource_type).groupby(resource_type.index).sum()
    severityTypeVectorized = pd.get_dummies(severity_type).groupby(severity_type.index).sum()
    mergedTables = eventTypeVectorized.join(severityTypeVectorized).join(logFeatureVectorized).join(resourceTypeVectorized)
    df = predict_data.join(mergedTables)
    return df

def predict_data(predict_data):
    #predict_data = predict_data.set_index('id')
    decision_tree = joblib.load('model/decision_tree_model.joblib')
    data =predict_data
    predict_data['location'] = [l.replace('location ', '') for l in predict_data['location']]
    predict_data['location'] = predict_data['location'].astype('int')
    predict_data = onehot(predict_data)
    predict = decision_tree.predict(predict_data)
    pred = pd.DataFrame(predict, columns = ['predict_disruptions'])
    a = data.index
    pred = pred.set_index(a)
    submission = pd.concat([data, pred], axis =1)

    result = submission[:0]
    result['id'] = submission.index
    result = result.drop('location', 1)
    result = result.drop('predict_disruptions', 1)
    result['location'] = list(submission['location'])
    result['predict_disruptions'] = list(submission['predict_disruptions'])
    result = DataFrame(result, columns= result.columns)
    network_csv = result.to_csv (r'data/submission.csv', index = None, header=True)
    return submission
