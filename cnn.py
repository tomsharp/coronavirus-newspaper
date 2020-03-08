import newspaper
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import sqlite3
import pandas as pd
import time
from datetime import datetime

from util import update_articles_table

def scrape_cnn_links(driver):
    els = driver.find_elements_by_class_name('cnn-search__results-list')
    links = []
    for article in els[0].find_elements_by_class_name('cnn-search__result--article'):
        link = article.find_elements_by_class_name('cnn-search__result-contents')[0].\
                find_elements_by_class_name('cnn-search__result-headline')[0].\
                find_elements_by_tag_name('a')[0].get_attribute('href')

        links.append(link)
    return links


if __name__ == '__main__':
    driver = webdriver.Firefox()

    for i in range(0, 15):
        print(i)
        
        if i == 0:
            url = "https://www.cnn.com/search?size=100&q=coronavirus&sort=newest"
        else:
            url = "https://www.cnn.com/search?size=100&q=coronavirus&sort=newest&from={}&page={}".format(100*i, i+1)
        
        driver.get(url)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print('sleeping... {}'.format(current_time))
        time.sleep(60)
        
        links = scrape_cnn_links(driver)
        bad_links = update_articles_table(links, 'cnn')
        if len(bad_links) == len(links):
            break