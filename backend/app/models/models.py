import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class TimeModel(BaseModel):
    created_at: datetime
    updated_at: datetime


class LocationModel(BaseModel):
    lat: float
    lon: float


class VotableModel(BaseModel):
    nLike: int
    nDislike: int


class ReplyModel(BaseModel):
    id: uuid.UUID
    rantId: uuid.UUID
    msg: str
    votes: VotableModel
    time: TimeModel


class RantModel(BaseModel):
    id: uuid.UUID
    replies: Optional[List[ReplyModel]] = None
    title: str
    body: str
    categ: str
    votes: VotableModel
    location: LocationModel
    time: TimeModel


def generate_mock_rant():
    now = TimeModel(
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    empty_vote = VotableModel(
        nLike=0,
        nDislike=0
    )

    reply0 = generate_mock_reply("I know mine too!")
    reply1 = generate_mock_reply("You should watch the road when you drive.")

    halifax = LocationModel(
        lat=44,
        lon=-63
    )

    rant = RantModel(
        id=uuid.uuid4(),
        title="Potholes",
        body="This pothole destroyed my car",
        categ="😭",
        replies=[reply0, reply1],
        location=halifax,
        votes=empty_vote,
        time=now
    )

    return rant

def generate_mock_reply(msg="Hello world!"):
    now = TimeModel(
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    empty_vote = VotableModel(
        nLike=0,
        nDislike=0
    )

    reply = ReplyModel(
        id=uuid.uuid4(),
        rantId=uuid.uuid4(),
        msg=msg,
        votes=empty_vote,
        time=now
    )

    return reply

if __name__ == "__main__":
    rant = generate_mock_rant()
    print(rant.model_dump_json(indent=2))
