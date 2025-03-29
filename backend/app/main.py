from typing import Union

from fastapi import FastAPI
from .models import models

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/rants")
def read_rants():
    rants = [models.generate_mock_rant(), models.generate_mock_rant()]
    return rants

@app.post("/rants/")
def create_item(item: models.RantModel):
    return item

@app.get("/rants/{rant_id}")
def read_item(rant_id: int, q: Union[str, None] = None):
    rant = models.generate_mock_rant()
    return rant
