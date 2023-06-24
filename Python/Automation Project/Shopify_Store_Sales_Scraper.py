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

# A function to utilize Selenium to crawl the Meta Ads Library and grab needed ads links 
def get_facebook_ads():

    past_date = (datetime.now() - timedelta(days=3)).strftime("%m/%d/%Y")
    meta_cta_buttons = ['Get Offer', 'Get offer', 'Open Link', 'Open link', 'Order Now', 'Order now', 'Save', 'Shop Now', 'Shop now', 'Subscribe', 'Contact Us', 'Contact us', 'Download']
    unique_store_urls = set()

    try:
        # Initialize the browser and navigate to the page
        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        browser.get("https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=ALL&q=%22%20%22&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped&search_type=keyword_exact_phrase&media_type=all")
        # (In working order): Look for keyword, make it clickable, clear existing data in box, enter new info, keep page open for 10 seconds
        search_box = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search by keyword or advertiser']")))
        search_box.click()
        search_box.clear()
        # search_box.send_keys("" "" + Keys.ENTER)
        search_box.send_keys("gift" + Keys.ENTER)
        time.sleep(5)
        
        # filters_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[5]/div[2]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]")))
        # filters_button.click()
        # time.sleep(3)
        
        # # [Popup] Activating the filters (English, active ads, date from (last 2 days) to today)
        # filters_language_dropdown = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[text()='All languages']")))
        # filters_language_dropdown.click()
        # time.sleep(2)
        # filters_language_selector_en = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[text()='English']")))
        # filters_language_selector_en.click()
        # time.sleep(2)
        # ## click out of dropdown selector
        # click_out = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@role='combobox']//div//div//div//div//div//div//div[contains(text(),'English')]")))
        # click_out.click()
        # time.sleep(2)
        # filters_active_status = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Active and inactive']")))
        # filters_active_status.click()
        # time.sleep(2)
        # filters_active_selector = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Active ads']")))
        # filters_active_selector.click()
        # time.sleep(2)
        # # scroll into view of date element
        # pg_down = browser.find_element(By.XPATH, "//input[@placeholder='mm/dd/yyyy']")
        # pg_down.location_once_scrolled_into_view
        # filters_from_date = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='mm/dd/yyyy']")))
        # filters_from_date.click()
        # filters_from_date.send_keys(Keys.CONTROL, "a")
        # filters_from_date.send_keys(Keys.BACK_SPACE)
        # filters_from_date.send_keys(past_date)
        # time.sleep(2)
        # ## apply all filters
        # filters_apply = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//body[1]/div[5]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[3]/div[1]/div[2]/div[1]")))
        # filters_apply.click()
        # time.sleep(5)

        # Now we must go through each ad tablet and output `unique` CTA urls
        current_element = browser.find_element(By.XPATH, "//body/div/div/div[@role='main']/div/div/div/div/div/div/div[4]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]")
        current_element.click()
        current_element.click()
        
        # it will end anyways, so regularly scroll until, check for footer element to see if tab has hit the end
        # if i do want it to break, i can keep a counter to stop at for example 1000 ads
        # slow down run time, to let page load with inifinite scroll as pect when it tabs to last ad

        # ads library loads 30 ads each load time (end of page)
        # starts with 30 ads only
        # check for spinner/loader animation, when iterated through 30 ads

        # FIND OUT WHEN IT TRIGGERS THE 'LOAD MORE' functionality of the infinite scroll, then you can check for end of page etc.

        # actual tabbing process, with a starting point and the next element being reassigned to the initial, to tab to
        ads_traversed = 0
        new_ad = 0
        last_traversed_ad = None

        while(True):
            
            if not current_element.get_attribute('aria-controls'):
                print("traversing...")
            elif current_element.get_attribute('aria-controls').startswith("js_"):
                print("\nNew ad - Traversing...")
                new_ad += 1

            current_element.send_keys(Keys.TAB)
            WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//body/div/div/div[@role='main']/div/div/div/div/div/div/div[4]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]")))
            current_element = browser.switch_to.active_element

            # check for a set of keywords when a CTA button is targeted, if matched then extract URL from source    
            if current_element.get_attribute('role') == "button" and current_element.get_attribute('aria-busy') == "false" and current_element.get_attribute('tabindex') == '0':
                button_text = current_element.text
                if button_text in meta_cta_buttons:
                    ads_traversed += 1
                    print("Ad traversed! Going next...\n")
                    parent_element = current_element.find_element(By.XPATH, "..")
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
                
            # should ideally break when it hits the first element in the footer (because ofcourse no further data was loaded in time or exists)
            elif current_element.get_attribute('text') == "Ad Library API":
                print("footer hit - returning to last ad and waiting for potential data to load")
                WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//body/div/div/div[@role='main']/div/div/div/div/div/div/div[4]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]")))
                print("footer hit - abort script!")
                break
            else:
                continue
            
            # try:
            #     # to look for the loading page data as part of infinite scroll
            #     # spinner_element = WebDriverWait(browser, 3).until(EC.visibility_of_element_located((By.XPATH, "//span[@role='progressbar']//*[name()='svg']")))
            #     spinner_element = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, "//*[local-name()='svg' and @role='progressbar']")))
            #     # end_of_page_element = browser.find_element(By.XPATH, "//a[contains(text(),'Ad Library API')]")
            #     print("")
            #     if spinner_element:
            #         print("Spinner exists -> waiting for data load")
            #         time.sleep(5)
            #     print("")
            # except TimeoutException:
            #     print("")
            #     print("Spinner doesn't exist -> resuming scroll\n")
            
            # check for at least 3 ads having been skipped, so that it can sleep to load more
            if new_ad - ads_traversed == 3:
                print("\n----------Stopping for data to load----------")
                time.sleep(5)
            else:
                continue 

            # Since the main issue im trying to avoid is, waiting for data to load when its scrolled all the way down the page, without it leaving the scroll/loop since it hits the footer. 
            # Instead of worrying about checking for skipped ads, or keeping counters or w.e. Why can't I just jump back to the last AD it was on before it hit the footer? Putting a sleep for 5 seconds so the auto-load takes place succesfully and it can resume tabbing from that element. The issue here is finding the unique identifier of that AD for the script to identify and select. 



        # prints numbered list of urls
        print("\n")
        for index, value in enumerate(unique_store_urls, start=1):
            print(f"{index}. {value}")            
    except Exception as e:
        print(e)
        browser.quit() 
        return unique_store_urls

# Automating control of the website 'builtwith.com', to determine if given url is shopfiy store and add them to a verified set
def is_shopify_store(test_set):
    
    # Initialize the browser and navigate to the page
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    validated_shopify_stores = set()
    # not useful for this script, but for general data
    non_shopify_stores = set()
    non_ecommerce = set()

    # loop given set of urls and check for Shopify platformness
    for i in test_set:

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
    
    percent_vss = (len(validated_shopify_stores) / len(test_set)) * 100
    percent_nss = (len(non_shopify_stores) / len(test_set)) * 100
    percent_ne = (len(non_ecommerce) / len(test_set)) * 100

    print("\nFrom the extracted Meta Library of '", len(test_set), "' total ads:\n->", percent_vss, "%", " are SHOPIFY stores [", len(validated_shopify_stores), "site(s)]\n->", percent_nss, "%" ," are NON-SHOPIFY ecommerce [", len(non_shopify_stores), "site(s)]\n->", percent_ne, "%", " are NON-ECOMMERCE based [", len(non_ecommerce), "site(s)]\n")

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
# In this JSON there is a field "updated_at". This field is updated every time a change is made. Also, when an order take place (the stock is changed).
# And with this, it is possible to track the sales (approximately).
#------------------------------------------------------------------------------------------------------------------------------#
# def get_sales_data():

    # read the stores sitemap to find the products in the store
    

# MAIN EXECUTION 
def main():

    # Step 1 - get_facebook_ads() with an open search query -> (" ")
    get_facebook_ads()

    # Step 2 - check if each index from set of collected urls, is_shopify_store(test_url)
    # test_set = set()
    # test_set = ("misvale.com", "validatorai.com", "youtube.com", "www.italojewelry.com/italo-purple-love-design-titanium-steel-couple-rings-251001.html")
    # is_shopify_store(test_set)
    
    # Step 3 - peform main step of collecting sales data from store sitemap etc.
    # get_sales_data()

if __name__ == "__main__":
    main()