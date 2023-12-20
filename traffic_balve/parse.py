import json


# Function to parse and reformat the data
def format_distance_matrix(data):
    formatted_data = []
    for i, origin in enumerate(data["origin_addresses"]):
        for j, destination in enumerate(data["destination_addresses"]):
            element = data["rows"][i]["elements"][j]
            formatted_data.append(
                {
                    "from": origin,
                    "to": destination,
                    "distance": element["distance"]["text"],
                    "duration": element["duration"]["text"],
                    "duration_in_traffic": element.get("duration_in_traffic", {}).get(
                        "text", "N/A"
                    ),
                }
            )
    return formatted_data


with open(
    "/Users/thomascamminady/Repos/traffic_balve/data/2023-12-20 10:50:43.063641.json",
) as f:
    distance_matrix_data = json.load(f)
# Format the data
formatted_matrix = format_distance_matrix(distance_matrix_data)

# Print formatted data
for entry in formatted_matrix:
    print(entry)
