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
from models.datamodel import DatasetConfig, SearchObject
# from redis_utility.redis_data import get_data, set_data 
import xarray as xr
import numpy as np
from pathlib import Path



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
def process_data(DatasetConfig_dict):
    
    print(DatasetConfig_dict)
    
    # Get the value of the environment variable DOWNLOAD_DIR
    download_dir = os.environ.get('DOWNLOAD_DIR')

    # If the environment variable is not set, you might want to handle it
    if download_dir is None:
        raise ValueError("DOWNLOAD_DIR environment variable is not set")
    
    task_id = process_data.request.id
    dcf = DatasetConfig()
    dcf.url = DatasetConfig_dict['url']
    dcf.variables = DatasetConfig_dict['variables']
    
    print(str('start processing'))
    ds = xr.open_dataset(dcf.url, decode_times=dcf.decoded_time)
    time_coord = [i for i in ds.coords if ds.coords.dtypes[i] == np.dtype('<M8[ns]')]
    time_dim = time_coord[0]

    if len(time_coord) != 0:
        dcf.decoded_time = True
    else:
        dcf.decoded_time = False
    dcf.time_range = [DatasetConfig_dict['time_range'][0], DatasetConfig_dict['time_range'][1]]
    dcf.is_resampled = False


    data_selected = {}
    if dcf.decoded_time:
        for time_dim in time_coord:
            data_selected[time_dim] = ds[dcf.variables].sel({time_dim: slice(dcf.time_range[0], 
                                                                                       dcf.time_range[1])})
        merged_dataset = xr.merge(data_selected.values())
    else:
        merged_dataset = ds[dcf.variables]
    if dcf.is_resampled:
        pass
    if dcf.output_format == 'csv':
        pass
    else:
        # filename = f"{os.getenv('DOWNLOAD_DIR')}/{time_dim}_selected_data.nc"
        # File name string
        # filename = f"{time_dim}_selected_data.nc"
        filename = DatasetConfig_dict['filename']
        # Construct the path using pathlib
        file_path = Path(download_dir) / filename
        print("filename : ", filename)
        print(f"attempting to save the dataset as netcdf file... in {file_path}")
        try:
            # merged_dataset.to_netcdf(f"{os.getenv('DOWNLOAD_DIR')}/{time_dim}_selected_data.nc")
            merged_dataset.to_netcdf(file_path)
        except ValueError:
            print("attempting to save the dataset as netcdf file... with encoding...in {os.getenv('DOWNLOAD_DIR')}/{time_dim}_selected_datca.nc")
            encoding = {i:{'_FillValue': np.nan} for i in ds[dcf.variables]}
            # merged_dataset.to_netcdf(f"{os.getenv('DOWNLOAD_DIR')}/{time_dim}_selected_datca.nc", encoding=encoding)
            merged_dataset.to_netcdf(file_path, encoding=encoding)
    # redis_client.set(task_id, json_string)
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
    print(str(dcf))
    return True



@celery.task(name="csw_search")
def csw_search(SearchObject_dict):
    print(SearchObject_dict)
    return True