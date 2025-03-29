
import dataclasses
from datetime import datetime, timezone
import gel
import uuid
from shapely import Point


@dataclasses.dataclass
class InsertRantResult:
    id: uuid.UUID


def insert_rant(
    executor: gel.Executor,
    *,
    title: str,
    body: str,
    geom: Point,
    category: str,
    created_at: datetime,
) -> InsertRantResult:
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


def example_insert():

    # blocking client
    client = gel.create_client()

    point = Point(-63.596570, 44.664466)  # Lon/lat ordering

    response = insert_rant(
        client,
        title="test rant title",
        body="this is a test body to a rant",
        geom=point,
        category="test category",
        created_at=datetime.now(timezone.utc),
    )

    return response



if __name__ == "__main__":
    print(example_insert())