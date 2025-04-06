import uuid
from datetime import datetime
from typing import List, Optional, Self
from dataclasses import asdict

from pydantic import BaseModel, Field

from typing import Optional
import uuid
from datetime import datetime
import gel
from shapely import Point, Polygon, box, from_wkb


class BoundingBoxModel(BaseModel):
    xmin: float
    ymin: float
    xmax: float
    ymax: float

    def to_list(self):
        # Note this ordering is what is expected by postgis (follows geojson bbox spec)
        return [self.xmin, self.ymin, self.xmax, self.ymax]

    def to_box(self):
        return box(*self.to_list())


class ModerationMixin(BaseModel):
    flagged_offensive: bool = False


class PointMixin(BaseModel):
    lat: float
    lon: float

    def get_geometry(self) -> Point:
        # Note the [Lon, lat] ordering here is expected by postgis
        return Point(self.lon, self.lat)


class TimestampMixin(BaseModel):
    created_at: datetime
    updated_at: Optional[datetime] = None


class VisibilityMixin(BaseModel):
    visible: bool = True
    icon: Optional[str] = None


class VotableMixin(BaseModel):
    num_likes: int = 1  # Assuming the poster likes the rant
    num_dislike: int = 0


class RantModel(
    ModerationMixin,
    PointMixin,
    TimestampMixin,
    VotableMixin,
    VisibilityMixin,
):
    id: Optional[uuid.UUID] = None
    replies: Optional[List["ReplyModel"]] = Field(default=None, exclude=True)
    title: str
    body: str
    category: Optional[str] = None
    visible: bool = False
    flagged_offensive: bool = False


    @staticmethod
    def _from_gel_obj(obj) -> Self:

        point = from_wkb(obj.geometry)[0]
        rant = RantModel(
            lon=point.x,
            lat=point.y,
            # replies=[ReplyModel(parent_rant_id=obj.id, **asdict(reply)) for reply in obj.replies],
            **asdict(
                obj,
                dict_factory=lambda x: {
                    k: v for (k, v) in x if k not in ["replies", "geometry"]
                },
            )
        )

        return rant

    def insert_rant(
        self,
        executor: gel.Executor,
    ):

        return executor.query_single(
            """\
            INSERT Rant {
                title := <str>$title,
                body := <str>$body,
                geometry := <ext::postgis::geometry>$geometry,
                category := <str>$category,
                created_at := <datetime>$created_at,
                visible := <bool>$visible,
                flagged_offensive := <bool>$flagged_offensive,
                icon := <str>$icon
            }\
            """,
            title=self.title,
            body=self.body,
            geometry=self.get_geometry(),
            category=self.category,
            created_at=self.created_at,
            visible=self.visible,
            icon=self.icon,
            flagged_offensive=self.flagged_offensive,
        )

    @classmethod
    def select_rant_by_id(
        cls,
        executor: gel.Executor,
        id: uuid.UUID,
    ) -> Self:

        obj = executor.query_single(
            """
            select Rant {*}
            filter .id = <uuid>$id
            """,
            id=id,
        )

        return cls._from_gel_obj(obj)

    @classmethod
    def select_rants_by_bbox(
        cls,
        executor: gel.Executor,
        bbox: BoundingBoxModel,
    ) -> list[Self]:
        objs = executor.query(
            """
            select Rant {*} 
            filter {
                ext::postgis::op_contains_2d(
                    <ext::postgis::box2d>$bbox,
                    .geometry
                )
            }
            """,
            bbox=bbox.to_box(),
        )
        return [cls._from_gel_obj(rant) for rant in objs]



class ReplyModel(
    ModerationMixin,
    TimestampMixin,
    VisibilityMixin,
    VotableMixin,
):
    id: Optional[uuid.UUID] = None
    parent_rant_id: uuid.UUID
    parent_reply_id: Optional[uuid.UUID] = None
    body: str

    @staticmethod
    def _from_gel_obj(obj) -> Self:
        parent_rant_id = obj.parent_rant.id
        parent_reply_id = obj.parent_reply.id if obj.parent_reply is not None else None
        return ReplyModel(parent_reply_id=parent_reply_id, parent_rant_id=parent_rant_id, **asdict(obj))

    def insert_reply(
        self,
        executor: gel.Executor,
    ):
        query_properties = [
            "parent_rant := (select Rant filter.id = < uuid > $parent_rant_id)",
            "body := <str>$body",
            "created_at := <datetime>$created_at",
            "visible := <bool>$visible",
            "flagged_offensive := <bool>$flagged_offensive",
            "icon := <str>$icon",
        ]

        kwargs = {
            "parent_rant_id": self.parent_rant_id,
            "body": self.body,
            "created_at": self.created_at,
            "icon": self.icon,
            "flagged_offensive": self.flagged_offensive,
            "visible": self.visible,
        }

        # Not every reply has a parent reply (though all replies have a parent rant
        if self.parent_reply_id is not None:
            query_properties.append(
                "(select detached Reply filter .id = <uuid>$parent_reply_id)"
            )
            kwargs["parent_reply_id"] = self.parent_reply_id

        query = f"""
            INSERT Reply {', '.join(query_properties)}
        """

        return executor.query_single(query, **kwargs)

    @classmethod
    def select_replies_by_rant_id(
        cls,
        executor: gel.Executor,
        id: uuid.UUID,
    ) -> list[Self]:

        obj = executor.query(
            """
            select Reply {**} 
            filter .parent_rant.id = <uuid>$parent_rant_id
            """,
            parent_rant_id=id,
        )
        return [cls._from_gel_obj(reply) for reply in obj]


# def generate_mock_rant():
#     now = TimeModel(
#         created_at=datetime.now(),
#         updated_at=datetime.now(),
#     )
#
#     empty_vote = VotableModel(nLike=0, nDislike=0)
#
#     reply0 = generate_mock_reply("I know mine too!")
#     reply1 = generate_mock_reply("You should watch the road when you drive.")
#
#     halifax = PointMixin(lat=44, lon=-63)
#
#     rant = RantModel(
#         id=uuid.uuid4(),
#         title="Potholes",
#         body="This pothole destroyed my car",
#         categ="😭",
#         replies=[reply0, reply1],
#         location=halifax,
#         votes=empty_vote,
#         time=now,
#     )
#
#     return rant
#
#
# def generate_mock_reply(msg="Hello world!"):
#     now = TimeModel(
#         created_at=datetime.now(),
#         updated_at=datetime.now(),
#     )
#
#     empty_vote = VotableModel(nLike=0, nDislike=0)
#
#     reply = ReplyModel(
#         id=uuid.uuid4(), rantId=uuid.uuid4(), msg=msg, votes=empty_vote, time=now
#     )
#
#     return reply
#
#
# if __name__ == "__main__":
#     rant = generate_mock_rant()
#     print(rant.model_dump_json(indent=2))
