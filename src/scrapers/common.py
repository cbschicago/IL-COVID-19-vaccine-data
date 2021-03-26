import time
import requests
import warnings


def get_with_retry(url, headers, max_tries=5):
    time.sleep(1)  # always delay
    tries = 0
    while tries < max_tries:
        try:
            resp = requests.get(url, headers=headers)
        except Exception as e:
            warnings.warn(
                f"request to url {url} failed. retrying [{tries + 1}/{max_tries}]\nError was {str(e)}"
            )
            time.sleep(300)
        else:
            return resp
    else:
        raise requests.RequestException(f"request to {url} failed")


idph_vaccine_request_headers = {
    "Connection": "keep-alive",
    "sec-ch-ua": "^\\^Google",
    "accept": "application/json,*/*",
    "sec-ch-ua-mobile": "?0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Origin": "http://www.dph.illinois.gov",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "http://www.dph.illinois.gov/",
    "Accept-Language": "en-US,en;q=0.9",
}