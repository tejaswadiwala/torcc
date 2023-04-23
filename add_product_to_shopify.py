# This is the most basic way to upload a product

import requests
import base64

from shopify_creds import ShopifyCreds

sc = ShopifyCreds()

# Set up the authentication and request headers
shopify_domain = f'{sc.shop_name}.myshopify.com'
api_key = sc.api_key
password = sc.api_password
headers = sc.headers
auth = (api_key, password)

# Set up the product data
product_data = {
    'product': {
        'title': 'My Product',
        'body_html': '<p>This is my product description.</p>',
        'vendor': 'My Company',
        'variants': [
            {
                'title': 'Default',
                'price': '10.00',
                'sku': 'MYPROD001',
                'inventory_management': 'shopify',
                'inventory_quantity': 10,
                'option1': 'Red',
                'option2': 'S'
            }
        ],
        'images': [
            {
                'attachment': base64.b64encode(open('automate_design/exports/mockup.png', 'rb').read()).decode('utf-8')
            }
        ],
        'options': [
            {
                'name': 'Color'
            },
            {
                'name': 'Size'
            }
        ]
    }
}

# Make the request to create the product
response = requests.post(f'https://{shopify_domain}/admin/api/2021-10/products.json', headers=headers, auth=auth, json=product_data)

# Print the response data
print(response.json())
