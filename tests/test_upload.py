import pytest
import os
import requests
import json

@pytest.fixture
def url():
    """Create api base url to be used in every test."""
    API_URL = 'http://127.0.0.1:5000/api/v1/user'
    yield API_URL

def test_upload_records_threshold_too_large(url):
    data = {}
    data['threshold'] = (None, '1.5')
    dirpath = os.getcwd()
    data['file'] = ('sample_user_records.csv', open(dirpath + '/app/static/sample_user_records.csv', 'rb'))
    response = requests.post(url + "/records", files=data)
    response_json = json.loads(response.content)
    assert response.status_code == 400 and response_json == 'Only threshold values in range 0.0 - 1.0 are supported'

def test_upload_records_threshold_too_small(url):
    data = {}
    data['threshold'] = (None, '-0.1')
    dirpath = os.getcwd()
    data['file'] = ('sample_user_records.csv', open(dirpath + '/app/static/sample_user_records.csv', 'rb'))
    response = requests.post(url + "/records", files=data)
    response_json = json.loads(response.content)
    assert response.status_code == 400 and response_json == 'Only threshold values in range 0.0 - 1.0 are supported'

def test_upload_records_file_not_csv(url):
    data = {}
    data['threshold'] = (None, '0.5')
    dirpath = os.getcwd()
    data['file'] = ('sample_user_records.txt', open(dirpath + '/app/static/sample_user_records.txt', 'rb'))
    response = requests.post(url + "/records", files=data)
    response_json = json.loads(response.content)
    assert response.status_code == 400 and response_json == 'Only .csv files are supported'

def test_upload_records_file_incorrect_format(url):
    data = {}
    data['threshold'] = (None, '0.5')
    dirpath = os.getcwd()
    data['file'] = ('sample_user_records_incorrect_format.csv', open(dirpath + '/app/static/sample_user_records_incorrect_format.csv', 'rb'))
    response = requests.post(url + "/records", files=data)
    response_json = json.loads(response.content)
    assert response.status_code == 400 and response_json == 'Only .csv files with id, name columns are supported'

def test_upload_records_success(url):
    data = {}
    data['threshold'] = (None, '0.5')
    dirpath = os.getcwd()
    data['file'] = ('sample_user_records.csv', open(dirpath + '/app/static/sample_user_records.csv', 'rb'))
    response = requests.post(url + "/records", files=data)
    response_json = json.loads(response.content)
    assert response.status_code == 200 and 'id' in response_json.keys() and 'status' in response_json.keys()
