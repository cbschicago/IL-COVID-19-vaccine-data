import pandas as pd

# CITYWIDE BY DAY

df = pd.read_csv("https://data.cityofchicago.org/resource/2vhs-cf6b.csv")
df["date"] = pd.to_datetime(df.date)

df = df.sort_values("date", ascending=True)
df["total_doses_7day_avg"] = df.total_doses_daily.rolling(7, min_periods=1).mean()
df[["date", "total_doses_daily", "total_doses_7day_avg"]].to_csv(
    "output/chicago_covid_vaccine_data_total_doses_daily.csv", index=False
)

# CURRENT BY ZIP CODE

df = pd.read_csv("https://data.cityofchicago.org/resource/553k-3xzc.csv?$limit=10000")
df["date"] = pd.to_datetime(df.date)

# get 7day avg for each zip code
dfs = []
for z in df.zip_code.unique():
    zdf = df[df.zip_code == z][["zip_code", "date", "total_doses_daily"]].sort_values(
        "date"
    )
    zdf["7_day_avg"] = zdf.total_doses_daily.rolling(7, min_periods=1).mean()
    dfs.append(zdf)

df = df.merge(
    pd.concat(dfs).drop_duplicates(), on=["zip_code", "date", "total_doses_daily"]
)


df = df[df.date == df.date.max()].fillna(
    "NULL"
)  # datawrapper breaks if there is a null value for some reason
df["vaccine_series_completed_percent_population"] = (
    # dw won't let me change it
    df.vaccine_series_completed_percent_population
    * 100
)
df = df[
    [
        "zip_code",
        "total_doses_cumulative",
        "7_day_avg",
        "vaccine_series_completed_cumulative",
        "vaccine_series_completed_percent_population",
    ]
]
df.to_csv(
    "output/chicago_covid_vaccine_data_total_doses_zip_code_current.csv", index=False
)
