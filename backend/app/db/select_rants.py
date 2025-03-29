
import gel
from shapely import  Polygon


def select_rants_by_aoi(
    executor: gel.Executor,
    aoi: Polygon,
):
    return executor.query(
        """
        select Rant {*} 
        filter {
            ext::postgis::op_contains_2d(
                <ext::postgis::box2d>$aoi,
                .geom
            )
        }
        """,
        aoi=aoi,
    )


# Example for inserting a rant into the database
def example_select():

    # blocking client
    client = gel.create_client()
    aoi = Polygon.from_bounds(-63.736582, 44.596349, -63.446131, 44.710648)

    response = select_rants_by_aoi(client, aoi)
    return response


if __name__ == "__main__":
    print(example_select())

