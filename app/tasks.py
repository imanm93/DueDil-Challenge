import os
import csv
import time

from .parser import parse_file
from .match import match
from . import config as Config

# Get Config
application_mode = os.getenv('APPLICATION_MODE', 'DEV')
config = Config.get_config(application_mode)

# Init celery
from celery import Celery
celery = Celery('tasks', backend=config.CELERY_RESULT_BACKEND, broker=config.CELERY_BROKER_URL)

@celery.task(bind=True, name='tasks.generate_matches')
def generate_matches(self, file, min_threshold):
    """
    :param self: Pass in the celery task instance to access task id, status, etc ...
    :param file: User uploaded csv file
    :param min_threshold: User specified threshold for matching algorithm
    :return string: Denoting successful completion of task
    """

    self.update_state(state='STARTED', meta={})
    if config.TESTING: # ONLY FOR TESTING PURPOSES
        time.sleep(1)

    # Parse files
    data = parse_file(file)
    companies = parse_file()

    results = []

    # Start matching process
    for index, item in enumerate(data):
        result = match(item['name'], companies, float(min_threshold))
        results.append({ 'id': item['id'], 'name': item['name'], 'matched_company': result['match_name'], 'matched_company_id': result['match_id'] })
        self.update_state(state='MATCHING_IN_PROGRESS', meta={'current': index, 'total': len(data)})
        if config.TESTING: # ONLY FOR TESTING PURPOSES
            time.sleep(1)

    self.update_state(state='MATCHING_COMPLETE', meta={})

    # Generate csv
    f = open('/api/app/static/matches_' + self.request.id + '.csv', 'w')
    write = csv.writer(f)
    write.writerow(results[0].keys())
    for index, item in enumerate(results):
        write.writerow(item.values())
        self.update_state(state='FILE_IN_CREATION', meta={ 'current': index, 'total': len(results) })
    f.close()

    return 'Matching Completed'
