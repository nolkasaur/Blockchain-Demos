from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import get_camPos
from metadata.sample_metadata import metadata_template
from pathlib import Path
from scripts.upload_to_pinata import upload_to_pinata
import json

# import requests


def main():
    advanced_collectible = AdvancedCollectible[-1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_advanced_collectibles} collectibles!")
    for token_id in range(number_of_advanced_collectibles):
        camPos = get_camPos(advanced_collectible.tokenIdToCamPos(token_id))
        metadata_file_path = (
            f"./metadata/{network.show_active()}/{token_id}-{camPos}.json"
        )
        collectible_metadata = metadata_template
        if Path(metadata_file_path).exists():
            print(f"{metadata_file_path} already exists! Delete it to overwrite")
        else:
            print(f"Creating metadata file: {metadata_file_path}")
            collectible_metadata["name"] = camPos
            collectible_metadata["description"] = f"Teddy number {camPos}!"
            image_path = "./img/" + camPos.lower() + ".png"
            # image_uri = upload_to_ipfs(image_path)
            filename = image_path.split("/")[-1:][0]
            print("Uploading image to Pinata!")
            image_uri = f"https://ipfs.io/ipfs/{upload_to_pinata(image_path)}?filename={filename}"
            print(f"Image URI: {image_uri}")
            collectible_metadata["image_uri"] = image_uri
            with open(metadata_file_path, "w") as file:
                json.dump(collectible_metadata, file)
            print("Uploading JSON to Pinata!")
            metadata_file_name = metadata_file_path.split("/")[-1:][0]
            json_uri = f"https://ipfs.io/ipfs/{upload_to_pinata(metadata_file_path)}?filename={metadata_file_name}"
            print(f"JSON URI: {json_uri}")


# def upload_to_ipfs(filepath):
#     with Path(filepath).open("rb") as fp:
#         image_binary = fp.read()
#         ipfs_url = "http://127.0.0.1:5001"
#         endpoint = "/api/v0/add"
#         response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
#         ipfs_hash = response.json()["Hash"]
#         filename = filepath.split("/")[-1:][0]
#         image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
#         print(image_uri)
#         return image_uri
