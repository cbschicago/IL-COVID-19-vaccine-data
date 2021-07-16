import pandas as pd
from common import get_with_retry

resp = get_with_retry(
    "https://idph.illinois.gov/DPHPublicInformation/api/COVIDVaccine/getVaccineFullyVaccinatedAge"
)
df = pd.DataFrame(resp.json())
df.columns = df.columns.str.lower()
df["report_date"] = pd.to_datetime(df.report_date)
# filter from january on
df = df[df.report_date >= "2021-01-01"].sort_values("report_date", ascending=True)

# export age group-level data
df.to_csv("output/idph_fully_vaccinated_age_group_cumulative_daily.csv", index=False)

# export total by day
total = (
    df.groupby("report_date")
    .personsfullyvaccinated.sum()
    .to_frame("persons_fully_vaccinated")
)
total.to_csv("output/idph_fully_vaccinated_total_cumulative_daily.csv")
