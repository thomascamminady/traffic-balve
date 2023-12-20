import json
from datetime import datetime

import googlemaps


def get_distance_matrix(
    api_key: str,
    origins: list[tuple[float, float]],
    destinations: list[tuple[float, float]],
    departure_time,
) -> dict:
    # Create a client instance
    gmaps = googlemaps.Client(key=api_key)

    # Retrieve the distance matrix
    distance_matrix = gmaps.distance_matrix(  # type: ignore
        origins,
        destinations,
        mode="driving",
        departure_time=departure_time,
    )

    return distance_matrix


if __name__ == "__main__":
    # Replace with your API key
    with open("/Users/thomascamminady/Repos/traffic_balve/.apikey") as file:
        api_key = file.read().replace("\n", "")

    hoehle = (51.341209, 7.872643)
    krankenhaus = (51.326923, 7.867607)
    schule = (51.327617, 7.852697)

    locations = [hoehle, krankenhaus, schule]
    departure_time = datetime.now()
    matrix = get_distance_matrix(
        api_key=api_key,
        origins=locations,
        destinations=locations,
        departure_time=departure_time,
    )
    with open(
        f"/Users/thomascamminady/Repos/traffic_balve/data/{departure_time}.json",
        "w",
    ) as file:
        json.dump(matrix, file, indent=4)
