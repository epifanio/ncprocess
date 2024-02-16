import sys
sys.path.append('/usr/src/app')
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from api import celery_task
from api import auth
from api import sse
import logging

logging.getLogger('passlib').setLevel(logging.ERROR)

app = FastAPI(
    title="ncapi",
    description="Prototype API to process NetCDF Data",
    version="0.0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_PROCESSING_SECOND = 600

def configure():
    """ run the routing configuration for the mail fastapi App"""
    configure_routing()
    
def configure_routing():    
    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.include_router(celery_task.router)
    app.include_router(sse.router)
    app.include_router(auth.router)

if __name__ == "__main__":
    configure()
    uvicorn.run(app, port=8000, host="0.0.0.0", reload=True, debug=True)
else:
    configure()
