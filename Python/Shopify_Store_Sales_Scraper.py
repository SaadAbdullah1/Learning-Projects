import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# A function to utilize Selenium to crawl the Meta Ads Library and grab needed ads links 
def get_facebook_ads():
    try:
        # Initialize the browser and navigate to the page
        browser = webdriver.Chrome(executable_path="C:\\Users\\SaadAbdullah\\OneDrive\\Programming\\Learning-Projects\\chromedriver.exe")
        browser.get("https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&q=%22%20%22&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped&search_type=keyword_exact_phrase&media_type=all&content_languages[0]=en")
        # (In working order): Look for keyword, make it clickable, clear existing data in box, enter new info, keep page open for 10 seconds
        search_box = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search by keyword or advertiser']")))
        search_box.click()
        search_box.clear()
        search_box.send_keys("" "" + Keys.ENTER)
        time.sleep(10)

    except Exception as e:
        print(e)
        browser.quit() 

    # # Select a filter
    # filter_button = browser.find_element_by_xpath('//button[@data-testid="adlibrary_filter_toggle"]')
    # filter_button.click()

    # # Find the checkbox for the desired filter
    # filter_checkbox = browser.find_element_by_xpath('//input[@data-testid="adlibrary_filter_political_org"]')
    # filter_checkbox.click()

    # # Apply the filter
    # apply_button = browser.find_element_by_xpath('//button[@data-testid="adlibrary_filter_apply"]')
    # apply_button.click()

    # # Find the first advertisement and click on the call-to-action button
    # ad = browser.find_element_by_xpath('//div[@data-testid="ad_preview"]')
    # cta_button = ad.find_element_by_xpath('.//a[@data-testid="ad_preview_cta_link"]')
    # cta_button.click()

    # # Output the URL of the advertisers landing page
    # advertisers_url = browser.current_url
    # print(advertisers_url)

    # # Close the browser
    # browser.quit()

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

#------------------------------------------------------------------------------------------------------------------------------#
# This is the steps PPSPY utilizes for scraping store data (According to a posting on Stackoverflow)
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


# MAIN EXECUTION 
def main():
    get_facebook_ads()
    
if __name__ == "__main__":
    main()