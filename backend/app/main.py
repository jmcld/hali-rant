from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .models import models
from .db.query import (
    insert_rant,
    select_rants_by_aoi,
    select_rant_by_id
)

#from .llm import

from datetime import datetime, timezone
import uuid
from shapely import Point, from_wkb
import gel

app = FastAPI()

# TODO figure out client pooling
# TODO Async client
client = gel.create_client()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
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

    response = insert_rant(
        client,
        title=item.title,
        body=item.body,
        geom=Point(item.location.lon, item.location.lat),  # Lon/lat ordering,
        category=item.categ,
        created_at=datetime.now(timezone.utc),
    )

    return {"id": response.id}

@app.get("/rants/{rant_id}")
def read_item(rant_id: uuid.UUID):

    db_obj = select_rant_by_id(client, rant_id)
    now = models.TimeModel(
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    votes = models.VotableModel(
        nLike=db_obj.num_downvote,
        nDislike=db_obj.num_upvote,
    )

    points = from_wkb(db_obj.geom)
    location = models.LocationModel(lon=points[0].x, lat=points[0].y)
    response = models.RantModel(
        id=db_obj.id,
        title=db_obj.title,
        body=db_obj.body,
        categ=db_obj.category,
        location=location,
        votes=votes,
        time=now,
        replies=db_obj.replies,
    )
    return response

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