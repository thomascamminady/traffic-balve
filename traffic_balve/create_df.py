import glob
import json

import polars as pl

from traffic_balve.parse import format_distance_matrix
from traffic_balve.utils.config import Config


def create_df() -> pl.DataFrame:
    files = glob.glob(f"{Config().foldername_root}/data/json/*.json")
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
                        "51.3269218,7.8675944": "Krankenhaus",
                        "51.3276141,7.8527007": "Krumpaul",
                        "Helle 11, 58802 Balve-Helle, Germany": "Höhle",
                    }
                )
            )
            .with_columns(from_to=pl.col("from") + pl.lit(" → ") + pl.col("to"))
            .with_columns(
                route=pl.when(pl.col("from") < pl.col("to"))
                .then(pl.col("from") + pl.lit(" ↔ ") + pl.col("to"))
                .otherwise(pl.col("to") + pl.lit(" ↔ ") + pl.col("from"))
            )
        )
    df = pl.concat(df_list)
    return df
