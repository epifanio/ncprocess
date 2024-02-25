from fastapi import APIRouter
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from models.datamodel import SearchObject

router = APIRouter()
templates = Jinja2Templates(directory="/usr/src/app/templates")

@router.get("/results/{id}")



@router.get("/search", response_class=HTMLResponse)
async def read_root(request: Request):
    # Read the HTML file and return it as a response
#    with open("index.html", "r") as file:
#        html_content = file.read()
    # context = {"key": "value"}
    # return templates.TemplateResponse("search.html", {"request": request, **context})
    context = {"request": request}
    return templates.TemplateResponse("search.html", context)


@router.post("/submit-form")
def submit_form(data: SearchObject):
    # Here you can access the submitted form data as attributes of the data object
    # For example: data.text_entry, data.start_time, etc.
    # You can perform any necessary processing or validation here
    # For demonstration purposes, let's just print the received data
    
    print("Received form data:")
    print("Text Entry:", data.text_entry)
    print("Start Time:", data.start_time)
    print("End Time:", data.end_time)
    print("Keywords List:", data.keywords_list)
    print("Bounding Box:", data.bbox)
    # Optionally, you can return a response
    return {"message": "Form data received successfully"}