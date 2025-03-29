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
    reply: List[ReplyModel]
    title: str
    body: str
    categ: str
