import pytest
import os
import requests
import json
import time

@pytest.fixture
def url():
    """Create api base url to be used in every test."""
    API_URL = 'http://127.0.0.1:5000/api/v1/user'
    yield API_URL

def test_matches_status_started(url):
    data = {}
    data['threshold'] = (None, '0.5')
    dirpath = os.getcwd()
    data['file'] = ('sample_user_records.csv', open(dirpath + '/app/static/sample_user_records.csv', 'rb'))
    post_response = requests.post(url + "/records", files=data)
    json_post_response = json.loads(post_response.content)

    # Get match process status
    get_response = requests.get(url + "/matches/" + json_post_response['id'])
    json_get_response = json.loads(get_response.content)

    assert get_response.status_code == 200 and (json_get_response['status'] == 'STARTED' or json_get_response['status'] == 'PENDING')

def test_matches_status_matching_in_progress(url):
    data = {}
    data['threshold'] = (None, '0.5')
    dirpath = os.getcwd()
    data['file'] = ('sample_user_records.csv', open(dirpath + '/app/static/sample_user_records.csv', 'rb'))
    post_response = requests.post(url + "/records", files=data)
    json_post_response = json.loads(post_response.content)

    matching_in_progress = False

    # Get match process status
    while not matching_in_progress:
        get_response = requests.get(url + "/matches/" + json_post_response['id'])
        try:
            json_get_response = json.loads(get_response.content)
            if json_get_response['status'] == 'MATCHING_IN_PROGRESS':
                matching_in_progress = True
                assert True
        except json.decoder.JSONDecodeError:
            assert False

def test_matches_status_complete_file(url):
    data = {}
    data['threshold'] = (None, '0.5')
    dirpath = os.getcwd()
    data['file'] = ('sample_user_records.csv', open(dirpath + '/app/static/sample_user_records.csv', 'rb'))
    post_response = requests.post(url + "/records", files=data)
    json_post_response = json.loads(post_response.content)

    complete = False

    # Get result csv one task is complete
    while not complete:
        get_response = requests.get(url + "/matches/" + json_post_response['id'])
        try:
            json_get_response = json.loads(get_response.content)
        except json.decoder.JSONDecodeError:
            complete = True
            # Check new columns have been added
            if get_response.content.decode('latin-1').startswith('id,name,matched_company,matched_company_id'):
                assert get_response.status_code == 200 and True
            else:
                assert get_response.status_code == 200 and False
