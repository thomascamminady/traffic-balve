def format_distance_matrix(data) -> list:
    formatted_data = []
    for i, origin in enumerate(data["origin_addresses"]):
        for j, destination in enumerate(data["destination_addresses"]):
            element = data["rows"][i]["elements"][j]
            formatted_data.append(
                {
                    "from": origin,
                    "to": destination,
                    "distance": element["distance"]["value"],
                    "duration": element["duration"]["value"],
                    "duration_in_traffic": element.get(
                        "duration_in_traffic", {}
                    ).get("value", -99999),
                }
            )
    return formatted_data
