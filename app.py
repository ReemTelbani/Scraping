'''======== IMPORTING PACKAGES =============================================================''' 
import os
import warnings
warnings.filterwarnings('ignore')
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_mail import Mail, Message
import smtplib
import json
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
#imports
import warnings
warnings.filterwarnings('ignore')
from datetime import datetime
import requests, uuid, json
from flask import Flask , jsonify, request
import time 
import os
import random
import re
from selenium import webdriver
from pymongo import MongoClient

from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


'''======== IMPORTING PACKAGES =============================================================''' 
import os
import warnings
warnings.filterwarnings('ignore')
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_mail import Mail, Message
import smtplib
import json
import re
from datetime import datetime
import numpy as np
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart





# Load environment variables from .env file
env_file = ".env"
load_dotenv(dotenv_path=env_file)


app = Flask(__name__)


def random_delay(min_sec=1, max_sec=5):
    time.sleep(random.uniform(min_sec, max_sec))

def simulate_typing(element, text):
    for char in text:
        element.send_keys(char)
        random_delay(0.1, 0.3)  # Simulate typing speed



def smooth_scroll(driver, min_h=500, max_h=800):
    height = random.uniform(min_h, max_h)
    """Smoothly scroll down the page by the specified height."""
    current_height = driver.execute_script("return window.pageYOffset;")
    target_height = current_height + height
    while current_height < target_height:
        driver.execute_script("window.scrollTo(0, arguments[0]);", current_height)
        current_height += 1  # Adjust this value for faster/slower scrolling
        time.sleep(0.01)  # Adjust delay for smoother scrolling
        
def mimic_human(driver):
    smooth_scroll(driver, 500,800)
    random_delay()


def save_to_mongo(data, db_name, collection_name):
    # Step 1: Create a MongoDB client
    client = MongoClient('mongodb://localhost:27017/')  # Adjust the URI as needed

    # Step 2: Access the database
    db = client[db_name]

    # Step 3: Access the collection
    collection = db[collection_name]

    # Step 4: Insert the dictionary into the collection
    result = collection.insert_one(data)

    # Print the inserted ID
    #print(f'Document inserted with ID: {result.inserted_id}')

'''
def retrieve_from_mongo(db_name, collection_name, query=None):
    # Step 1: Create a MongoDB client
    client = MongoClient('mongodb://localhost:27017/')  # Adjust as needed

    # Step 2: Access the database
    db = client[db_name]

    # Step 3: Access the collection
    collection = db[collection_name]

    # Step 4: Query the collection
    if query is None:
        # Retrieve all documents if no query is provided
        results = collection.find()
    else:
        # Retrieve documents that match the query
        results = collection.find(query)

    # Step 5: Process and print the results
    #for document in results:
    #    print(document)
'''

def retrieve_from_mongo(db_name, collection_name, query):
    # Step 1: Create a MongoDB client
    client = MongoClient('mongodb://localhost:27017/')  # Adjust as needed

    # Step 2: Access the database
    db = client[db_name]

    # Step 3: Access the collection
    collection = db[collection_name]

    # Step 4: Query the collection
    if query is None:
        # Retrieve all documents if no query is provided
        results = ""
        status = False
    else:
        # Step 5: Retrieve and sort the documents by price in descending order
        results = collection.find(query).sort("price", -1)
        status=True

    # Step 6: Process and return the results
    return status, list(results)



def categorize_listing(text):
    # Split the listing into lines
    lines = text.splitlines()

    # Initialize variables
    extra_info = None
    price = None
    description = None
    ad_creation_time = None


    # Check if the first line contains "مميز"
    if "مميز" in lines[0]:
        extra_info = lines[0].strip()  # First line as extra info

    # Check for price in the relevant lines
    if "ج.م" in lines[1]:
        price = lines[1].strip()
    elif "ج.م" in lines[0]:
        price = lines[0].strip()
    else:
        price = None

    if "منذ" in lines[2]:
        temp_list= lines[2].strip().split('منذ')
        ad_creation_time = temp_list[1]
        place= temp_list[0]
        
    elif "منذ" in lines[3]:
        temp_list = lines[3].strip().split('منذ')
        ad_creation_time = temp_list[1]
        place= temp_list[0]
        
    elif "منذ" in lines[4]:
        temp_list = lines[4].strip().split('منذ')
        ad_creation_time = temp_list[1]
        place= temp_list[0]
        
    else:
        ad_creation_time = None
        place = None

    # Combine remaining lines for description
    description = " ".join(lines[1:])  # Combine to form the description

    # Create a dictionary for the current listing
    categorized_listing = {
        'price': price,
        'ad_creation_time_since': ad_creation_time,
        'description': description,
        'place':place,
        'special_ad': extra_info,
        
    }
    return categorized_listing


def extract_number(text):
    # Use regular expressions to find all digits in the text
    match = re.search(r'\d+', text)
    if match:
        # Convert the found digits to an integer
        return int(match.group(0))
    else:
        # Return None if no digits are found
        return 0

       

def categorize_listing(text):
    # Split the listing into lines
    lines = text.splitlines()

    # Initialize variables
    extra_info = None
    price = None
    description = None
    ad_creation_time = None
    place = None
    
    # Check for the word "منذ" in each line
    for line in lines:
        if "منذ" in line:
            # Print the line for debugging
            #print(f"The word 'منذ' is in line: {line}")
            temp_list = line.strip().split('منذ')
            if len(temp_list) > 1:
                place = temp_list[0].strip()
                ad_creation_time = temp_list[1].strip()
        
        if "ج.م" in line:
            # Print the line for debugging
            price = line.strip()

        if "مميز" in line:
            # Print the line for debugging
            extra_info = line.strip()

    # Combine remaining lines for description, except the first line
    description = " ".join(lines[1:])

    # Create a dictionary for the current listing
    categorized_listing = {
        'price': price,
        'ad_creation_time_since': ad_creation_time,
        'description': description,
        'place': place,
        'special_ad': extra_info,
    }
    
    return categorized_listing






def old_scrape_page(driver, ad_links, page_number, search_keyword):
    links = []
    for link in ad_links:
        href = link.get_attribute('href')
        if href not in links:
            links.append(href)
    #for i in links:
    #    print(i)
    print("len(links) ",len(links))
    
    # Find all elements that match the CSS selector 
    list_ele = driver.find_elements(By.CSS_SELECTOR, "[aria-label='Listing']") 

    # Loop over the elements and print their text 
    c=0
    ads_list = []
    for element in list_ele: 
        #print(element.text)
        #print("")
        text = element.text
        result = categorize_listing(text)
        result['ad_link'] = links[c]
        result['insertion_date'] = datetime.today().strftime('%Y-%m-%d')
        result['page_number']=page_number
        result['search_keyword']=search_keyword
        result['links_count_in_page']= len(ad_links)
        ads_list.append(result)
        #ads_dic[c]=text
        # Save the data to MongoDB
        save_to_mongo(result, 'olx_ads', 'ads_temp')
        c=c+1
    #print("ads_dic.keys ",len(ads_dic.keys()))
    #print(ads_dic) 
    print("Number of returned ads from page number: ",str(page_number), " is ",str(len(ads_list)))
    
    return True, ads_list
    



def scrape_page_flow(driver, page_number, search_keyword):
    # Check if the ChromeDriver is initialized
    if driver is not None:
        ad_links = driver.find_elements(By.CSS_SELECTOR, 'a[href^="/ad/"]')
        #print(f"Number of matching links: {len(set(ad_links))}")
        mimic_human(driver)
    
        print("3- scarping_ads_links start TODO")
        page_scrapping_status, ads_list = old_scrape_page(driver, ad_links, page_number, search_keyword)
        print("3- scarping_ads_links done TODO")
    
        if page_scrapping_status:
            counted_items= len(ads_list)
        else:
            counted_items=0
        print("ChromeDriver is initialized and ready to use.")
    else:
        page_scrapping_status=False
        counted_items=0
        print("ChromeDriver failed to initialize.")
        
    return  page_scrapping_status, counted_items, ads_list


def navigate_to_the_next_page(driver, page_number):
        try:
            print(" 4- navigate_to_the_next_page start")
            print("navigate to page number:---->", page_number)
            
        
            # Locate the <div> with role="navigation"
            navigation_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@role="navigation"]'))
            )
        
            mimic_human(driver)
        
            last_li = navigation_element.find_element(By.XPATH, './ul/li[last()]')
            last_a = last_li.find_element(By.TAG_NAME, 'a')
            href_value = last_a.get_attribute('href')
            print("Extracted href:", href_value)
            
            href_value_new = href_value.split('page=')[0]+"=page="+str(page_number)
            print("href_value_new :", href_value_new)
            
            #href_value = "/ads/q-"+query+"/?page="+str(page_number)
            #next_point = "https://www.dubizzle.com.eg/ads/q-"+query+"/?page="+str(page_number)
            #print(next_point)
            
            # add the page count to the page number iteratively
            #driver.get(next_point)
            
            
    
            #print(href_value)
            #print("search for href")
    
            driver.execute_script("window.open(arguments[0], '_self');", href_value)
            time.sleep(20)
            print(driver.title)

            if (driver.title!='خطأ داخلي | دوبيزل مصر (أوليكس)'):
                print("4- navigate_to_the_next_page done ")
                print("")
                return True
            else:
                print("4- navigate to the next page failed")
                print("")
                return False
                

        except:
            return False
            print("4- navigate to the next page failed")
            print("")

def main_page_flow(driver, query):
    print("1-search_with_keyword.... ")
    search = driver.find_element(By.XPATH, '//*[@id="body-wrapper"]/div[1]/header/div[2]/div[2]/div/div/div/div/div[1]/input')
    #search= driver.find_element(By.CSS_SELECTOR, "input[type='search'][autocomplete='free-text-search']")
    mimic_human(driver)
    
    print("searching with:", query)
    simulate_typing(search, query)
    
    search.send_keys(Keys.RETURN)
    print("1-search_with_keyword done....")
    print("")
    random_delay()

    print("2-scarping_ads_count... ")
    # Collect ads count
    ads_count_element = driver.find_elements(By.XPATH, '//*[@id="body-wrapper"]/div[2]/header[2]/div/div/div/div[2]/div[1]/div[2]/div/div')
    if ads_count_element:
        ads_count = int(re.sub(r'[^a-zA-Z0-9]', '', ads_count_element[0].text))
    else:
        ads_count=0
    print("Ads Count:", ads_count)
    print("2-scarping_ads_count done...")
    print("")
    return driver, ads_count

def SCRAPER(keyword, requested_returned_ads_count):
       
        # Set up Chrome options
        options = Options()
        #ua = UserAgent()
        #options.add_argument(f'user-agent={ua.random}')
        #options.add_argument("--incognito")
        #options.add_argument("--headless")  # Run in headless mode
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")  # Help prevent detection ,  adding argument to disable the AutomationControlled flag 
        options.add_experimental_option("excludeSwitches", ["enable-automation"]) # exclude the collection of enable-automation switches 
        options.add_experimental_option("useAutomationExtension", False)  # turn-off userAutomationExtension 
        options.add_argument("window-size=1920,1080")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--ignore-certificate-errors")
    
        # List of proxy servers
        proxies = [
            'http://184.82.55.109:8080',
            'http://188.166.229.121:80',
            'http://49.49.60.99:8080'
        ]
        # Function to get a random proxy
        def get_random_proxy():
            return random.choice(proxies)
    
        status = False
        query = keyword
        
    # Loop through proxies
   # for _ in range(5):  # Adjust the number of attempts as needed
        
        #proxy = get_random_proxy()
        #options.add_argument(f'--proxy-server={proxy}')

        end_point ="https://www.dubizzle.com.eg/"

        # Initialize the Chrome driver
        driver = webdriver.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") # changing the property of the navigator value for webdriver to undefined
        
        driver.get(end_point)
        print(driver.title)
        
        random_delay()
        
        
    
        try:
            retrived_items_counter = 0
            all_ads_fetched = []
            driver, ads_count = main_page_flow(driver, query)
    
            target_number_of_ads =0
    
            # 2<150

            
            if (requested_returned_ads_count<=ads_count) :
                print("requested ads is suitable...")
                target_number_of_ads= requested_returned_ads_count
                retriving_count_message="we will retrive for you "
    
            else:
                print("requested ads is Not suitable...")
                #print("requested ads more than the existing ads in the website, retrive all the ads found as much as the scraper can get...")
                target_number_of_ads=ads_count
                retriving_count_message= '''you requested ads more than the avilable ads exist on OLX, 
                                            try generalize your search keyword....'''

            print("********************************************")
            print("requested_returned_ads_count: ",requested_returned_ads_count)
            print("ads_count: ",ads_count)
            print("target_number_of_ads: ",target_number_of_ads)
            print("********************************************")
    
            #scrape 1st page:
            page_scrape_status, retrived_ads_count_from_page_1, ads_list = scrape_page_flow(driver, 1, keyword)
            all_ads_fetched.append(ads_list)
            
            retrived_items_counter = retrived_items_counter + retrived_ads_count_from_page_1
            print("retrived_items_counter: ", retrived_items_counter)
            
            if target_number_of_ads< retrived_ads_count_from_page_1: # no need to navigate to page 2, 3 , 4, scrape only page 1
                print("retrive from page 1 only.")
                retriving_count_message = retriving_count_message + str(target_number_of_ads) +" ads."
                return True
    
            else:
                print("retrive from other pages.")
                #print("the targeted number of ads is more than the retrived_ads_count from page 1, you have to navigate to page 2, 3, 4...")
                pages_counter=1
                number_to_return = 0
                
                while True:
                    pages_counter = pages_counter+1
                    #80<100 , 110>100
                    if (retrived_items_counter< target_number_of_ads):
                        
                        print("scrapy didnt reach to the target_number_of_ads, loop till reach the target number...")
                        navigate_to_the_next_page_status = navigate_to_the_next_page(driver , pages_counter)
                        
                        if navigate_to_the_next_page_status:
                            time.sleep(20)
                            page_scrape_status, retrived_ads_count, ads_list  = scrape_page_flow(driver, pages_counter, keyword)
                            all_ads_fetched.append(ads_list)
                            
                            
                            if page_scrape_status:
                                retrived_items_counter = retrived_items_counter + retrived_ads_count
                                print("retrived_items_counter: ", retrived_items_counter)
                                number_to_return = retrived_items_counter
                                print("crapping other pages in progress")
                                continue
                                
                            else:
                                number_to_return = retrived_items_counter
                                print("error could be happen while scrapping other pages")
                                break
    
                                
                        else:
                            number_to_return = retrived_items_counter
                            print("error could be happen while navigating to other pages")
                            break

                        print("number_to_return: ", number_to_return)
                            
                        
                       # continue
    
                    else:
                        print("scrapy reached to the target_number_of_ads, remove extra retrived items...")
                        number_to_return = target_number_of_ads
                        #ads_list = ads_list[:target_number_of_ads])
                        break

                    
            print("type all_ads_fetched: ", type(all_ads_fetched))
            print("all_ads_fetched: ", len(all_ads_fetched))
            all_ads_fetched = [item for sublist in all_ads_fetched for item in sublist]
            print("all_ads_fetched: ", len(all_ads_fetched))
            all_ads_fetched = all_ads_fetched[:number_to_return+1]
            print("all_ads_fetched: ", len(all_ads_fetched))
            #print("all_ads_fetched", all_ads_fetched)
    
            '''
            while (retrived_items_counter< requested_returned_ads_count):
                if main_page_flag==0:
    
                    # Check if the ChromeDriver is initialized
                    if driver is not None:
                        print("ChromeDriver is initialized and ready to use.")
                        page_scrape_status, counted_items = scrape_page_flow(driver, 1)
                        retrived_items_counter = retrived_items_counter+counted_items
                        main_page_flag=1
                        continue
                    else:
                        print("ChromeDriver failed to initialize.")
                        break
                    
                    
    
                else:
                    navigate_to_the_next_page_status = navigate_to_the_next_page(driver , 2)
                    if navigate_to_the_next_page_status:
                        time.sleep(20)
                        scrap_second_page_status, counted_items  = scrape_page_flow(driver, 2)
                        
                        if scrap_second_page_status:
                            return True
                        else:
                            return False
                    else:
                        return False
            '''
            status = True
    
        except Exception as e:
            
            print("An error occurred:", e)
            status = False
            all_ads_fetched=[]
            
        finally:
            print("print i quit")
            driver.quit()
            
    
        return status, all_ads_fetched



def SEND_SAMPLE_TO_EMAIL(sender_email, sender_password, recipient_email, subject, body):
    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach the email body
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Set up the server
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Gmail SMTP server
        server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
        
        # Log in to your account
        server.login(sender_email, sender_password)  # Use your App Password here

        # Send the email
        server.send_message(msg)
        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email: {e}")

    finally:
        server.quit()  # Close the connection


def keyword_preprocessing(search_keyword):
    if search_keyword is None or search_keyword == "null" or (isinstance(search_keyword, float) and np.isnan(search_keyword)):
        search_keyword=""

    modified=False
    
    # Remove special characters 
    cleaned_search_keyword = re.sub(r'[^A-Za-zء-ي0-9\s]', '', search_keyword) # Remove extra spaces 
    cleaned_search_keyword = re.sub(r'\s+', ' ', cleaned_search_keyword).strip()
    if (cleaned_search_keyword!=search_keyword):
        modified=True
    
    #if (cleaned_search_keyword!="") | (cleaned_search_keyword!=None) | (cleaned_search_keyword!=np.nan):
    # Check if the variable is not an empty string, None, or NaN
    if (cleaned_search_keyword != ""):
        status = True
    else:
        status = False

    return status, modified, cleaned_search_keyword


def check_email_is_valid(email):
    modified=False
    # Define the regular expression for a valid email address
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    # Check if the email matches the regular expression
    status = re.match(email_regex, email) is not None
    return status, modified, email


def check_sample_size_valid(sample_size):
    modified=False
    if sample_size < 20:
        status =False
        updated_sample_size = 20
    else:
        status =True
        updated_sample_size = sample_size

    if (updated_sample_size!=sample_size):
        modified=True

    return status, modified, updated_sample_size

def PROCESS_REQUEST(request_components):

    try:
        preprocessing_status, search_keyword_modification_flag     , search_keyword = keyword_preprocessing(request_components['search_keyword'])
        
        reciver_email_status, reciver_email_modification_flag      , reciver_email          = check_email_is_valid(request_components['reciver_email'])
        
        sample_size_status  , sample_size_modification_flag        , updated_sample_size    = check_sample_size_valid(request_components['size'])

        
        # Check for valid input
        if ((not preprocessing_status) or (not reciver_email_status) or (not sample_size_status)):
            status = False

        else:
            status = True

    except:
        status = False


    return status, search_keyword, reciver_email, updated_sample_size



'''
def CHECK_KEYWORD_IN_DB_TODAY(search_keyword, sample_size):
    today = datetime.today().strftime('%Y-%m-%d')
    query = {"keyword": search_keyword, "date": today}

    #TODO
    # Check if data exists for today
    #existing_data = mongo.db.ads.find_one(search_keyword)

    existing_data = {"results": [
    {"id": 1, "name": "Product A", "price": 10.99},
    {"id": 2, "name": "Product B", "price": 5.99},
    {"id": 3, "name": "Product C", "price": 15.99},
    {"id": 4, "name": "Product D", "price": 8.49},
    {"id": 5, "name": "Product E", "price": 12.99},
    {"id": 6, "name": "Product F", "price": 7.49},
    {"id": 7, "name": "Product G", "price": 4.99},
    {"id": 8, "name": "Product H", "price": 9.99},
    {"id": 9, "name": "Product I", "price": 6.99},
    {"id": 10, "name": "Product J", "price": 14.99},
    {"id": 11, "name": "Product K", "price": 11.49},
    {"id": 12, "name": "Product L", "price": 3.99},
    {"id": 13, "name": "Product M", "price": 16.49},
    {"id": 14, "name": "Product N", "price": 2.99},
    {"id": 15, "name": "Product O", "price": 13.49},
    {"id": 16, "name": "Product P", "price": 8.99},
    {"id": 17, "name": "Product Q", "price": 5.49},
    {"id": 18, "name": "Product R", "price": 1.99},
    {"id": 19, "name": "Product S", "price": 12.49},
    {"id": 20, "name": "Product T", "price": 11.99}
    ]
                    }

    if (sample_size>len(existing_data['results'])):
        existing_data=False

    return existing_data
'''

def CHECK_KEYWORD_IN_DB_TODAY(search_keyword, sample_size):
    today = datetime.today().strftime('%Y-%m-%d')
    query = {"keyword": search_keyword, "date": today}
    
    existing_data = retrieve_from_mongo('olx_ads', 'ads_temp', query)

    if (sample_size>len(existing_data)):
        existing_data=False

    else:
        existing_data = existing_data[:sample_size]

    return existing_data

def SCRAPE_ADS(search_keyword):
    #ads_dict=
    scrape_ads_status=False
    ads_dict={}
    return scrape_ads_status, ads_dict

'''
def SCRAPER(search_keyword):
    scrape_process_status= False

    #2.1- scrape ads 
    scrape_ads_status, ads_dict = SCRAPE_ADS(search_keyword)
    if scrape_ads_status:
        print("2.1- SCRAPE_ADS Status Success...")
        
        #2.2- save output of scraper to mongodb
        save_to_db_status = SAVE_RESULT_TO_DB(ads_dict)
        if save_to_db_status:
            print("2.2- SAVE_RESULT_TO_DB Status Sucess")
            scrape_process_status= {"status":"success", "status_description": "Save Scraped data to DB process succeded."}

        else:
            print("2.2- SAVE_RESULT_TO_DB Status  Failed...")
            scrape_process_status= {"status":"error", "status_description": "Save Scraped data to DB falied due to 2- scrape_ads_status."}

    else:
        print("2.1- SCRAPE_ADS Status Failed...")
        scrape_process_status= {"status":"error", "status_description": "Scrape process falied due to 2- scrape_ads_status."}

    return Scrape_process_status
'''       
        
'''
def RETRIVE_DATA(search_keyword):

    check_result = CHECK_KEYWORD_IN_DB_TODAY(search_keyword)
    
    if check_result:
        ads = existing_data['results']
    else:
        # Scrape data
        ads = SCRAPER(keyword, max(size, 300))

    return  scrap_result
'''

def list_to_string(input_list):
    result = []

    for item in input_list:
        if isinstance(item, dict):
            # Convert dictionary to string
            dict_string = ', '.join(f"{key}: {value}" for key, value in item.items())
            result.append(f"{{ {dict_string} }}")  # Add curly braces for dictionary representation
        elif isinstance(item, str):
            result.append(item)
        else:
            result.append(str(item))  # Convert other types to string if necessary

    return ' '.join(result)  # Join all elements into a single string


def RETRIVE_DATA(search_keyword, sample_size):
    check_result = CHECK_KEYWORD_IN_DB_TODAY(search_keyword, sample_size)

    if check_result:
        ads = check_result
        status = True
    else:
        # Scrape data
        status, ads = SCRAPER(search_keyword, max(sample_size, 300))
    
    ads = ads[:max(sample_size, 300)]
    #ads = " ".join(ads)
    ads= list_to_string(ads)
    return status,  ads


def full_process(request_data):
    full_process_status= False

    #1- processing the request
    request_processing_status, search_keyword, reciver_email, sample_size = PROCESS_REQUEST(request_data)
    if request_processing_status:
        print("1-PROCESS_REQUEST Status Success...")
    
        #2- retrive data whether from the database  or scraper 
        retriving_data_status, retrived_sample_data = RETRIVE_DATA(search_keyword, sample_size)
        if retriving_data_status:
            print("2-RETRIVE_DATA Status Success...")
            full_process_status = {"status":"success", "status_description": "full process succeded."}

        else:
            print("2-RETRIVE_DATA Status Failed...")
            full_process_status= {"status":"error", "status_description": "full process falied due to 2- scraper_status."}
    else:
        retrived_sample_data=""
        print("1-PROCESS_REQUEST Status Failed...")
        full_process_status= {"status":"error", "status_description": "full process falied due to bad inputs, make sure you entered a sample more than 20 , a valid email and a valid keyword."}
        
    return full_process_status, retrived_sample_data


@app.route('/retrive_ads', methods=['POST'])
def retrive_ads():
    data = request.get_json()
    print(request)
    print("request printed")
    status, sample_str = full_process(data)
        
    sender_email = os.getenv('MAIL_USERNAME')
    sender_password = os.getenv('MAIL_PASSWORD')
    recipient_email = data['reciver_email']
    subject ="retrive sample of requested ads"
    body = sample_str

    #SEND_SAMPLE_TO_EMAIL(sender_email, sender_password, recipient_email, subject, body)
    return jsonify(status)



print(">>>>>>>>>>> APIs are up running...") 

if  __name__ == '__main__':

    print(">>>>>>>>>>> Application Works..") 
    debug = os.getenv("DEBUG")  # Access the DEBUG environment variable
    if debug:
        app.debug = True
    else:
        app.debug = False
    app.run(port=4996 ,  use_reloader=False)
