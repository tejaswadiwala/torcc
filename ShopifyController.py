import requests
from shopify_creds import ShopifyCreds
import time

shopify_creds = ShopifyCreds()
API_VERSION = "2023-10"
BASE_URL = f"https://{shopify_creds.api_key}:{shopify_creds.api_password}@{shopify_creds.shop_name}.myshopify.com/admin/api/{API_VERSION}"

class ShopifyController:
    def get_product_by_id(self, id):
        product_url = f"{BASE_URL}/products/{id}.json"
        response = requests.get(product_url, headers=shopify_creds.headers)
        product_data = response.json()
        return product_data

    def update_product(self, id, data):
        url = f"{BASE_URL}/products/{id}.json"
        response = requests.put(url, json=data, headers=shopify_creds.headers)
        if response.status_code == 200:
            print(f"Product updated successfully for product: {id}")
        else:
            response.raise_for_status()
    
    def update_variant(self, id, data):
        url = f"{BASE_URL}/variants/{id}.json"
        response = requests.put(url, json=data, headers=shopify_creds.headers)
        if response.status_code == 200:
            data = response.json()
            print(f"Variant updated successfully for variant: {id}")
        elif response.status_code == 429:
            print(f"I am in rate limit - {id}")
            time.sleep(1)
            response = requests.put(url, json=data, headers=shopify_creds.headers)
        else:
            response.raise_for_status()
    
    def delete_variant(self, id):
        url = f"{BASE_URL}/variants/{id}.json"
        response = requests.delete(url, headers=shopify_creds.headers)
        if response.status_code == 200:
            print(f"Variant deleted successfully for variant: {id}")
        elif response.status_code == 429:
            print(f"I am in rate limit - {id}")
            time.sleep(1)
            response = requests.put(url, headers=shopify_creds.headers)
        else:
            response.raise_for_status()

