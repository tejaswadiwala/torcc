import requests
from shopify_creds import ShopifyCreds

shopify_creds = ShopifyCreds()

UPDATE_ALL_PRODUCTS = False
PRODUCT_TITLE_TO_BE_CHECKED = 'sweatshirt'
TEMPLATE_SUFFIX = 'sweatshirt'
DATA = {
        'product': {
            'template_suffix': TEMPLATE_SUFFIX
        }
    }


def main():
    try:
        print(f'Getting all products from Shopify.')
        
        done = False
        url = f'https://{shopify_creds.api_key}:{shopify_creds.api_password}@{shopify_creds.shop_name}.myshopify.com/admin/api/2022-10/products.json?status=active&count=true'
            
        # Loop until all pages have been retrieved
        while not done:
            response = requests.get(url, headers=shopify_creds.headers)
            products = response.json()['products']
            print(len(products))
            
            # If the request was successful, print the response data
            if response.status_code == 200:
                print(f'GET request successful.')
                update_product(products)
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
                        print(next_url)
                        break

            # If there is no next URL, set the done flag to True to exit the loop
            if not next_url:
                done = True

            # Set the URL for the next iteration to the URL for the next page of data
            url = next_url
                    
        print(f'Completed getting all products from Shopify.')
        return products
    except Exception as e:
        print(f'Error occured while getting all products from Shopify: {e}')
        raise

def update_product(products=None):
    try:
        print(f'Updating products started.')
        for product in products:
            product_id = product['id']
            if UPDATE_ALL_PRODUCTS or PRODUCT_TITLE_TO_BE_CHECKED in product['title'].lower():
                url = f'https://{shopify_creds.api_key}:{shopify_creds.api_password}@{shopify_creds.shop_name}.myshopify.com/admin/api/2020-04/products/{product_id}.json'
                response = requests.put(url, json=DATA, headers=shopify_creds.headers)
                if response.status_code == 200:
                    print(f'Product updated successfully for product: {product_id}')
                else:
                    response.raise_for_status()
        print(f'Completed updating products.')
    except Exception as e:
        print(f'Error occured while updating products to Shopify: {e}')
        raise

main()