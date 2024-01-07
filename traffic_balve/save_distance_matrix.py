import json
from datetime import datetime

import googlemaps
import pytz


def get_distance_matrix(
    api_key: str,
    origin: tuple[float, float],
    destinations: list[tuple[float, float]],
    departure_time,
) -> dict:
    # Create a client instance
    gmaps = googlemaps.Client(key=api_key)

    # Retrieve the distance matrix
    print(departure_time)
    distance_matrix = gmaps.distance_matrix(
        [origin],  # Single origin
        destinations,  # Multiple destinations
        mode="driving",
        departure_time=departure_time,
    )

    return distance_matrix


if __name__ == "__main__":
    # Replace with your API key
    with open(
        file="/Users/thomascamminady/Repos/traffic_balve/.apikey"
    ) as file:
        api_key = file.read().replace("\n", "")

    hoehle = (51.341209, 7.872643)
    krankenhaus = (51.326923, 7.867607)
    schule = (51.327617, 7.852697)

    locations = [hoehle, krankenhaus, schule]
    names = ["hoehle", "krankenhaus", "schule"]

    berlin_timezone = pytz.timezone("Europe/Berlin")
    departure_time = datetime.now(berlin_timezone)

    for i, origin in enumerate(locations):
        destinations = [loc for j, loc in enumerate(locations) if j != i]
        matrix = get_distance_matrix(
            api_key=api_key,
            origin=origin,
            destinations=destinations,
            departure_time=departure_time,
        )
        with open(
            f"/Users/thomascamminady/Repos/traffic_balve/data/{departure_time}_from_{names[i]}.json",
            "w",
        ) as file:
            json.dump(matrix, file)
