"""
====================

Copyright 2022 MET Norway

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import os
import time
import sys
# setting path
sys.path.append('/usr/src/app')

import redis
import json
from celery import Celery
from models.datamodel import DatasetConfig 
# from redis_utility.redis_data import get_data, set_data 


celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")

redis_client = redis.StrictRedis(host='redis', port=6379, db=0)  # Create a Redis client


@celery.task(name="create_task")
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    # Store data
    task_id = create_task.request.id
    data = {"status": False, 'download_token': 'download_token', 'filename': 'filename'}
    json_string = json.dumps(data)
    redis_client.set(task_id, json_string)
    return True

@celery.task(name="create_processing_task")
def create_processing_task(processing_task):
    time.sleep(int(10))
    # Store data
    task_id = create_processing_task.request.id
    # data = {"status": False, 'download_token': 'download_token', 'filename': 'filename'}
    json_string = json.dumps(processing_task)
    redis_client.set(task_id, json_string)
    return True

@celery.task(name="process_data")
def process_data(DatasetConfig: DatasetConfig):
    print(str('start processing'))
    # # set the dataset status to processing itno redis
    # data = {"status": False, 'download_token': 'download_token', 'filename': 'filename'}
    # set_data(
    #     transaction_id='download_token',
    #     data=data,
    #     redishost=os.environ["REDIS_HOST"],
    #     password=os.environ["REDIS_PASSWORD"],
    # )
    # # and start processing the dataset
    # time.sleep(100)
    print(str("completed processing"))
    # store the process resutls into redis and change the status of the task
    print(str(DatasetConfig))
    return True
