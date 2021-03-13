import json
import os
import requests
import pandas as pd


def sort_pin_statewide(df, by, ascending=False):
    return df[df.county_name == "Illinois"].append(
        df[df.county_name != "Illinois"].sort_values(by, ascending=ascending)
    )


with open("input/il_counties.json", "r") as f:
    counties = json.load(f)

dfs = []
for county in counties:
    url = (
        "https://idph.illinois.gov/DPHPublicInformation/api/covidVaccine/"
        f"getVaccineAdministration?countyName={county}"
    )
    resp = requests.get(url)
    assert (
        resp.status_code == 200
    ), f"request failed with status code {resp.status_code}"
    data = resp.json()
    df = pd.DataFrame(data["VaccineAdministration"])
    df.columns = (
        df.columns.str.replace(r"(?<!^)(?=[A-Z])", "_", regex=True)
        .str.lower()
        .str.replace("_+", "_")
    )
    df["report_date"] = pd.to_datetime(df.report_date)
    df["administered_doses_per_100k"] = df.administered_count / df.population * 100_000
    # datawrapper needs percents, not decimals
    df["pct_vaccinated_population"] = df.pct_vaccinated_population * 100
    dfs.append(df)

df = pd.concat(dfs)
latest = df[df.report_date == df.report_date.max()].copy()

############### OUTPUT ###############

# DAILY BY COUNTY
df.drop_duplicates().to_csv(
    "output/idph_vaccine_administration_data_daily_by_county.csv", index=False
)

# DAILY STATEWIDE
statewide_df = df[df.county_name == "Illinois"]
statewide_df.to_csv(
    "output/idph_vaccine_administration_data_daily_statewide.csv", index=False
)

table_cols = [
    "census_county_name",
    "county_name",
    "administered_count",
    "administered_count_roll_avg",
    "persons_fully_vaccinated",
    "pct_vaccinated_population",
]

# CURRENT BY COUNTY
latest["census_county_name"] = latest.county_name.apply(lambda n: f"{n} County, IL")
latest = latest[
    ["census_county_name"] + [c for c in latest if c != "census_county_name"]
]
# ensure statewide number is top row for datawrapper
# then sort by vax rate to set the default datawrapper sort view
out = sort_pin_statewide(latest, "pct_vaccinated_population")[table_cols]
out.to_csv("output/idph_vaccine_administration_data_current_by_county.csv", index=False)

# CURRENT STATEWIDE
latest_statewide = latest[latest.county_name == "Illinois"][table_cols]

# sort by vax rate to set the default datawrapper sort view
latest_statewide.sort_values("pct_vaccinated_population", ascending=False).to_csv(
    "output/idph_vaccine_administration_data_current_statewide.csv", index=False
)

# INVENTORY POINTS FOR MAP
latest["total_inventory_per_100k"] = (
    latest.total_reported_inventory / latest.population * 100_000
)
out = latest[
    [
        "census_county_name",
        "county_name",
        "l_h_d_reported_inventory",
        "community_reported_inventory",
        "total_reported_inventory",
        "total_inventory_per_100k",
        "latitude",
        "longitude",
    ]
]
out = sort_pin_statewide(out, "total_inventory_per_100k")
out.to_csv(
    "output/idph_vaccine_administration_data_current_inventory_by_county.csv",
    index=False,
)
