import uuid
from datetime import datetime
from typing import List

from pydantic import BaseModel

class LocationModel(BaseModel):
    lat: float
    lon: float

class MessageModel(BaseModel):
    title: str
    descr: str
    nLike: int
    nDislike: int
    loc: LocationModel
    timestamp: datetime
    id: uuid.UUID
    parent: int
    category: str
    # Future considerations:
    # attachements: uuid.UUID

class ReplyModel(BaseModel):
    id: uuid.UUID
    rantId: uuid.UUID
    msg: str

class RantModel(BaseModel):
    id: uuid.UUID
    reply: List[ReplyModel]
    title: str
    body: str
    categ: str


if __name__ == "__main__":
    reply0 = ReplyModel(
        id = uuid.uuid4(),
        rantId = uuid.uuid4(),
        msg = "I know mine too!"
    )

    reply1 = ReplyModel(
        id=uuid.uuid4(),
        rantId=uuid.uuid4(),
        msg="You should watch the road when you drive."
    )

    rant = RantModel(
        id = uuid.uuid4(),
        title = "Potholes",
        body = "This pothole destroyed my car",
        categ = "😭",
        reply = [reply0, reply1]
    )

    print(rant.model_dump_json(indent=2))
