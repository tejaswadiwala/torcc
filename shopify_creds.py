# Populate the below through Shopify

class ShopifyCreds():
    def __init__(self):
        self.shop_name = 'toronto-clothing-company'
        self.api_key = ''
        self.api_password = ''
        self.access_token = ''
        self.headers = {'X-Shopify-Access-Token': f'{self.access_token}'}
        self.pickup_store_id = 71976157433
  