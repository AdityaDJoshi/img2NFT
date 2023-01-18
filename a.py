import requests
import json


def post_to_nftport(name, description, img_path, wallet_address):
    file = open(img_path, "rb")

    query_params = {
        "chain": "polygon",
        "name": name,
        "description": description,
        "mint_to_address": wallet_address
    }
    print(query_params)
    # ans = json.load(open('response.json', 'r'))
    # return ans
    response = requests.post(
        "https://api.nftport.xyz/v0/mints/easy/files",
        headers={"Authorization": "3ca26e7d-6e68-4644-a9cd-72a567f90f44"},
        params=query_params,
        files={"file": file}
    )
    print(response.text)
    jsonFile = open("data.json", "w")
    json.dump(response.json(), jsonFile, ensure_ascii=False)
    jsonFile.close()
    return response.json()
