import requests
import base64
import os
import sys
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from torcc.shopify_creds import ShopifyCreds
from Product import Product

VENDOR = 'TORCC'

# Get Shopify credentials
sc = ShopifyCreds()

# Set up the authentication and request headers
shopify_domain = f'{sc.shop_name}.myshopify.com'
api_key = sc.api_key
password = sc.api_password
headers = sc.headers
auth = (api_key, password)

# Change the product below to the required Product
product = Product.ToteTshirtCoordSet()

NAME = 'Inspire'
SIZES = ['11L']
OPTION_1 = 'Color'
OPTION_2 = 'Size'

def create_product():
    print('Create Product Starting Now. ')
    variants, options = create_product_variants_and_options()
    # Set up the product data
    product_data = {
        'product': {
            'title': f'{NAME}{product.title}',
            'body_html': f'{product.body_html}',
            'product_type': f'{product.product_type}',
            'template_suffix': f'{product.template_suffix}',
            'vendor': VENDOR,
            'variants': variants, 
            'options': options
        }
    }

    # Add images to product data
    images = []
    for filename in os.listdir('add_product/import'):
        if filename.endswith('.jpg'):
            with open(f'add_product/import/{filename}', 'rb') as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                images.append({
                    'attachment': encoded_string,
                    'filename': filename,
                    'alt': f'{os.path.splitext(filename)[0]} {NAME}{product.title}'
                })

    print(f"Product Data: {json.dumps(product_data)}")

    product_data['product']['images'] = images

    try:
        # Make the request to create the product
        response = requests.post(f'https://{shopify_domain}/admin/api/2021-10/products.json', headers=headers, auth=auth, json=product_data, timeout=30)
        print(response.text)
        response.raise_for_status()
        product_id = response.json()['product']['id']
        print(f'Product created successfully with ID {product_id}')
        
        return product_id
        
    except Exception as e:
       print('Product creation failed: %s', e)
       raise

def get_image_data_for_product(product_id):
    try:
        print('Get Image Data for Product: Starting now.')
        # Make the request to get the product information
        response = requests.get(f'https://{shopify_domain}/admin/api/2021-10/products/{product_id}.json', headers=headers, auth=auth)
        response.raise_for_status()
        product_info = response.json()['product']

        # Extract image ids
        images = []
        for image in product_info['images']:
            images.append(image)

        print('Get Image Data for Product: Successfully completed execution.')
        return images
    except Exception as e:
        print(f'Get Image Data for Product: Error occurred - {e}')
        raise

# Function to update variants
def update_product_variants(product_id, image_info_mapping):
    try: 
        print('Update Product Variants: Starting now.')
        # Build the endpoint URL
        endpoint = f'https://{shopify_domain}/admin/api/2023-04/products/{product_id}/variants.json'

        # Get the existing variants of the product
        response = requests.get(endpoint, headers=headers, auth=auth)
        variants = json.loads(response.text)['variants']
        print(f"Update Product Variants: Variants - {variants}")

        # Loop through the existing variants and update the price and inventory_quantity
        for variant in variants:
            variant_data = {
                'id': variant['id'],
                'price': product.price, 
                'image_id': image_info_mapping[variant['option1']]
            }
            put_endpoint = f'https://{shopify_domain}/admin/api/2023-04/variants/{variant["id"]}.json'
            response = requests.put(put_endpoint, headers=headers, auth=auth, json={'variant': variant_data})
            if variant['inventory_quantity'] < 50:
                update_inventory(variant)
            if response.status_code == 200:
                print(f'Variant {variant["id"]} updated successfully')
            else:
                print(f'Error updating variant {variant["id"]}: {response.text}')
    
        print('Update Product Variants: Successfully completed execution.')
    except Exception as e:
        print(f"Update Product Variants: Error occurred - {e}")
        raise

def update_inventory(variant):
    url = f'https://{sc.api_key}:{sc.api_password}@{sc.shop_name}.myshopify.com/admin/api/2022-10/inventory_levels/set.json'
    data = {
        'inventory_item_id': variant['inventory_item_id'],
        'location_id': sc.pickup_store_id, 
        'available': 50
    }
    response = requests.post(url, json=data, headers=sc.headers)
    if response.status_code == 200:
        print(f"Inventory updated, inventory_item_id: {variant['inventory_item_id']}")
        print(response.json())
    else:
        response.raise_for_status()

def populate_image_info_mapping(images):
    try:
        image_info_mapping = {}
        print(f'Populate Image Info Mapping: Starting now.')
        for image in images:
            color_name = image['alt'].split(f'{NAME}{product.title}')[0].strip()
            image_info_mapping[color_name] = image['id']
        print(f'Populate Image Info Mapping: Successfully completed execution.')
        return image_info_mapping
    except Exception as e:
        print(f'Get Image Data for Product: Error occurred - {e}')
        raise

def create_product_variants_and_options():
    print('Create Product Variants Starting Now. ')
    
    # Set up the variant data
    variants = []
    color_names = []

    # Loop through the files in the import folder
    for filename in os.listdir('add_product/import'):
        if filename.endswith('.jpg'):
            # Extract the color name from the filename
            color_name = filename.split('.')[0]
            color_names.append(color_name)

            # Loop through the sizes and add a variant for each size
            for size in SIZES:
                variant = {
                    "title": f'{color_name}-{size}',
                    "option1": color_name,
                    "option2": size,
                    "inventory_management": "shopify",
                    "price": f'{product.price}'
                }
                variants.append(variant)

    options = get_options(color_names)

    print('Create Product Variants Successfully Completed Execution. ')
    return variants, options

def get_options(color_names): 
    return [
        {
        "name": OPTION_1,
        "values": color_names
        },
        {
        "name": OPTION_2,
        "values": SIZES
        }
    ]

if __name__ == '__main__':
    product_id = create_product()
    images = get_image_data_for_product(product_id)
    print(images)
    image_info_mapping = populate_image_info_mapping(images)
    print(image_info_mapping)
    update_product_variants(product_id, image_info_mapping)