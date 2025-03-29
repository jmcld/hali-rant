from typing import Union

from fastapi import FastAPI
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
        time=now
    )
    return response

@app.post("/replies/")
def create_item(item: models.ReplyModel):
    return item

@app.get("/replies/{reply_id}")
def read_item(reply_id: int, q: Union[str, None] = None):
    reply = models.generate_mock_reply()
    return reply