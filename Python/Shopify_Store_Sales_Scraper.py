
import requests
from bs4 import BeautifulSoup

# A function that will first crawl the web to scrape all active 'shopify' stores
def get_shopify_stores():
    shops = []
    url = 'https://www.google.com/search?q=site:shopify.com'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    links = soup.find_all('a')

    for link in links:
        shop = link.get('href')
        if shop and 'shopify.com' in shop:
            if shop.startswith('/url?q='):
                shop = shop[7:]
                if '&sa=' in shop:
                    shop = shop.split('&sa=')[0]
            shops.append(shop)
    
    print("Found the following Shopify stores:")
    for shop in shops:
        print(" -", shop)

get_shopify_stores()
#------------------------------------------------------------------------------------------------------------------------------#
# This is the steps PPSPY utilizes for scraping store data (According a posting on Stackoverflow)
#-------------------------------------------------------------------------------------------------------------------------------
# 1. Reads your Shopify sitemap to find the products in the store. .../sitemap_products_1.xml
# 2. As fallback, it parses the URL: .../collections/all?sort_by=best-selling - and tries to find the products there.
# 3. Next, it uses the JSON URL from Shopify. There again it tries to find all products. An example URL: 
#    .../products.json?page=1&limit=250 - most store owners don't even know this exists.
# 4. After that, it calls the JSON URL for each product. You can get this URL in your online store by simply opening a product 
#    page and writing ".json" after it in the URL. Example URL: .../products/your-productname.json.
# 
# In this JSON there is a field "updated_at". This field is updated every time a change is made. Also, when an order take place (the stock is changed).
# And with this, it is possible to track the sales (approximately).
#------------------------------------------------------------------------------------------------------------------------------#

