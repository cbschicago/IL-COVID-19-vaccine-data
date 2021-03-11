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

archive_file = "output/idph_vaccine_administration_data_daily_by_county.csv"
if os.path.exists(archive_file):
    archive_data = pd.read_csv(archive_file)
    archive_data["update_date"] = pd.to_datetime(archive_data.update_date)
    last_archived_date = archive_data.update_date.max()
else:
    archive_data = pd.DataFrame()
    last_archived_date = pd.Timestamp(1900, 1, 1)

if last_updated_date > last_archived_date:
    new_data = pd.DataFrame(data["VaccineAdministration"])
    new_data.columns = new_data.columns.str.replace(
        r"(?<!^)(?<!_)(?=[A-Z])", "_", regex=True
    ).str.lower()
    new_data["update_date"] = last_updated_date
    new_data["administered_doses_per_100k"] = (
        new_data.administered_count / new_data.population * 100_000
    )

    archive = archive_data.append(new_data).sort_values("update_date")
    archive.drop_duplicates().to_csv(archive_file, index=False)

    new_data["census_county_name"] = new_data.county_name.apply(
        lambda n: f"{n} County, IL"
    )
    new_data.drop_duplicates().to_csv(
        "output/idph_vaccine_administration_data_current_by_county.csv", index=False
    )
