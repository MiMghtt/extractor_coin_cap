import requests
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="config/api_auth.env")  

BASE_URL = "https://api.coincap.io/v2"

def get_data(endpoint, params=None):  
    bearer_token = os.getenv("API_KEY")  
    url = f"{BASE_URL}/{endpoint}"

    if bearer_token is None:
        print('Erro na chave da API')
        exit()

    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Accept-Encoding": "gzip"
    }

    response = requests.get(url, headers=headers, params=params)  
    
    if response.status_code == 200:
        assets = response.json()  
        return assets
    else:
        print(f"Erro ao acessar {url}: {response.status_code}")
        return None

def get_paginated_data(endpoint, params=None):
    offset = 0
    all_data = []

    while True:
        params["offset"] = offset
        data = get_data(endpoint, params)
        
        if data and "data" in data:
            all_data.extend(data["data"])
            if len(data["data"]) < params["limit"]:
                break
            offset += params["limit"]
        else:
            break
    
    return {"data": all_data}

def get_all_assets(limit=2000):
    endpoint = "assets"
    params = {"limit": limit}
    return get_paginated_data(endpoint, params)

def get_asset_history(asset_id, interval="d1", limit=500):
    endpoint = f"assets/{asset_id}/history"
    params = {"interval": interval, "limit": limit}
    return get_paginated_data(endpoint, params)

def get_conversion_rates():
    endpoint = "rates"
    return get_data(endpoint)
