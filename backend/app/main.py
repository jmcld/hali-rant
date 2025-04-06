import uuid

import gel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .models.models import BoundingBoxModel, RantModel, ReplyModel

# from .llm.moderator import ContentModerator


app = FastAPI()
# moderator = ContentModerator()

# TODO figure out client pooling
# TODO Async client
client = gel.create_client()

origins = ["*"]

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


@app.get("/rants/")
def get_rants_by_bbox(
    xmin: float,
    ymin: float,
    xmax: float,
    ymax: float,
) -> list[RantModel]:
    bbox = BoundingBoxModel(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)
    rants = RantModel.select_rants_by_bbox(client, bbox)

    return rants


@app.post("/rants/")
def insert_rant(rant: RantModel):
    # TODO: optimize OpenAI call here so we arent holding threads
    # item = moderator.moderate_rant(item)
    response = rant.insert_rant(client)
    return {"id": response.id}


@app.get("/rants/{rant_id}")
def select_rant_by_id(rant_id: uuid.UUID):
    return RantModel.select_rant_by_id(client, rant_id)


@app.post("/replies/")
def create_reply(reply: ReplyModel):
    # TODO: optimize OpenAI call here so we arent holding threads
    # reply = moderator.moderate_rant(reply)
    response = reply.insert_reply(client)
    return {"id": response.id}


@app.get("/replies/{rant_id}")
def get_replies_by_rant_id(rant_id: uuid.UUID):
    return ReplyModel.select_replies_by_rant_id(client, rant_id)


#
# @app.post("/replies/{rant_id}/like")
# def like_item(reply_id: uuid.UUID):
#     reply = generate_mock_reply()
#     reply.votes.num_likes += 1
#     return reply
#
#
# @app.post("/replies/{reply_id}/dislike")
# def dislike_item(reply_id: uuid.UUID):
#     reply = generate_mock_reply()
#     reply.votes.num_dislike += 1
#     return reply
