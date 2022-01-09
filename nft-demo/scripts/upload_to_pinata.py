import os
from pathlib import Path
import requests
from requests.api import head

PINATA_BASE_URL = "https://api.pinata.cloud/"
endpoint = "pinning/pinFileToIPFS"
headers = {
    "pinata_api_key": os.getenv("PINATA_API_KEY"),
    "pinata_secret_api_key": os.getenv("PINATA_API_SECRET"),
}


def upload_to_pinata(filepath):
    filename = filepath.split("/")[-1:][0]
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        response = requests.post(
            PINATA_BASE_URL + endpoint,
            files={"file": (filename, image_binary)},
            headers=headers,
        )
        # print(response.json())
        # print(response.json()["IpfsHash"])
        return response.json()["IpfsHash"]


def main(filepath):
    upload_to_pinata(filepath)
