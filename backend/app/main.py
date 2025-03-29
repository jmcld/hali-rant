from typing import Union

from fastapi import FastAPI
from .models import models
from .db import insert_rant
#from .llm import

from datetime import datetime, timezone
import uuid
from shapely import Point
import gel

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
    # blocking client
    client = gel.create_client()

    point = Point(item.location.lon, item.location.lat)  # Lon/lat ordering

    now = datetime.now(timezone.utc)

    _ = insert_rant.insert_rant(
        client,
        title=item.title,
        body=item.body,
        geom=point,
        category=item.categ,
        created_at=now,
    )

    return item

@app.get("/rants/{rant_id}")
def read_item(rant_id: int, q: Union[str, None] = None):
    rant = models.generate_mock_rant()
    return rant

@app.post("/replies/")
def create_item(item: models.ReplyModel):
    return item

@app.get("/replies/{reply_id}")
def read_item(reply_id: int, q: Union[str, None] = None):
    reply = models.generate_mock_reply()
    return reply