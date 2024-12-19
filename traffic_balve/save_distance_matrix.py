import json
from datetime import datetime

import googlemaps
import polars as pl
import pytz

from traffic_balve.create_df import create_df

# from traffic_balve.create_image2 import create_image
from traffic_balve.utils.config import Config


def get_distance_matrix(
    api_key: str,
    origin: tuple[float, float],
    destinations: list[tuple[float, float]],
    departure_time,
) -> dict:
    # Create a client instance
    gmaps = googlemaps.Client(key=api_key)

    # Retrieve the distance matrix
    distance_matrix = gmaps.distance_matrix(  # type: ignore
        [origin],  # Single origin
        destinations,  # Multiple destinations
        mode="driving",
        departure_time=departure_time,
    )

    return distance_matrix


if __name__ == "__main__":
    # Replace with your API key
    with open(file=f"{Config().foldername_root}/.apikey") as file:
        api_key = file.read().replace("\n", "")

    hoehle = (51.341209, 7.872643)
    krankenhaus = (51.326923, 7.867607)
    schule = (51.327617, 7.852697)

    locations = [hoehle, krankenhaus, schule]
    names = ["hoehle", "krankenhaus", "schule"]

    for i, origin in enumerate(locations):
        destinations = [loc for j, loc in enumerate(locations) if j != i]
        berlin_timezone = pytz.timezone("Europe/Berlin")
        departure_time = datetime.now(berlin_timezone)

        matrix = get_distance_matrix(
            api_key=api_key,
            origin=origin,
            destinations=destinations,
            departure_time=departure_time,
        )
        with open(
            f"{Config().foldername_root}/data/json/{departure_time}_from_{names[i]}.json",
            "w",
        ) as file:
            json.dump(matrix, file)

    df = create_df().sort("datetime", descending=False)
    df.write_csv("data/summary.csv")
    df.to_pandas().to_csv("data/summary.csv.zip")

    df.with_columns(
        ideal_duration_s=pl.col("distance_m") / 1000 / 50 * 3600
    ).with_columns(
        pl.col("datetime").cast(pl.Datetime(time_unit="ms")),
        pl.col("from", "to").cast(pl.Categorical),
        pl.col("duration_in_traffic_s").cast(pl.UInt16),
        pl.col("ideal_duration_s").cast(pl.Float32),
    ).drop("from_to", "distance_m", "duration_s").select(
        "datetime", "from", "to", "duration_in_traffic_s", "ideal_duration_s"
    ).write_parquet("data/summary.parquet")
