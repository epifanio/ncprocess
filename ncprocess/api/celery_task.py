import sys
# setting path
sys.path.append('/usr/src/app')

from celery.result import AsyncResult
from worker import create_task, process_data, create_processing_task
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter
from fastapi import Body, FastAPI, Form, Request
from models.datamodel import DatasetConfig
import redis
import json

router = APIRouter()
templates = Jinja2Templates(directory="/usr/src/app/templates")

redis_client = redis.StrictRedis(host='redis', port=6379, db=0)  # Create a Redis client


@router.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", context={"request": request})


@router.post("/tasks", status_code=201)
def run_task(payload = Body(...)):
    task_type = payload["type"]
    task = create_task.delay(int(task_type))
    return JSONResponse({"task_id": task.id})


@router.post("/tasks_model", status_code=201)
def run_task(payload : DatasetConfig):
    payload_dict = payload.dict()
    # task_duration = payload_dict["duration"]
    task = create_processing_task.delay(payload_dict)
    return JSONResponse({"task_id": task.id})


@router.get("/celery_tasks/{task_id}")
def get_celery_task_status(task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": str(task_id),
        "task_status": str(task_result.status),
        "task_result": str(task_result.result)
    }
    return JSONResponse(result)


@router.get("/tasks/{task_id}")
def get_status(task_id):
    value = redis_client.get(task_id)
    if value is not None:
        print("Value retrieved from Redis:", value.decode('utf-8'))  # Decode bytes to string if needed
        try:
            task_data = json.loads(value)
        except Exception as e:
            print('json.loads(value) failed with: ', e)
            task_data = value.decode('utf-8')
    else:
        print("Key not found in Redis.")
        task_data = value
    task_result = AsyncResult(str(task_id))
    result = {
        "task_id": str(task_id),
        "task_status": str(task_result.status),
        "task_result": str(task_result.result),
        "task_data": task_data,
    }
    return JSONResponse(result)

@router.get("/kill_tasks/{task_id}")
def kill_task(task_id):
    print(AsyncResult(str(task_id)))
    print(AsyncResult(str(task_id)).status)
    print(AsyncResult(str(task_id)).result)
    AsyncResult(str(task_id)).revoke(terminate=True)
    print(AsyncResult(str(task_id)))
    print(AsyncResult(str(task_id)).status)
    print(AsyncResult(str(task_id)).result)
    # AsyncResult(task_id).revoke(terminate=True)
    return JSONResponse({f'{task_id}': 'killed'})
    


@router.post("/process", status_code=201)
def run_task(payload = Body(...)):
    task = process_data.delay(payload)
    return JSONResponse({"task_id": task.id})