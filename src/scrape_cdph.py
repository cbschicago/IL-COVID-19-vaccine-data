import pandas as pd

# citywide by day

df = pd.read_csv("https://data.cityofchicago.org/resource/2vhs-cf6b.csv")
df["date"] = pd.to_datetime(df.date)

df = df.sort_values("date", ascending=True)
df["total_doses_7day_avg"] = df.total_doses_daily.rolling(7, min_periods=1).mean()
df[["date", "total_doses_daily", "total_doses_7day_avg"]].to_csv(
    "output/chicago_covid_vaccine_data_total_doses_daily.csv", index=False
)

# by zip code, current
df = pd.read_csv("https://data.cityofchicago.org/resource/553k-3xzc.csv?$limit=10000")
df["date"] = pd.to_datetime(df.date)
df = df[df.date == df.date.max()].fillna(
    "NULL"
)  # datawrapper breaks if there is a null value for some reason
df["vaccine_series_completed_percent_population"] = (
    df.vaccine_series_completed_percent_population * 100
)  # dw won't let me change it
df.to_csv(
    "output/chicago_covid_vaccine_data_total_doses_zip_code_current.csv", index=False
)
