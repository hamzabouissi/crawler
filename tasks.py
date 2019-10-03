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
import psycopg2
from psycopg2.extras import DateRange


conn = psycopg2.connect(user="testuser",password="testuser",database='crawlerdb',host='postgres')
conn.set_session(autocommit=True)
cur = conn.cursor()

@app.task
def save(data):
    cur.executemany("insert into hotels values(%s,%s,%s,%s,%s,%s)",data)


def hotel_fetch(hotel):

    global start_date,final_date
    
    hotels = []
    name = hotel.find(class_='sr-hotel__name')
    price = hotel.find(class_='bui-price-display__value prco-inline-block-maker-helper')
    stars = hotel.find(class_='bk-icon-wrapper bk-icon-stars star_track')
    distance = list(hotel.find(class_='sr_card_address_line').contents)

    if price and stars :
        price = price.string.strip().split('\xa0')[1].replace(",","")
        hotels.append(name.string.strip())
        hotels.append(start_date)
        hotels.append(price)
        hotels.append(stars.span.string[0])
        hotels.append(distance[-2].string.strip().split(" ")[0])
        hotels.append(final_date)
    return hotels 

def parser(driver,base_url,offset):
    page = driver.page_source
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print(f'fetching page {offset} on date {start_date}')
    html = BeautifulSoup(page,"lxml")
    next_page = html.find("a",title='Next page')
    hotelist = html.find_all("div",attrs={"data-hotelid":True})
    hotels = []

    for hotel in hotelist:
        data = hotel_fetch(hotel)
        if data:hotels.append(data)
    
    print(hotels)
    save.delay(hotels)

    if next_page :
        offset+=30
        url = base_url + f"&row=30&offset={offset}"
        driver.get(url)
        parser(driver,base_url,offset)


@app.task
def search(item):
    global start_date,final_date
    offset=0
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    driver = webdriver.Firefox(options=options)
    url,start_date,final_date = item
    driver.get(url)
    parser(driver,url,offset)
    driver.quit()

        




