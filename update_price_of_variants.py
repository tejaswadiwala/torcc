import time
import requests
from shopify_creds import ShopifyCreds
import categories as c

shopify_creds = ShopifyCreds()

# Change this
#categories = [c.PremiumBackHoodies(), c.PremiumFrontHoodies(), c.PremiumFrontSweatshirts(), c.PremiumBackSweatshirts(), c.SignatureToronnoHoodies(), c.SignatureToronnoSweatshirt(), 
#              c.SignatureWTNHoodies(), c.SignatureWTNSweatshirts(), c.ClassicSweatshirt(), c.ClassicHoodie(), c.TorccCollectionHoodies(), c.TorccCollectionSweatshirts(), c.NewHoodies(),
#             c.Oversized()]

categories = [c.ClassicTees()]

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
                update_variants(products)
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

def update_variants(products=None):
    try:
        print(f'Updating variants started.')
        rate_limit_products = []
        for category in categories:
            PRICE = category.price
            COMPARE_AT_PRICE = category.compare_at_price
            PRODUCT_NAME_CONTAINS = category.products
            for product in products:
                for PRODUCT_NAME_CONTAIN in PRODUCT_NAME_CONTAINS:
                    # Uncomment the below line if you want to update T-shirt
                    # if product['product_type'] == 'T-shirt':
                    if PRODUCT_NAME_CONTAIN in product['title']:
                        variants = product['variants']
                        for variant in variants:
                            url = f"https://{shopify_creds.api_key}:{shopify_creds.api_password}@{shopify_creds.shop_name}.myshopify.com/admin/api/2022-10/variants/{variant['id']}.json"
                            variant_data = create_data_for_updating_variants(product['id'], variant['id'], PRICE, COMPARE_AT_PRICE)
                            response = requests.put(url, json=variant_data, headers=shopify_creds.headers)
                            if response.status_code == 200:
                                data = response.json()
                                print(data)
                            elif response.status_code == 429:
                                print('I am in rate limit.')
                                rate_limit_products.append(variant['id'])
                                time.sleep(1)
                                response = requests.put(url, json=variant_data, headers=shopify_creds.headers)
                            else:
                                response.raise_for_status()
        print(f'Products affected by rate limit: {rate_limit_products}')
        print(f'Completed updating variants.')
    except Exception as e:
        print(f'Products affected by rate limit: {rate_limit_products}')
        print(f'Error occured while updating variants on Shopify: {e}')
        raise

def create_data_for_updating_variants(product_id, variant_id, PRICE, COMPARE_AT_PRICE):
    data = {
    "variant": {
        "id": variant_id,
        "product_id": product_id,
        "price": PRICE,
        "compare_at_price": COMPARE_AT_PRICE
        }
    }   
    return data

main()