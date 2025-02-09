import pandas as pd
from google.cloud import storage
from io import BytesIO
from endpoints.requests import get_all_assets, get_asset_history, get_conversion_rates

def convert_to_parquet(data, filename):
    df = pd.DataFrame(data)
    parquet_file = BytesIO()
    df.to_parquet(parquet_file, engine='pyarrow', index=False)
    parquet_file.seek(0)
    return parquet_file, filename

def upload_to_bucket(parquet_file, bucket_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_file(parquet_file)
    print(f'Arquivo enviado para o bucket {bucket_name} como {destination_blob_name}')

def process_asset_history():
    all_assets = get_all_assets(limit=2000)
    all_history = []
    if all_assets:
        for asset in all_assets['data']:
            asset_id = asset['id']
            print(f"Obtendo histórico para o ativo {asset_id}...")
            asset_history = get_asset_history(asset_id)
            if asset_history and 'data' in asset_history:
                for entry in asset_history['data']:
                    entry['id'] = asset_id
                all_history.extend(asset_history['data'])
    return all_history

def main():   
    all_assets = get_all_assets(limit=2000)       
    if all_assets:
        parquet_file, filename = convert_to_parquet(all_assets['data'], 'all_assets_data.parquet')
        upload_to_bucket(parquet_file, 'extractor_coincap_api', filename)

    conversion_rates = get_conversion_rates()
    if conversion_rates:
        parquet_file, filename = convert_to_parquet(conversion_rates['data'], 'conversion_rates_data.parquet')
        upload_to_bucket(parquet_file, 'extractor_coincap_api', filename)
    
    all_history = process_asset_history()
    if all_history:
        parquet_file, filename = convert_to_parquet({'data': all_history}, 'all_assets_history.parquet')
        upload_to_bucket(parquet_file, 'extractor_coincap_api', filename)

if __name__ == "__main__":
    main()


