
import uuid
from datetime import datetime
import gel
from shapely import Point, Polygon, box


def select_rants_by_bbox(
    executor: gel.Executor,
    bbox: list[float, float, float, float],
):

    return executor.query(
        """
        select Rant {**} 
        filter {
            ext::postgis::op_contains_2d(
                <ext::postgis::box2d>$bbox,
                .geom
            )
        }
        """,
        bbox=box(*bbox),
    )


def select_rant_by_id(
    executor: gel.Executor,
    id: uuid.UUID,
):
    return executor.query_single(
        """
        select Rant {**} 
        filter .id = <uuid>$id
        """,
        id=id,
    )

def select_replies_by_rand_it(
    executor: gel.Executor,
    id: uuid.UUID,
    ):
    return executor.query(
        """
        select Rant {**} 
        filter .id = <uuid>$id
        """,
        id=id,
    )

def insert_rant(
    executor: gel.Executor,
    *,
    title: str,
    body: str,
    geom: Point,
    category: str,
    created_at: datetime,
):
    return executor.query_single(
        """\
        INSERT Rant {
            title := <str>$title,
            body := <str>$body,
            geom := <ext::postgis::geometry>$geom,
            category := <str>$category,
            created_at := <datetime>$created_at,
        }\
        """,
        title=title,
        body=body,
        geom=geom,
        category=category,
        created_at=created_at,
    )
