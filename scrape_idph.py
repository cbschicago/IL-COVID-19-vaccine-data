import os
import requests
import pandas as pd


resp = requests.get(
    "https://idph.illinois.gov/DPHPublicInformation/api/covidVaccine/"
    "getVaccineAdministrationCurrent"
)
assert resp.status_code == 200, f"request failed with status code {resp.status_code}"
data = resp.json()

last_updated_date = pd.Timestamp(**data["lastUpdatedDate"])

archive_file = "output/idph_vaccine_administration_data.csv"
if os.path.exists(archive_file):
    archive_data = pd.read_csv(archive_file)
    archive_data["update_date"] = pd.to_datetime(archive_data.update_date)
    last_archived_date = archive_data.update_date.max()
else:
    archive_data = pd.DataFrame()
    last_archived_date = pd.Timestamp(1900, 1, 1)

if last_updated_date > last_archived_date:
    df = pd.DataFrame(data["VaccineAdministration"])
    df.columns = df.columns.str.replace(r"(?<!^)(?<!_)(?=[A-Z])", "_").str.lower()
    df["update_date"] = last_updated_date
    df["administered_doses_per_100k"] = df.administered_count / df.population * 100_000
    out = archive_data.append(df)
    out.to_csv(archive_file)
