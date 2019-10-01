from __future__ import absolute_import, unicode_literals
from .celery import app

from bs4 import BeautifulSoup
from datetime import date,timedelta
import requests
from selenium import webdriver
from collections import defaultdict
import csv,time
from dataclasses import dataclass,field
import random
import pandas as pd




#@app.task
def generate_csv(data):
    df = pd.DataFrame(data)
    df.to_csv("output.csv",index=False)


hotels = defaultdict(list)

def hotel_fetch(hotel,start_date):
    
    global hotels

    name = hotel.find(class_='sr-hotel__name')
    price = hotel.find(class_='bui-price-display__value prco-inline-block-maker-helper')
    stars = hotel.find(class_='bk-icon-wrapper bk-icon-stars star_track')
    distance = list(hotel.find(class_='sr_card_address_line').contents)

    if price and stars :
        price = price.string.strip().split('\xa0')[1].replace(",","")
        hotels["name"].append(name.string.strip())
        hotels['day'].append(start_date)
        hotels['price'].append(price)
        hotels['stars'].append(stars.span.string)
        hotels['distance'].append(distance[-2].string.strip().split(" ")[0])

    
    
def parser(driver,base_url,start_date,offset):
    page = driver.page_source
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print(f'fetching page {offset} on date {start_date}')
    html = BeautifulSoup(page,"lxml")
    next_page = html.find("a",title='Next page')
    hotelist = html.find_all("div",attrs={"data-hotelid":True})

    for hotel in hotelist:
        hotel_fetch(hotel,start_date)
    

    if next_page :
        offset+=30
        url = base_url + f"&row=30&offset={offset}"
        driver.get(url)
        parser(driver,base_url,start_date,offset)


@app.task
def search(item):
    global hotels

    offset=0
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    driver = webdriver.Firefox(options=options)
    url,start_date = item
    driver.get(url)
    parser(driver,url,start_date,offset)
    generate_csv(hotels)
    driver.quit()

        




