import pandas as pd

df = pd.read_csv("https://data.cityofchicago.org/resource/2vhs-cf6b.csv")
df["date"] = pd.to_datetime(df.date)

df = df.sort_values("date", ascending=True)
df["total_doses_7day_avg"] = df.total_doses_daily.rolling(7, min_periods=1).mean()
df[["date", "total_doses_daily", "total_doses_7day_avg"]].to_csv(
    "output/chicago_covid_vaccine_data_total_doses_daily.csv", index=False
)
