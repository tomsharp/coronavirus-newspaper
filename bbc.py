import newspaper
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import sqlite3
import pandas as pd
import time
from datetime import datetime

from util import update_articles_table


def scrape_bbc_links(driver):
    url = 'https://www.bbc.co.uk/search?q=coronavirus'
    driver.get(url)
    
    global_links = ['https://www.bbc.co.uk', 'https://www.bbc.co.uk/',
                    'https://www.bbc.co.uk/usingthebbc/terms/', 'https://www.bbc.co.uk/aboutthebbc', 
                    'https://www.bbc.co.uk/usingthebbc/privacy/', 'https://www.bbc.co.uk/usingthebbc/cookies/', 
                    'https://www.bbc.co.uk/accessibility/', 'https://www.bbc.co.uk/guidance', 
                    'https://www.bbc.co.uk/contact', 'https://www.bbc.co.uk/bbcnewsletter',
                    'https://www.bbc.co.uk/search?q=coronavirus#search-content', 'https://www.bbc.co.uk/accessibility/',
                    'https://www.bbc.co.uk/search?q=coronavirus#orb-footer', 'https://www.bbc.co.uk/search?q=coronavirus&suggid=',
                    "https://www.bbc.co.uk/search?q=coronavirus#search-content",
                    "https://www.bbc.co.uk/search?q=coronavirus&filter=iwonder&suggid=",
                    "https://www.bbc.co.uk/search?q=coronavirus&filter=learning_english&suggid=",
                    "https://www.bbc.co.uk/search?q=coronavirus&filter=news&suggid=",
                    "https://www.bbc.co.uk/search?q=coronavirus&filter=newsround&suggid=",
                    "https://www.bbc.co.uk/search?q=coronavirus&filter=programmes&suggid=",
                    "https://www.bbc.co.uk/search?q=coronavirus&filter=sport&suggid=",
                    "https://www.bbc.co.uk/sounds",
                    "https://www.bbc.com/",
                    "https://www.bbc.com/culture",
                    "https://www.bbc.com/culture/music",
                    "https://www.bbc.com/future",
                    "https://www.bbc.com/news",
                    "https://www.bbc.com/reel",
                    "https://www.bbc.com/sport",
                    "https://www.bbc.com/travel",
                    "https://www.bbc.com/usingthebbc/cookies/how-can-i-change-my-bbc-cookie-settings/",
                    "https://www.bbc.com/weather",
                    "https://www.bbc.com/worklife",
                    "https://advertising.bbcworldwide.com/",
                ]

    new_links = ['init']
    while len(new_links)!=0:
    
        # find list tags, grab links 
        els = driver.find_elements_by_tag_name('li')
        links = []
        for el in els:
            try:
                a = el.find_element_by_tag_name('a')
                href = a.get_attribute('href')
            except:
                print("bad element, no <a> tag:", el)
            links.append(href)

        # cut off links in footer of page
        links = list(set(links))

        # filter out links already in global_links
        new_links = [l for l in links if l not in global_links]
        global_links.extend(new_links)

        # update db
        update_articles_table(new_links, 'bbc')

        # find and click 'show more' button
        navs = driver.find_elements_by_tag_name('nav')
        button = [n for n in navs if n.text=='Show more results'][0]
        button.click()

        # sleep 
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print('sleeping... {}'.format(current_time))
        time.sleep(60)

if __name__ == '__main__':
    scrape_bbc_links(driver=webdriver.Firefox())