from flask import Flask, render_template, url_for, request
import pandas as pd
from model import predict
from flask import config

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def getIndex():
    if request.method == 'GET':
        test = pd.read_csv('data/test1.csv')
        event_data = pd.read_csv('data/event_type1.csv')
        feature_data = pd.read_csv('data/log_feature1.csv')
        resource_data = pd.read_csv('data/resource_type1.csv')
        severity_data = pd.read_csv('data/severity_type1.csv')

        test_fieldnames = test.columns.values
        test_id = list(test['id'].value_counts())
        test_location = list(test['location'].value_counts())
        test1 = test
        test1['location'] = [l.replace('location ', '')
                             for l in test1['location']]
        test1['location'] = test1['location'].astype('int')
        #corr = corr.sort_values(ascending=False)
        # location
        location = test1['location'].value_counts()
        location = pd.DataFrame.sort_index(location, ascending=True, axis=0)
        labels_location = location.index.values
        values_location = location.values

        # event
        event1 = event_data
        event1['event_type'] = [
            l.replace('event_type ', '') for l in event1['event_type']]
        event1['event_type'] = event1['event_type'].astype('int')
        event = event1['event_type'].value_counts()
        event = pd.DataFrame.sort_index(event, ascending=True, axis=0)
        labels_event = event.index.values
        values_event = event.values
        event_fieldnames = event_data.columns.values

        # feature
        feature1 = feature_data
        feature1['log_feature'] = [
            l.replace('feature ', '') for l in feature1['log_feature']]
        feature1['log_feature'] = feature1['log_feature'].astype('int')
        feature = feature1['log_feature'].value_counts()
        feature = pd.DataFrame.sort_index(feature, ascending=True, axis=0)
        labels_feature = feature.index.values
        values_feature = feature.values
        feature_fieldnames = feature_data.columns.values

        # resource
        resource1 = resource_data
        resource1['resource_type'] = [
            l.replace('resource_type ', '') for l in resource1['resource_type']]
        resource1['resource_type'] = resource1['resource_type'].astype('int')
        resource = resource1['resource_type'].value_counts()
        resource = pd.DataFrame.sort_index(resource, ascending=True, axis=0)
        labels_resource = resource.index.values
        values_resource = resource.values
        resource_fieldnames = resource_data.columns.values

        # severity
        severity1 = severity_data
        severity1['severity_type'] = [
            l.replace('severity_type ', '') for l in severity1['severity_type']]
        severity1['severity_type'] = severity1['severity_type'].astype('int')
        severity = severity1['severity_type'].value_counts()
        severity = pd.DataFrame.sort_index(severity, ascending=True, axis=0)
        labels_severity = severity.index.values
        values_severity = severity.values
        severity_fieldnames = severity_data.columns.values

        return render_template('index.html', test_fieldnames=test_fieldnames, event_fieldnames=event_fieldnames, feature_fieldnames=feature_fieldnames, data=test, event_data=event_data,
                               labels_location=labels_location, values_location=values_location, labels_event=labels_event, values_event=values_event, labels_feature=labels_feature, values_feature=values_feature,
                               labels_resource=labels_resource, values_resource=values_resource, resource_fieldnames=resource_fieldnames, resource_data=resource_data, labels_severity=labels_severity,
                               values_severity=values_severity, severity_fieldnames=severity_fieldnames, severity_data=severity_data, feature_data=feature_data, results_location=test_location, results_id=test_id, len=len)


@app.route('/predict')
def predict_test():
    test = pd.read_csv('data/test1.csv', index_col=0)   
    submission = predict.predict_data(test)
    test = pd.read_csv('data/submission.csv')
    test_fieldnames = test.columns.values
    test_id = list(test['id'].value_counts())
    test_location = list(test['location'].value_counts())
    test1 = test
    # test1['location'] = [l.replace('location ', '')
    #                      for l in test1['location']]
    # test1['location'] = test1['location'].astype('int')    
    location = test1['location'].value_counts()
    location = pd.DataFrame.sort_index(location, ascending=True, axis=0)
    labels_location = location.index.values
    values_location = location.values
    predict_disruptions = test['predict_disruptions'].value_counts()
    labels_predict = predict_disruptions.index.values
    values_predict = predict_disruptions.values

    return render_template('predict.html',test_fieldnames=test_fieldnames,labels_location=labels_location,values_location=values_location,data=test,
    labels_predict=labels_predict,values_predict=values_predict,results_location=test_location, results_id=test_id, len = len)


if __name__ == "__main__":
    app.run(debug=True)
   