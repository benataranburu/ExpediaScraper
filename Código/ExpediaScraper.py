############################################################
################  ExpediaScraper.py  #######################
############################################################

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import pandas as pd
import time
import datetime
import myconstants as mc

browser = webdriver.Chrome(executable_path='chromedriver')

# User space
departure_country = 'Bilbao'
arrival_country = 'London'
day = '03'
month = '10'
year = '2019'

# Tickets
## Ticket type path
one_way_ticket = "//label[@id='flight-type-one-way-label-hp-flight']"
#return_ticket = "//label[@id='flight-type-roundtrip-label-hp-flight']"
#multi_ticket = "//label[@id='flight-type-multi-dest-label-hp-flight']"

## Choose ticket type
def ticket_chooser(ticket):
    try:
        ticket_type = browser.find_element_by_xpath(ticket)
        ticket_type.click()
    except Exception as e:
        pass

# Choose departure country
def departure_city_chooser(departure_country):
    fly_from = browser.find_element_by_xpath("//input[@id='flight-origin-hp-flight']")
    time.sleep(mc.wait_next_step)
    fly_from.clear()
    time.sleep(mc.wait_next_step)
    fly_from.send_keys('  ' + departure_country)
    time.sleep(mc.wait_next_step)
    first_item = browser.find_element_by_xpath("//a[@id='aria-option-0']")
    time.sleep(mc.wait_next_step)
    first_item.click()

# Choose arrival country
def arrival_city_chooser(arrival_country):
    fly_to = browser.find_element_by_xpath("//input[@id='flight-destination-hp-flight']")
    time.sleep(mc.wait_next_step)
    fly_to.clear()
    time.sleep(mc.wait_next_step)
    fly_to.send_keys('  ' + arrival_country)
    time.sleep(mc.wait_next_step)
    first_item = browser.find_element_by_xpath("//a[@id='aria-option-0']")
    time.sleep(mc.wait_next_step)
    first_item.click()

# Choose departure date
def departure_date_chooser(day, month, year):
    dep_date_button = browser.find_element_by_xpath("//input[@id='flight-departing-single-hp-flight']")
    dep_date_button.clear()
    dep_date_button.send_keys(day + '/' + month + '/' + year)

# Search
def search():
    search = browser.find_element_by_xpath("//button[@class='btn-primary btn-action gcw-submit']")
    search.submit()
    time.sleep(10)

# Create data frame
df = pd.DataFrame()
def compile_data(day, month, year):
    global df
    global dep_times_list
    global arr_times_list
    global airlines_list
    global price_list
    global durations_list
    global stops_list
    global layovers_list

    #date_flight
    date_flight = day + '/' + month + '/' + year

    #name_departure_airport

    #name_arrival_airport

    #name_airline
    airlines = browser.find_elements_by_xpath("//span[@data-test-id='airline-name']")
    airlines_list = [value.text for value in airlines]

    #duration
    durations = browser.find_elements_by_xpath("//span[@data-test-id='duration']")
    durations_list = [value.text for value in durations]

    #time_departure
    dep_times = browser.find_elements_by_xpath("//span[@data-test-id='departure-time']")
    dep_times_list = [value.text for value in dep_times]

    #time_arrival
    arr_times = browser.find_elements_by_xpath("//span[@data-test-id='arrival-time']")
    arr_times_list = [value.text for value in arr_times]

    #number_stops
    stops = browser.find_elements_by_xpath("//span[@class='number-stops']")
    stops_list = [value.text for value in stops]

    #name_layovers
    layovers = browser.find_elements_by_xpath("//span[@data-test-id='layover-airport-stops']")
    layovers_list = [value.text for value in layovers]

    #prices
    prices = browser.find_elements_by_xpath("//span[@data-test-id='listing-price-dollars']")
    price_list = [value.text.split('€')[1] for value in prices]

    for i in range(len(dep_times_list)):

        try:
            df.loc[i, 'date_flight'] = date_flight
        except Exception as e:
            pass

        try:
            df.loc[i, 'name_departure_airport'] = departure_country
        except Exception as e:
            pass

        try:
            df.loc[i, 'name_arrival_airport'] = arrival_country
        except Exception as e:
            pass

        try:
            df.loc[i, 'name_airline'] = airlines_list[i]
        except Exception as e:
            pass

        try:
            df.loc[i, 'duration'] = durations_list[i]
        except Exception as e:
            pass

        try:
            df.loc[i, 'time_departure'] = dep_times_list[i]
        except Exception as e:
            pass

        try:
            df.loc[i, 'time_arrival'] = arr_times_list[i]
        except Exception as e:
            pass

        try:
            df.loc[i, 'number_stops'] = stops_list[i]
        except Exception as e:
            pass

        try:
            df.loc[i, 'name_layovers'] = layovers_list[i]
        except Exception as e:
            pass

        try:
            df.loc[i, 'prices'] = price_list[i]
        except Exception as e:
            pass

# Run code
link = 'https://www.expedia.es/'
browser.get(link)
time.sleep(5)

#choose flights only
flights_only = browser.find_element_by_xpath("//button[@id='tab-flight-tab-hp']")
flights_only.click()
ticket_chooser(one_way_ticket)
departure_city_chooser(departure_country)
arrival_city_chooser(arrival_country)
departure_date_chooser(day, month, year)
search()
compile_data(day, month, year)
print(df)
df.to_csv('PVCM-' + time.strftime("%m-%Y") +'.csv', header=True, index=False)
