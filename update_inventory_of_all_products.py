import requests
from shopify_creds import ShopifyCreds

shopify_creds = ShopifyCreds()

def main():
    try:
        print(f'Main function started now.')
        page_count = 1
        
        done = False
        url = f'https://{shopify_creds.api_key}:{shopify_creds.api_password}@{shopify_creds.shop_name}.myshopify.com/admin/api/2022-10/products.json'
            
        # Loop until all pages have been retrieved
        while not done:
            print(f'GET all products request started.')
            response = requests.get(url, headers=shopify_creds.headers)
            products = response.json()['products']
            print(f"Page {page_count}, products fetched: {len(products)}")
            
            # If the request was successful, print the response data
            if response.status_code == 200:
                print(f'GET request successful.')
                update_inventory(products)
            else:
                response.raise_for_status()

            # Get the URL for the next page of data from the Link header
            next_url = None
            link_header = response.headers.get('Link')
            if link_header:
                links = link_header.split(',')
                for link in links:
                    if 'rel="next"' in link:
                        next_url = link[link.index('<')+1:link.index('>')]
                        page_count += 1
                        print(f"Paginating now, next page url: {next_url}")
                        break

            # If there is no next URL, set the done flag to True to exit the loop
            if not next_url:
                done = True

            # Set the URL for the next iteration to the URL for the next page of data
            url = next_url
                    
        print(f'Main function completed execution.')
        return products
    except Exception as e:
        print(f'Error occured in the main function : {e}')
        raise

def update_inventory(products=None):
    try:
        print(f'Updating inventory started.')
        for product in products:
            variants = product['variants']
            for variant in variants:
                if variant['inventory_quantity'] < 50:
                    print(f"Product id: {product['id']}, Variant id: {variant['id']}")
                    inventory_item_id = variant['inventory_item_id']
                    url = f'https://{shopify_creds.api_key}:{shopify_creds.api_password}@{shopify_creds.shop_name}.myshopify.com/admin/api/2022-10/inventory_levels/set.json'
                    data = create_data_for_updating_inventory(inventory_item_id)
                    response = requests.post(url, json=data, headers=shopify_creds.headers)
                    if response.status_code == 200:
                        print(f'Inventory updated, inventory_item_id: {inventory_item_id}')
                        print(response.json())
                    else:
                        response.raise_for_status()
        print(f'Completed updating inventory.')
    except Exception as e:
        print(f'Error occured while updating products to Shopify: {e}')
        raise

def create_data_for_updating_inventory(inventory_item_id):
    data = {
        'inventory_item_id': inventory_item_id,
        'location_id': shopify_creds.pickup_store_id, 
        'available': 50
    }

    return data

main()