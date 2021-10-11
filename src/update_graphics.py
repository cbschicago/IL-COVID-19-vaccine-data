import os
import warnings
from datawrapper import Datawrapper
import dotenv

dotenv.load_dotenv()

dw_api_token = os.getenv("DATAWRAPPER_API_TOKEN")
assert dw_api_token, "couldn't locate datawrapper api token"
dw = Datawrapper(access_token=dw_api_token)

charts = [
    "g7EuE",
    "GvEK6",
    "TIIA3",
    "xl8sT",
    "qV77i",
    "Hq3Ai",
    "bvbM8",
    "Z1ofc",
]

for chart_id in charts:
    resp = dw.refresh_data(chart_id)
    if resp.status_code == 204:
        print(f"refreshed data for chart with id {chart_id}")
    else:
        warnings.warn(
            f"refreshing data for chart id {chart_id} returned code "
            f"{resp.status_code}, not 204"
        )
