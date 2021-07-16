import pandas as pd

df = pd.read_csv(
    "https://hub.mph.in.gov/dataset/c484a6a3-2f32-4af9-8e02-c98801c3454f/resource/"
    "a4d23ae8-34c2-4951-85e0-3ea9345ee6ea/download/county-vaccinations-by-date.csv"
)
df["date"] = pd.to_datetime(df.date)
df = df[df.date >= "2021-01-01"].sort_values("date")

# export by county
df.to_csv("output/indiana_dph_vaccinations_daily_by_county.csv", index=False)

# export statewide
statewide = df.groupby("date")[
    [
        "first_dose_administered",
        "second_dose_administered",
        "single_dose_administered",
        "all_doses_administered",
        "fully_vaccinated",
        "new_first_dose_administered",
        "new_second_dose_administered",
        "new_single_dose_administered",
        "new_all_doses_administered",
        "new_fully_vaccinated",
    ]
].sum()
statewide.to_csv("output/indiana_dph_vaccinations_daily_statewide.csv", index=False)
