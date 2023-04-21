import requests
import json

from shopify_creds import ShopifyCreds

shopify_creds = ShopifyCreds()

# Replace with your own values
SHOP_DOMAIN = f'{shopify_creds.shop_name}.myshopify.com'
API_KEY = shopify_creds.api_key
PASSWORD = shopify_creds.api_password
PRODUCT_TYPE = 'Oversized T-shirt'
NEW_WEIGHT = 0.25

# First, get a list of all products with the specified product type
url = f'https://{API_KEY}:{PASSWORD}@{SHOP_DOMAIN}/admin/api/2021-07/products.json?product_type={PRODUCT_TYPE}&fields=id'
response = requests.get(url, headers = shopify_creds.headers)
products = response.json()['products']

# Next, update the weight of each product variant
for product in products:
    product_id = product['id']
    url = f'https://{API_KEY}:{PASSWORD}@{SHOP_DOMAIN}/admin/api/2021-07/products/{product_id}/variants.json?fields=id,weight'
    response = requests.get(url, headers=shopify_creds.headers)
    variants = json.loads(response.text)['variants']
    print(f'Updating variants: {variants}')
    for variant in variants:
        variant_id = variant['id']
        print(f'Product Id: {product_id}, Variant Id: {variant_id}')
        url = f'https://{API_KEY}:{PASSWORD}@{SHOP_DOMAIN}/admin/api/2022-10/variants/{variant_id}.json'
        payload = {
        "variant": {
            "id": variant_id,
            "product_id": product_id,
            "weight": NEW_WEIGHT
            }
        }
        response = requests.put(url, headers=shopify_creds.headers, data=json.dumps(payload))
        print(response.text)
