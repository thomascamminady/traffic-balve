import altair as alt

from traffic_balve.create_df import create_df

df = create_df()

base = (
    alt.Chart(
        df  # type:ignore
    )
    .mark_line(strokeWidth=3)
    .encode(
        x=alt.X("datetime:T").title("Uhrzeit"),
        color=alt.Color("from_to:N")
        .title("Richtung")
        .scale(
            domain=[
                "Höhle -> Krankenhaus",
                "Krankenhaus -> Höhle",
                "Krumpaul -> Höhle",
                "Höhle -> Krumpaul",
                "Krankenhaus -> Krumpaul",
                "Krumpaul -> Krankenhaus",
            ],
            range=[
                "#1F77B4",
                "#AEC7E8",
                "#FF7F0E",
                "#FFBB78",
                "#2CA02C",
                "#98DF8A",
            ],
        ),
    )
    .properties(width=1500, height=550)
)


alt.layer(
    base.encode(
        y=alt.Y("duration_in_traffic_s:Q").title("Reisezeit [Sekunden]"),
    ),
    base.mark_line(strokeWidth=2, strokeDash=[2, 2]).encode(
        y=alt.Y("duration_s:Q").title("Reisezeit [Sekunden]"),
    ),
).save("output/image.png", scale_factor=4)
