import requests
import base64
import os
import sys
import logging
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from torcc.shopify_creds import ShopifyCreds

# Set up logging
logging.basicConfig(filename='product_creation.log', level=logging.INFO)

def create_product():
    print('Create Product Starting Now. ')
    # Get Shopify credentials
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
            'title': 'My Product1',
            'body_html': '<p>This is my product description.</p>',
            'vendor': 'TORCC',
            'images': [
                {
                    'attachment': base64.b64encode(open('automate_design/exports/mockup.png', 'rb').read()).decode('utf-8')
                }
            ],
            'variants': [],
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

    # Define the colors and sizes to be used
    colors = ['Red', 'Blue', 'Green']
    sizes = ['S', 'M', 'L', 'XL']

    # Create variants for each file in the "import" folder
    for filename in os.listdir('add_product/import'):
        if filename.endswith('.png'):
            variant_title = filename[:-4]
            print(variant_title)  # Remove the .csv extension

            # Create a variant for each color and size combination
            for color in colors:
                for size in sizes:
                    variant_data = {
                        'title': f'{variant_title} - {color} - {size}',
                        'price': 21.99,
                        'sku': f'MYPROD001-{variant_title}-{color}-{size}',
                        'inventory_management': 'shopify',
                        'inventory_quantity': 10,
                        'images': [
                                {
                                    'attachment': base64.b64encode(open('automate_design/exports/mockup.png', 'rb').read()).decode('utf-8')
                                }
                            ],
                        'option1': color,
                        'option2': size
                    }
                    product_data['product']['variants'].append(variant_data)

    try:
        # Make the request to create the product
        response = requests.post(f'https://{shopify_domain}/admin/api/2021-10/products.json', headers=headers, auth=auth, json=product_data, timeout=30)
        print(response.text)
        # Check for errors in the response
        response.raise_for_status()
        print('Product creation successful.')
        logging.info('Product creation successful: %s', response.json())
        
    except Exception as e:
        logging.error('Product creation failed: %s', e)

if __name__ == '__main__':
    create_product()
