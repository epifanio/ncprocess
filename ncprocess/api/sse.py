# import sys
# # setting path
# sys.path.append('/usr/src/app')

from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="/usr/src/app/templates")

router = APIRouter()

@router.get("/task/status/render/{task_id}", response_class=HTMLResponse)
async def render_task_status(request: Request, task_id: str):
    # task_status = get_task_status(task_id)
    # , "task_status": 'task_status'
    return templates.TemplateResponse("stream.html", {"request": request, "task_id": task_id, "task_status": 'task_status'})
