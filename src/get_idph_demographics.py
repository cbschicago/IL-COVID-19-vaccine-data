import json
import os
import requests
import pandas as pd

with open("input/il_counties.json", "r") as f:
    counties = json.load(f)

outfiles = {
    "Age": "output/idph_vaccine_administration_data_demo_age_daily.csv",
    "Race": "output/idph_vaccine_administration_data_demo_race_daily.csv",
    "Gender": "output/idph_vaccine_administration_data_demo_gender_daily.csv",
}

dfs = {
    "Age": [],
    "Race": [],
    "Gender": [],
}

for county in counties:
    url = f"https://idph.illinois.gov/DPHPublicInformation/api/covidVaccine/getVaccineAdministrationDemos?countyname={county}"
    resp = requests.get(url)
    assert (
        resp.status_code == 200
    ), f"request failed with status code {resp.status_code}"

    data = resp.json()
    for df_name in data.keys():
        df = pd.DataFrame(data[df_name])
        df.columns = (
            df.columns.str.replace(r"(?<!^)(?=[A-Z])", "_", regex=True)
            .str.lower()
            .str.replace("_+", "_")
        )

        dfs[df_name].append(df)

for df_name in dfs:
    df = pd.concat(dfs[df_name])
    outfile = outfiles[df_name]
    if os.path.exists(outfile):
        archive = pd.read_csv(outfile)
    else:
        archive = pd.DataFrame()
    df = df.append(archive)
    df.to_csv(outfile, index=False)