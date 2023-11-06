from ShopifyController import ShopifyController
from shopify_creds import ShopifyCreds
import requests
shopify_creds = ShopifyCreds()

shopify_controller = ShopifyController()

NEW_SIZES = ['2X Large', '3X Large', '4X Large']

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
                for product in products:
                    update_product(product['id'])
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


def update_product(id):
    product = shopify_controller.get_product_by_id(id)
    image_ids, price = get_image_ids_and_price(product)
    print(image_ids, price)
    new_variants = get_new_variant_data(image_ids, price)

    product['product']['variants'].extend(new_variants)

    shopify_controller.update_product(id, product)

    updated_product = shopify_controller.get_product_by_id(id)
    
    update_images_of_new_variants(updated_product, image_ids)

def get_image_ids_and_price(product):
    image_ids = {}
    for variant in product['product']['variants']:
        if variant['option1'] in image_ids:
            continue
        else:
            image_ids[variant['option1']] = variant['image_id']
            price = variant['price']

    return image_ids, price

def get_new_variant_data(image_ids, price):
    new_variants = []
    for image in list(image_ids.keys()):
        for size in NEW_SIZES:
            new_variant = {
                "option1": image,
                "option2": size,
                "price": price,
                "inventory_quantity": 50,
                "image_id": image_ids[image],
            }
            new_variants.append(new_variant)
    return new_variants

def update_images_of_new_variants(updated_product, image_ids):
    for variant in updated_product['product']['variants']:
        if variant['option2'] in NEW_SIZES:
            variant['image_id'] = image_ids[variant['option1']]
            del variant['inventory_quantity']
            new_variant_data = {
                'variant': variant
            }
            shopify_controller.update_variant(variant['id'], new_variant_data)

main()