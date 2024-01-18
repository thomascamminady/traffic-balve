import json
from datetime import datetime

import altair as alt
import polars as pl

from traffic_balve.utils.config import Config


def create_image() -> None:
    alt.data_transformers.disable_max_rows()

    def theme():
        with open(
            f"{Config().foldername_root}/traffic_balve/camminady_theme.json",
        ) as f:
            return json.load(f)

    alt.themes.register("_my_theme", theme)
    alt.themes.enable("_my_theme")

    df = pl.read_csv(
        "https://raw.githubusercontent.com/thomascamminady/traffic-balve/main/data/summary.csv"
    )

    (
        alt.Chart(
            df.with_columns(pl.col("datetime").cast(pl.Datetime))  # type: ignore
            .with_columns(
                duration_at_50kph_s=pl.col("distance_m") / 1000 / 50 * 3600
            )
            .with_columns(
                delay_m=(
                    pl.col("duration_in_traffic_s")
                    - pl.col("duration_at_50kph_s")
                )
                / 60
            )
            .with_columns(pl.col("from_to").str.replace("->", "→"))
            .sort("datetime", descending=False)
            .rolling(
                pl.col("datetime"),
                period=f"{(period:=15)}m",
                offset=f"-{period//2}m",
                by=["from", "to"],
            )
            .agg(pl.col("delay_m").mean(), from_to=pl.col("from_to").first())
            .with_columns(
                today=pl.col("datetime").dt.date() == datetime.now().date(),
            )
            .select("today", "datetime", "delay_m", "to", "from")
        )
        .mark_line(point=False, clip=True)
        .encode(
            x=alt.X("hoursminutes(datetime):T").title("Uhrzeit"),
            y=alt.Y("delay_m:Q")
            .scale(zero=False, domainMin=0)
            .title("Verspätung [min]"),
            detail="date(datetime):T",
            color=alt.Color("to:N").title("Nach", labelLimit=0),
            opacity=alt.condition(  # type: ignore
                alt.datum.today,
                alt.value(1.0),
                alt.value(0.1),
            ),
            strokeWidth=alt.condition(  # type: ignore
                alt.datum.today,
                alt.value(4),
                alt.value(2),
            ),
            tooltip=["from:N", "to:N", "datetime:T", "delay_m:Q"],
            row=alt.Row("from:N", spacing=50).title(None),
        )
        .configure_header(  # type: ignore
            labelColor="gray",
            labelFontSize=15,
            labelAngle=0,
            labelAlign="left",
            titleColor="gray",
            titleFontSize=20,
        )
        .properties(width=1000, height=300)
    ).save("output/overview.png", scale_factor=4)
