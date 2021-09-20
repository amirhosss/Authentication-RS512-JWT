from fastapi import FastAPI

from api.routers import main


app = FastAPI()

app.include_router(main.router)
