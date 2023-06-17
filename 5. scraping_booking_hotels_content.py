from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager 
import pandas as pd
import os
import logging
import json 
import scrapy
from scrapy.crawler import CrawlerProcess 

file = open("Booking\scraping_booking_hotels_urls.json")
file = json.load(file)
list_urls = [line['url'] for line in file]

#Define the spider
class booking_spider_content(scrapy.Spider): 
    # Name of the spider 
    name = "booking_hotels_content" 

    # Url to start the spider from 
    start_urls = list_urls

    # Parse function for scraping content 
    def parse(self, response): 

        # Create the instance of Chrome WebDriver 
        driver = webdriver.Chrome()  
        driver.get(response.request.url)
        driver.implicitly_wait(0.5)
        
        # scrape content of each hotel url
        hotel_name = driver.find_element(By.XPATH, '//*[@id="hp_hotel_name"]/div/h2').text 
        rating = driver.find_element(By.XPATH, '//*[@id="js--hp-gallery-scorecard"]/a/div/div/div/div[1]').text 
        coordinates = driver.find_element(By.ID, 'hotel_address').get_attribute('data-atlas-latlng')
        descriptions = driver.find_element(By.XPATH, '//*[@id="property_description_content"]/p')
        description = [paragraph.text for paragraph in descriptions]
        address = driver.find_element(By.XPATH, '//*[@id="showMap2"]/span[1]').text 
        city = driver.find_element(By.ID, ":Rp5:").get_attribute("value") 

        return { 
            'city_name': city,
            'hotel_name': hotel_name,
            'hotel_url': response.request.url,
            'hotel_address': address,
            'hotel_latitude': coordinates.split(",")[0],
            'hotel_longitude': coordinates.split(",")[1],
            'hotel_score': rating,
            'hotel_description': description
        }
  
# Name of the file where the results will be saved
filename = "booking_hotel_content.json"

# If file already exists, delete it before crawling (because Scrapy will 
# concatenate the last and new results otherwise)
if filename in os.listdir('Booking/'):
        os.remove('Booking/' + filename)

# Declare a new CrawlerProcess with some settings
process = CrawlerProcess(settings = {
    'USER_AGENT': 'Chrome/114.0',                   
    'LOG_LEVEL': logging.INFO,
    "FEEDS": {
        'Booking/' + filename : {"format": "json"},
    }
})

# Start the crawling using the spider defined above
process.crawl(booking_spider_content)  
process.start()
