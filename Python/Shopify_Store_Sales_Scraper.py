import time
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# A function to utilize Selenium to crawl the Meta Ads Library and grab needed ads links 
def get_facebook_ads():

    past_date = (datetime.now() - timedelta(days=3)).strftime("%m/%d/%Y")
    meta_cta_buttons = ['Get Offer', 'Open Link', 'Order Now', 'Save', 'Shop Now', 'Subscribe', 'Learn More', 'Contact Us', 'Download']
    unique_store_urls = set()

    try:
        # Initialize the browser and navigate to the page
        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        browser.get("https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=ALL&q=%22%20%22&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped&search_type=keyword_exact_phrase&media_type=all")
        # (In working order): Look for keyword, make it clickable, clear existing data in box, enter new info, keep page open for 10 seconds
        search_box = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search by keyword or advertiser']")))
        search_box.click()
        search_box.clear()
        search_box.send_keys("" "" + Keys.ENTER)
        time.sleep(3)
        filters_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[5]/div[2]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]")))
        filters_button.click()
        time.sleep(3)
        
        # [Popup] Activating the filters (English, active ads, date from (last 2 days) to today)
        filters_language_dropdown = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[text()='All languages']")))
        filters_language_dropdown.click()
        time.sleep(3)
        filters_language_selector_en = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[text()='English']")))
        filters_language_selector_en.click()
        time.sleep(3)
        ## click out of dropdown selector
        click_out = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@role='combobox']//div//div//div//div//div//div//div[contains(text(),'English')]")))
        click_out.click()
        time.sleep(3)
        filters_active_status = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Active and inactive']")))
        filters_active_status.click()
        time.sleep(3)
        filters_active_selector = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Active ads']")))
        filters_active_selector.click()
        time.sleep(3)
        # scroll into view of date element
        pg_down = browser.find_element(By.XPATH, "//input[@placeholder='mm/dd/yyyy']")
        pg_down.location_once_scrolled_into_view
        filters_from_date = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='mm/dd/yyyy']")))
        filters_from_date.click()
        filters_from_date.send_keys(Keys.CONTROL, "a")
        filters_from_date.send_keys(Keys.BACK_SPACE)
        filters_from_date.send_keys(past_date)
        time.sleep(3)
        ## apply all filters
        filters_apply = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//body[1]/div[5]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[3]/div[1]/div[2]/div[1]")))
        filters_apply.click()
        time.sleep(5)

        # Now we must go through each ad tablet and output `unique` CTA urls
        starting_element = browser.find_element(By.XPATH, "//body/div/div/div[@role='main']/div/div/div/div/div/div/div[4]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]")
        starting_element.click()
        time.sleep(1)
        starting_element.click()
        time.sleep(3)

        # actual tabbing process, with a starting point and the next element being reassigned to the initial, to tab to
        for i in range(50):
            starting_element.send_keys(Keys.TAB)
            tab_wait = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//body/div/div/div[@role='main']/div/div/div/div/div/div/div[4]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]")))
            starting_element = browser.switch_to.active_element
            # check for a set of keywords when a CTA button is targeted, if matched then extract URL from source
            if starting_element.aria_role == 'button':
                button_text = starting_element.text
                if button_text in meta_cta_buttons:
                    parent_element = starting_element.find_element(By.XPATH, "..")
                    while (True):
                        if parent_element.tag_name != 'a':
                            # moves up element ancestry chain 
                            parent_element = parent_element.find_element(By.XPATH, "..") 
                        else:
                            cta_url = parent_element.get_attribute('href')
                            # store links in a set
                            unique_store_urls.add(cta_url)
                            break
            else:
                continue
        # prints numbered list of urls
        print("\n")
        for index, value in enumerate(unique_store_urls, start=1):
            print(f"{index}. {value}")            
    except Exception as e:
        print(e)
        browser.quit() 

# A function that will first crawl the web to scrape all active 'shopify' stores
def get_shopify_stores(site_url):
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