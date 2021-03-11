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
    archive_data["report_date"] = pd.to_datetime(archive_data.report_date)
else:
    archive_data = pd.DataFrame()

new_data = pd.DataFrame(data["VaccineAdministration"])
new_data.columns = new_data.columns.str.replace(
    r"(?<!^)(?<!_)(?=[A-Z])", "_", regex=True
).str.lower()
new_data["report_date"] = pd.to_datetime(new_data.report_date)
new_data["administered_doses_per_100k"] = (
    new_data.administered_count / new_data.population * 100_000
)
# datawrapper needs percents, not decimals
new_data["pct_vaccinated_population"] = new_data.pct_vaccinated_population * 100

new_data = new_data.drop_duplicates()

############### OUTPUT ###############

# DAILY BY COUNTY
archive = archive_data.append(new_data).sort_values("update_date")
archive.drop_duplicates().to_csv(archive_file, index=False)

# DAILY STATEWIDE
statewide_archive = archive[archive.county_name == "Illinois"]
statewide_archive.to_csv(
    "output/idph_vaccine_administration_data_daily_statewide.csv", index=False
)

# CURRENT BY COUNTY
new_data["census_county_name"] = new_data.county_name.apply(lambda n: f"{n} County, IL")
new_data = new_data[
    ["census_county_name"] + [c for c in new_data if c != "census_county_name"]
]
# ensure statewide number is top row for datawrapper
# then sort by vax rate to set the default datawrapper sort view
outfile = new_data[new_data.county_name == "Illinois"].append(
    new_data[new_data.county_name != "Illinois"].sort_values(
        "pct_vaccinated_population", ascending=False
    )
)
outfile.to_csv(
    "output/idph_vaccine_administration_data_current_by_county.csv", index=False
)

# CURRENT STATEWIDE
new_data_statewide = new_data[new_data.county_name == "Illinois"]

# sort by vax rate to set the default datawrapper sort view
new_data_statewide.sort_values("pct_vaccinated_population", ascending=False).to_csv(
    "output/idph_vaccine_administration_data_current_statewide.csv", index=False
)