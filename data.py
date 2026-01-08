import os
import json
from pathlib import Path
from urllib3.util import Retry

import dotenv
import requests
from requests.adapters import HTTPAdapter

dotenv.load_dotenv()
data_dir = Path("data")
sulpub_key = os.environ.get("SULPUB_KEY")
sulpub_host = "sul-pub-cap-uat.stanford.edu"

def main() -> None:
    fetch_sulpub_data()
    # assign_orcids()
    # filter
    # compare 


def fetch_sulpub_data() -> None:
    jsonl_file = data_dir / "sulpub.jsonl"
    if jsonl_file.is_file():
        print("skipping download of sulpub data since data/sulpub.jsonl exists")
        return

    print(f"writing {jsonl_file}")
    with jsonl_file.open("w") as jsonl_output:
        for sulpub_pub in _publications():
            jsonl_output.write(json.dumps(sulpub_pub) + "\n")


def _publications():
    # configure an http client that retries 5 times
    http = requests.Session()
    retries = Retry(connect=5, read=5)
    http.mount("https://", HTTPAdapter(max_retries=retries))

    # set some variables for all the http requests
    url = f"https://{sulpub_host}/publications.json"
    http_headers = {"CAPKEY": sulpub_key}
    params = {"per": 1000}

    # loop through each page and yield each record
    page = 0
    more = True
    while more:
        page += 1
        params["page"] = page

        resp = http.get(url, params=params, headers=http_headers)
        resp.raise_for_status()

        records = resp.json()["records"]
        if len(records) == 0:
            more = False
        else:
            yield from records


if __name__ == "__main__":
    main()
