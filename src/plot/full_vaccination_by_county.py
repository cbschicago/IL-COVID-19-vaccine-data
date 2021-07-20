import numpy as np
import pandas as pd
import geopandas as gpd

# ILLINOIS
gdf = gpd.read_file("input/acs2019_5yr_B01003_05000US17071.geojson")
df = pd.read_csv("output/idph_vaccine_administration_data_current_by_county.csv")

fig = (
    gdf.merge(df, how="inner", left_on="name", right_on="census_county_name")
    .plot("pct_vaccinated_population", figsize=(12, 18), cmap="RdYlGn", legend=True)
    .get_figure()
)

filename = "output/img/il_current_vaccination_rate_by_county"
fig.savefig(f"{filename}.png", facecolor="white")
fig.savefig(f"{filename}.svg", facecolor="white")

# INDIANA
gdf = gpd.read_file("input/acs2019_5yr_B01003_05000US18147.geojson")
gdf["name"] = gdf.name.apply(lambda name: name.split(" County")[0].strip())
gdf["name"] = gdf.name.str.replace(" ", "").str.replace(".", "").str.lower()
df = pd.read_excel(
    "https://hub.mph.in.gov/dataset/145a43b2-28e5-4bf1-ad86-123d07fddb55/resource/82d99020-093f-41ac-95c7-d3c335b8c2ba/download/county-vaccination-demographics.xlsx"
)
df = df.replace("Suppressed", np.NaN)
df["county"] = df.county.str.replace(" ", "").str.replace(".", "").str.lower()
df["fully_vaccinated"] = df.fully_vaccinated.astype(float)
df = df.groupby("county").fully_vaccinated.sum().to_frame("persons_fully_vaccinated")
gdf = gdf.merge(df, how="left", left_on="name", right_index=True)
gdf["pct_fully_vaccinated"] = gdf.persons_fully_vaccinated / gdf["B01003001"] * 100

fig = gdf.plot(
    "pct_fully_vaccinated", figsize=(12, 18), cmap="RdYlGn", legend=True
).get_figure()

filename = "output/img/in_current_vaccination_rate_by_county"
fig.savefig(f"{filename}.png", facecolor="white")
fig.savefig(f"{filename}.svg", facecolor="white")
