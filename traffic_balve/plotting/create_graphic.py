import altair as alt
import polars as pl

from traffic_balve.create_df import create_df
from traffic_balve.utils.config import Config


def create_graphic() -> None:
    alt.data_transformers.disable_max_rows()

    df = (
        create_df()
        .sort("datetime")
        .with_columns(
            delay_due_to_traffic_min=(
                pl.col("duration_in_traffic_s") - pl.col("duration_s")
            )
            / 60,
            delay_due_to_traffic_percent=100
            * (pl.col("duration_in_traffic_s") - pl.col("duration_s"))
            / pl.col("duration_s"),
        )
        .sort("datetime")
        .rolling(
            index_column="datetime",
            period="1m",
            by=["from_to"],
        )
        .agg(
            pl.col(
                "delay_due_to_traffic_percent",
                "delay_due_to_traffic_min",
                "duration_in_traffic_s",
                "duration_s",
                "distance_m",
            ).mean()
        )
    )
    base = (
        alt.Chart(
            df.with_columns(
                fake_datetime=pl.datetime(
                    year=2000,
                    month=1,
                    day=1,
                    hour=pl.col("datetime").dt.hour(),
                    minute=pl.col("datetime").dt.minute(),
                    second=pl.col("datetime").dt.second(),
                )
            )
            .with_columns(
                delta=(
                    (
                        pl.col("duration_in_traffic_s")
                        - pl.col("duration_in_traffic_s").quantile(0.05)
                    )
                    / 60
                    # / pl.col("duration_in_traffic_s").min()
                    # * 100
                ).over("from_to")
            )
            .with_columns(day_of_week=pl.col("datetime").dt.to_string("%A"))
            .with_columns(
                weekend=pl.col("day_of_week").is_in(["Saturday", "Sunday"])
            )
            .with_columns(
                kph=(pl.col("distance_m") / 1000)
                / (pl.col("duration_in_traffic_s") / 3600)
            )
            # .with_columns(z=pl.col("delta"))
            # .with_columns(z=pl.col("duration_in_traffic_s"))
            .with_columns(z=pl.col("kph"))
            .sort("fake_datetime")
            .group_by_dynamic(
                index_column="fake_datetime",
                every="5m",
                period="20m",
                by=["from_to", "weekend"],
            )
            .agg(
                min=pl.col("z").min(),
                qlow=pl.col("z").quantile(0.1),
                mean=pl.col("z").mean(),
                median=pl.col("z").median(),
                std=pl.col("z").std(),
                count=pl.col("z").count(),
                qhigh=pl.col("z").quantile(0.9),
                max=pl.col("z").max(),
            )
            .with_columns(pl.col("fake_datetime") + pl.duration(minutes=10))
            .with_columns(
                cat=pl.col("from_to").replace(
                    {
                        "Höhle -> Krankenhaus": "A",
                        "Krankenhaus -> Höhle": "A",
                        "Höhle -> Krumpaul": "B",
                        "Krumpaul -> Höhle": "B",
                        "Krumpaul -> Krankenhaus": "C",
                        "Krankenhaus -> Krumpaul": "C",
                    }
                )
            )
            .filter(pl.col("fake_datetime").dt.hour() < 21)
            # .filter(pl.col("weekend").not_())
            .to_pandas()
        )
        .encode(
            x=alt.X("hoursminutes(fake_datetime):T"),
            # color="from_to:N",
            color="from_to:N",
        )
        .properties(width=800, height=200)
    )

    chart = (
        alt.layer(
            # base.mark_area(clip=True, opacity=0.2).encode(
            #     y=alt.Y("min:Q").scale(domainMax=50, domainMin=20), y2="max:Q"
            # ),
            base.mark_area(clip=True, opacity=0.2).encode(
                y=alt.Y("qlow:Q").scale(domainMax=50, domainMin=0),
                y2="qhigh:Q",
            ),
            base.mark_line(clip=True).encode(
                y=alt.Y("mean:Q").scale(domainMax=50, domainMin=0)
            ),
        )
        .facet(
            row=alt.Row(
                "cat"
                # "day_of_week:N",
                # sort=[
                #     "Monday",
                #     "Tuesday",
                #     "Wednesday",
                #     "Thursday",
                #     "Friday",
                #     "",
                #     "Saturday",
                #     "Sunday",
                # ],
            ),
            column=alt.Column("weekend"),
            # columns=2,
        )
        .resolve_scale(color="independent")  # type: ignore
    )
    chart.save(f"""{Config().foldername_root}/chart.png""", scale_factor=3)


if __name__ == "__main__":
    create_graphic()
