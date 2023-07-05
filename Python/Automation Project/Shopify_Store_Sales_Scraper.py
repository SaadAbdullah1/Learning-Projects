###-----------------------------------------------------------------------------------------
# -Author: Saad Abdullah
# -Purpose: To help automate the process of finding winning-products VIA the Meta Ads Library
# -Date of Creation: Feb 1, 2023
###-----------------------------------------------------------------------------------------

import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

def load_new_ads(browser):
    actions = ActionChains(browser)
    actions.move_to_element(browser.find_element('xpath', '//a[text() = "Ad Library API"]')).perform()
    try:
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@data-visualcompletion="loading-state"]')))
    except:
        load_new_ads(browser)
        return
    WebDriverWait(browser, 60).until(EC.invisibility_of_element((By.XPATH, '//div[@data-visualcompletion="loading-state"]')))

# A function to utilize Selenium to crawl the Meta Ads Library and grab needed ads links 
def get_facebook_ads():

    # past_date = (datetime.now() - timedelta(days=3)).strftime("%m/%d/%Y")
    past_date = (datetime.now() - timedelta(days=3)).strftime("%m/%d/%Y")
    meta_cta_buttons = ['Get Offer', 'Get offer', 'Open Link', 'Open link', 'Order Now', 'Order now', 'Save', 'Shop Now', 'Shop now', 'Subscribe', 'Contact Us', 'Contact us', 'Download']
    unique_store_urls = set()

    try:

        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        browser.maximize_window()
        browser.get("https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=ALL&q=%22%20%22&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped&search_type=keyword_exact_phrase&media_type=all")
        search_box = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search by keyword or advertiser']")))
        search_box.click()
        search_box.clear()

        #--------------------------------------------------- CHANGE KEYWORD SEARCH TEXT ---------------------------------------------------#
        search_box.send_keys("" "" + Keys.ENTER)
        #--------------------------------------------------- CHANGE KEYWORD SEARCH TEXT ---------------------------------------------------#

        filters_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[text()="Filters"]//ancestor::div[@role="button"]')))
        filters_button.click()
        # # [Popup] Activating the filters (English, active ads, date from (last 2 days) to today)
        filters_language_dropdown = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[text()='All languages']")))
        filters_language_dropdown.click()
        filters_language_selector_en = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[text()='English']")))
        filters_language_selector_en.click()
        # click_out = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@role='combobox']//div//div//div//div//div//div//div[contains(text(),'English')]")))
        # click_out.click()
        browser.find_element('xpath', '//div[text()="Filters" and @role="heading"]').click()
        filters_active_status = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Active and inactive']")))
        filters_active_status.click()
        filters_active_selector = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Active ads']")))
        filters_active_selector.click()
        # scroll into view of date element
        pg_down = browser.find_element(By.XPATH, "//input[@placeholder='mm/dd/yyyy']")
        pg_down.location_once_scrolled_into_view
        filters_from_date = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='mm/dd/yyyy']")))
        filters_from_date.click()
        filters_from_date.send_keys(Keys.CONTROL, "a")
        filters_from_date.send_keys(Keys.BACK_SPACE)
        filters_from_date.send_keys(past_date)

        browser.find_element('xpath', '//div[text()="Filters" and @role="heading"]').click()

        ## apply all filters
        WebDriverWait(browser, 10).until(lambda x: browser.find_element('xpath', '//div[contains(text(),"Apply 3")]//ancestor::div[@role="button"]').get_attribute('aria-disabled') != 'true')
        filters_apply = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[contains(text(),"Apply")]//ancestor::div[@role="button"]')))
        filters_apply.click()

        # Now we must go through each ad tablet and output `unique` CTA urls

        # actual scraping process, with a starting point and the next element being reassigned to the initial, to tab to
        all_ads = []
        cta_ads_traversed = 0
        ads_traversed = 0
        # use user input for requested # of ads to scrape
        num_ads_requested = int(input("\nEnter the # of Ads you want data for (a greater # will take longer to scrape)\n-> "))
        print("\n")
        start_time = time.time()

        while(True):
            print("Scraping...")
            WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class,"_7jyg")]')))
            # time.sleep(2)
            ads = browser.find_elements('xpath', '//div[contains(@class,"_7jyg")]')
            ads = [ad for ad in ads if ad not in all_ads]
            for ad in ads:
                ads_traversed+=1
                # print(f'ads traversed: {ads_traversed}')
                btns = ad.find_elements('xpath', './/div[@role="button"]')
                btn = [btn for btn in btns if btn.text in meta_cta_buttons]
                if btn:
                    btn = btn[0]
                    url = btn.find_element('xpath', './/ancestor::a').get_attribute('href')
                    unique_store_urls.add(url)
                    cta_ads_traversed += 1
            #--------------------------------------------------- CHANGE NUMBER OF ADS TO GRAB LINKS FOR ---------------------------------------------------#
            if len(unique_store_urls) >= num_ads_requested:
            #--------------------------------------------------- CHANGE NUMBER OF ADS TO GRAB LINKS FOR ---------------------------------------------------#
                break
            all_ads.extend(ads)
            # print("Total ads traversed through = ", len(all_ads))
            # browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            load_new_ads(browser)
            time.sleep(2)
        print("Completed.\n")
        print("Total ads traversed through = ", len(all_ads))

        # prints numbered list of urls 
        # for index, url in enumerate(unique_store_urls, start=1):
        #     print(index, url)
        print("\nNumber of URLS requested = ", num_ads_requested, "\nNumber of UNIQUE URLS found = ", len(unique_store_urls))
        end_time = time.time()
        scrape_time = end_time - start_time
        print("\nTotal time(sec) taken to scrape these ads = ", round(scrape_time, 1))
        browser.quit()
        return unique_store_urls
          
    except Exception as e:
        print(e)
        browser.quit() 
        return unique_store_urls

# Automating control of the website 'builtwith.com', to determine if given url is shopfiy store and add them to a verified set
def is_shopify_store(random_unique_urls):
    
    # Initialize the browser and navigate to the page
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    validated_shopify_stores = set()
    # not useful for this script, but for general data
    non_shopify_stores = set()
    non_ecommerce = set()

    # loop given set of urls and check for Shopify platformness
    for i in random_unique_urls:

        browser.get("https://www.builtwith.com")
        search_box = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='q']")))
        search_box.click()
        search_box.clear()
        search_box.send_keys(i, Keys.ENTER)
        # print(i)       

        try:
            # find the `eCommerce` tag, under which website sales platform is found
            ecom_element = browser.find_element(By.XPATH, "//h6[normalize-space()='eCommerce']")
            platform_element = browser.find_element(By.XPATH, "//div[3]//div[1]//div[2]//div[1]//h2[1]//a[1]")
            if ecom_element.text == 'eCommerce' and platform_element.text == "Shopify":
                # print("Is a Shopify ecommerce platform\n")
                validated_shopify_stores.add(i)
            else:
                # print("Is a non-Shopify ecommerce platform\n")
                non_shopify_stores.add(i)
        except NoSuchElementException:
            # print("Not an ecommerce platform at all\n")
            non_ecommerce.add(i)
    
    percent_vss = (len(validated_shopify_stores) / len(random_unique_urls)) * 100
    percent_nss = (len(non_shopify_stores) / len(random_unique_urls)) * 100
    percent_ne = (len(non_ecommerce) / len(random_unique_urls)) * 100

    print("\nFrom the extracted Meta Library of '", len(random_unique_urls), "' total ads:\n->", percent_vss, "%", " are SHOPIFY stores [", len(validated_shopify_stores), "site(s)]\n->", percent_nss, "%" ," are NON-SHOPIFY ecommerce [", len(non_shopify_stores), "site(s)]\n->", percent_ne, "%", " are NON-ECOMMERCE based [", len(non_ecommerce), "site(s)]\n")

    browser.quit()
    return validated_shopify_stores

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
# In this JSON there is a field "updated_at". This field is updated every time a change is made. Also, when an order takes place (the stock is changed).
# And with this, it is possible to track the sales (approximately).
#------------------------------------------------------------------------------------------------------------------------------#
# def get_sales_data():

    # read the stores sitemap to find the products in the store
    

# MAIN EXECUTION 
def main():

    # Step 1 - get_facebook_ads() with an open search query -> (" ")
    print("\n-------------------->STEP 1: Scrape Ads Library for X#<--------------------")
    get_facebook_ads()

    # Step 2 - check if each index from set of collected urls, is_shopify_store(test_url)
    # test_set = set()
    # test_set = ("misvale.com", "validatorai.com", "youtube.com", "www.italojewelry.com/italo-purple-love-design-titanium-steel-couple-rings-251001.html")
    print("\n-------------------->STEP 2: Validate URLs via 'builtwith.com'<--------------------")
    # is_shopify_store(get_facebook_ads())
    
    # Step 3 - peform main step of collecting sales data from store sitemap etc.
    print("\n-------------------->STEP 3: Retrieve Sales Data & Rank by 'Top Hourly Sales<--------------------")
    # get_sales_data()

if __name__ == "__main__":
    main()