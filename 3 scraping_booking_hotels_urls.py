from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager 
import pandas as pd
import os
import logging
import scrapy
from scrapy.crawler import CrawlerProcess 

cities_list = [
            "Mont Saint Michel",
            "St Malo",
            "Bayeux",
            "Le Havre",
            "Rouen",
            "Paris",
            "Amiens",
            "Lille",
            "Strasbourg",
            "Chateau du Haut Koenigsbourg",
            "Colmar",
            "Eguisheim",
            "Besancon",
            "Dijon",
            "Annecy",
            "Grenoble",
            "Lyon",
            "Gorges du Verdon",
            "Bormes les Mimosas",
            "Cassis",
            "Marseille",
            "Aix en Provence",
            "Avignon",
            "Uzes",
            "Nimes",
            "Aigues Mortes",
            "Saintes Maries de la mer",
            "Collioure",
            "Carcassonne",
            "Ariege",
            "Toulouse",
            "Montauban",
            "Biarritz",
            "Bayonne",
            "La Rochelle"
            ]

#Define the spider
class booking_spider(scrapy.Spider): 
    # Name of the spider 
    name = "booking_hotels_urls" 

    # Url to start the spider from 
    start_urls = ['https://www.booking.com/index.fr.html'] 

    # Parse function for form request 
    def parse(self, response): 
        # FormRequest used to make a search of cities 
        
        for city in cities_list: 
            yield scrapy.FormRequest.from_response(
            response,
            formdata={'ss': city}, 
            formid = "city_searched",
            callback=self.after_search,
            cb_kwargs = dict(city_name = city)  
        )
    

    # Callback used after city search
    def after_search(self, response, city_name): 

        # Create the instance of Chrome WebDriver 
        driver = webdriver.Chrome()  
        driver.get(response.request.url)
        driver.implicitly_wait(0.5)
        
        # extraction of the urls of all the hotels
        urls_all_hotels = driver.find_element(By.XPATH, '//*[@id="search_results_table"]/div[2]/div/div/div[3]/div[45]/div[1]/div[2]/div/div[1]/div/div[1]/div/div[1]/div/h3/a')

        # scrape data from each hotel page
        for url in urls_all_hotels:
            yield {
                 'city' : city_name, 
                 'url' : url.get_attribute('href') 
            }


# Name of the file where the results will be saved
filename = "booking_hotel_urls.json"

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
process.crawl(booking_spider)  
process.start()
