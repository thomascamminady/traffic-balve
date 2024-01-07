import glob
import json

import polars as pl

from traffic_balve.parse import format_distance_matrix


def create_df() -> pl.DataFrame:
    files = glob.glob(
        "/Users/thomascamminady/Repos/traffic_balve/data/json/*.json"
    )
    df_list = []
    for file in files:
        with open(file=file) as f:
            distance_matrix_data = json.load(f)
        formatted_matrix = format_distance_matrix(distance_matrix_data)

        df_list.append(
            pl.from_dicts(formatted_matrix)
            .with_columns(
                datetime=pl.lit(
                    file.split("+")[0].split("/")[-1].replace(".json", "")
                ).str.strptime(format="%Y-%m-%d %H:%M:%S%.f", dtype=pl.Datetime)
            )
            .filter(pl.col("from") != pl.col("to"))
            .rename(
                mapping={
                    "distance": "distance_m",
                    "duration": "duration_s",
                    "duration_in_traffic": "duration_in_traffic_s",
                }
            )
            .with_columns(
                pl.col("from", "to").replace(
                    {
                        "Am Krumpaul 2, 58802 Balve, Germany": "Krumpaul",
                        "Balve, Krankenhaus, 58802 Balve, Germany": "Krankenhaus",
                        "Helle 11, 58802 Balve, Germany": "Höhle",
                    }
                )
            )
            .with_columns(
                from_to=pl.col("from") + pl.lit(" -> ") + pl.col("to")
            )
        )
    df = pl.concat(df_list)
    return df
