from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .models import models
from .db import insert_rant
#from .llm import

from datetime import datetime, timezone
import uuid
from shapely import Point
import gel

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
def read_item(rant_id: uuid.UUID, q: Union[str, None] = None):
    rant = models.generate_mock_rant()
    return rant

@app.post("/replies/")
def create_item(item: models.ReplyModel):
    return item

@app.get("/replies/{reply_id}")
def read_item(reply_id: uuid.UUID, q: Union[str, None] = None):
    reply = models.generate_mock_reply()
    return reply

@app.post("/replies/{reply_id}/like")
def like_item(reply_id: uuid.UUID):
    reply = models.generate_mock_reply()
    reply.votes.nLike += 1
    return reply

@app.post("/replies/{reply_id}/dislike")
def dislike_item(reply_id: uuid.UUID):
    reply = models.generate_mock_reply()
    reply.votes.nDislike += 1
    return reply