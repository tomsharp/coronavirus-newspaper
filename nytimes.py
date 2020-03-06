import newspaper
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import sqlite3
import pandas as pd
import time
from datetime import datetime

def update_articles_table(links, site):
    bad_links = []
    with sqlite3.connect('data/newspaper.db') as conn:
        c = conn.cursor()
        for link in links:
            c.execute("""SELECT link
                        FROM articles
                        WHERE link="{}"
                        """.format(link))
            
            result = c.fetchone()
            if result:
                print("link already exists: {}".format(link))
                bad_links.append(link)
            else:
                c.execute("INSERT INTO articles VALUES (?, ?)", (site, link))
                conn.commit()
        return bad_links 

def scrape_nytimes_links(end_date, start_date, driver):
    url = 'https://www.nytimes.com/search?dropmab=false&endDate={}&query=coronavirus&sort=newest&startDate={}&types=article'.format(end_date, start_date)
    driver.get(url)

    # calculate n_clicks required
    p = driver.find_element_by_tag_name('p')
    n_articles = int(p.text.split('Showing ')[1].split(' results for')[0])
    n_clicks = (n_articles-1)//10
    print("click required:", n_clicks)
    
    
    global_links = []
    for i in range(n_clicks+1):
    
        print("Click # {} of {}".format(i,n_clicks))

        # find list tags, grab links 
        els = driver.find_elements_by_tag_name('li')
        links = []
        for el in els:
            try:
                a = el.find_element_by_tag_name('a')
                href = a.get_attribute('href')
            except:
                print("bad element, no <a> tag:", el)
            link = href.split('?searchResultPosition')[0]
            links.append(link)

        # cut off links in footer of page
        cut_index = [i for i, link in enumerate(links) if link == 'https://www.nytimes.com/'][0]
        links = links[:cut_index]

        # filter out links already in global_links
        links = [l for l in links if l not in global_links]
        global_links.extend(links)

        # update db
        update_articles_table(links, 'nytimes')

        # find and click 'show more' button
        buttons = driver.find_elements_by_tag_name('button')
        button = [b for b in buttons if b.text=='SHOW MORE'][0]
        button.click()

        # sleep 
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print('sleeping... {}'.format(current_time))
        time.sleep(60)

if __name__ == '__main__':
    scrape_nytimes_links(start_date=20200306, 
                         end_date=20200306, 
                         driver=webdriver.Firefox())