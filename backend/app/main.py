from typing import Union

from fastapi import FastAPI
from .models import models

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/rant")
def read_rant():
    return models.generate_mock_rant()

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}