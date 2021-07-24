from fastapi import FastAPI, Body, Header, File
from routes.v1 import app_v1
from routes.v2 import app_v2
from starlette.requests import Request

app = FastAPI()

app.mount("/v1", app_v1)
app.mount("/v2", app_v2)


@app.middleware("http")
async def middleware(request: Request, call_next):
    # modify request
    response = await call_next(request)
    # modify response
    return response
