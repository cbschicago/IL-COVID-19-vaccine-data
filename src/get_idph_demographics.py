import json
import os
import requests
import pandas as pd
from common import get_with_retry, idph_vaccine_request_headers

with open("input/il_counties.json", "r") as f:
    counties = json.load(f)

outfiles = {
    "Age": "output/idph_vaccine_administration_data_demo_age",
    "Race": "output/idph_vaccine_administration_data_demo_race",
    "Gender": "output/idph_vaccine_administration_data_demo_gender",
}

dfs = {
    "Age": [],
    "Race": [],
    "Gender": [],
}

county_vax_current = pd.read_csv(
    "output/idph_vaccine_administration_data_daily_by_county.csv"
).rename(
    columns={
        "administered_count": "administered_count_all",
        "persons_fully_vaccinated": "persons_fully_vaccinated_all",
    }
)
county_vax_current["report_date"] = pd.to_datetime(county_vax_current.report_date)

for county in counties:
    url = f"https://idph.illinois.gov/DPHPublicInformation/api/covidVaccine/getVaccineAdministrationDemos?countyname={county}"
    resp = get_with_retry(url, headers=idph_vaccine_request_headers)
    data = resp.json()
    for df_name in data.keys():
        df = pd.DataFrame(data[df_name])
        if len(df) == 0:
            continue

        df.columns = (
            df.columns.str.replace(r"(?<!^)(?=[A-Z])", "_", regex=True)
            .str.lower()
            .str.replace("_+", "_")
        )
        df["report_date"] = pd.to_datetime(df.report_date)

        df = df.merge(
            county_vax_current[
                [
                    "county_name",
                    "report_date",
                    "administered_count_all",
                    "persons_fully_vaccinated_all",
                ]
            ],
            how="left",
            on=["county_name", "report_date"],
        ).drop_duplicates()

        df["administered_count_pct"] = df.administered_count / df.administered_count_all
        df["persons_fully_vaccinated_pct"] = (
            df.persons_fully_vaccinated / df.persons_fully_vaccinated_all
        )

        del df["administered_count_all"]
        del df["persons_fully_vaccinated_all"]

        dfs[df_name].append(df)

for df_name in dfs:
    df = pd.concat(dfs[df_name])
    df["report_date"] = pd.to_datetime(df.report_date)
    outfile = outfiles[df_name] + "_daily.csv"
    if os.path.exists(outfile):
        archive = pd.read_csv(outfile)
    else:
        archive = pd.DataFrame()
    df = df.append(archive)
    df.to_csv(outfile, index=False)

    current = df[df.report_date == df.report_date.max()]
    current.to_csv(outfiles[df_name] + "_current.csv")