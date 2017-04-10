#!/usr/bin/env/python3

import re
import sys

from datetime import date, datetime, timedelta
from selenium import webdriver
from urllib.request import urlopen

class ERDDAPScraper:
    def __init__(self, dataset_id, start, stop, latitude, longitude, step=30):
        # set ERDDAP database by ID
        self.dataset_id = dataset_id
        self.database = 'https://coastwatch.pfeg.noaa.gov/erddap/griddap/{}.html'.format(self.dataset_id)

        # range of dates to be pulled
        self.start = self.validate_date(start) 
        self.stop = self.validate_date(stop)

        # initialize scraper
        self.driver = webdriver.PhantomJS()
        self.driver.get(self.database)
        self.generic_link = self.generate_generic_link()

        # coordinates
        self.latitude = latitude
        self.longitude = longitude

        # number of days pulled at once
        self.step = step

    def find_date_bounds(self, date_entry):
        text = date_entry.get_attribute('onmouseover')
        bounds = re.findall('\d{4}-\d{2}-\d{2}T[01][0268]:00:00Z', text)

        try:
            self.lo = self.validate_date(bounds[0])
            self.hi = self.validate_date(bounds[1])

        except IndexError as e:
            print(e)
            self.lo = self.validate_date('1970-1-1')
            self.hi = self.validate_date('2020-1-1')

    def generate_generic_link(self):
        idx = 0
        while True: # Surely there's a better way than looping until failure
            try:
                elem = self.driver.find_element_by_name('avar{}'.format(idx))

            except:
                break

            if elem.get_attribute('value') == 'time':
                self.find_date_bounds(self.driver.find_element_by_name('start{}'.format(idx)))
                start, stop = '{0}', '{1}'

            elif elem.get_attribute('value') == 'latitude':
                start, stop = '{2}', '{2}'

            elif elem.get_attribute('value') == 'longitude':
                start, stop = '{3}', '{3}'

            else:
                idx += 1
                continue

            self.data_entry('start{}'.format(idx), start)
            self.data_entry('stop{}'.format(idx), stop)

            idx += 1

        self.driver.find_element_by_name('getUrl').click()

        return self.driver.find_element_by_name('tUrl').get_attribute('value')

    def data_entry(self, name, data):
        tgt = self.driver.find_element_by_name(name)
        tgt.clear()
        tgt.send_keys(data)

    def create_date_intervals(self):
        dates = []
        curr = self.start

        if self.start < self.lo:
            print('Start date is out of bounds, setting it to {}.'.format(self.lo))
            self.start = self.lo

        if self.stop > self.hi:
            print('Stop date is out of bounds, setting it to {}.'.format(self.hi))
            self.stop = self.hi

        elif self.stop < self.start:
            print('Stop date is earlier than start date. Setting it to {}'.format(self.hi))
            self.stop = self.hi

        while curr < self.stop:
            dates.append(curr.strftime('%Y-%m-%dT00:00:00Z'))
            curr = curr + timedelta(days=self.step)
        
        if curr != self.stop:
            dates.append(self.stop.strftime('%Y-%m-%dT00:00:00Z'))

        return dates

    def create_links(self):
        dates = self.create_date_intervals()

        return [ self.generic_link.format(dates[i], dates[i+1], self.latitude, self.longitude) for i in range(len(dates)-1) ]

    def validate_date(self, date):
        try:
            date = re.split('-|/', date[:10])
            date = [ int(elem) for elem in date ]
            return datetime(date[0], date[1], date[2])

        except:
            if type(date) == date or type(date) == datetime:
                return date

            else:
                print('WARNING: Could not recognize date "{}"'.format(date))
                return None
                
    def pull_data(self):
        links = self.create_links()

        for link in links:
            self.driver.get(link)
            rows = self.driver.find_elements_by_tag_name('tr')[3:]
            last_date = None

            for row in rows[:-1]:
                line = []
                cols = row.find_elements_by_tag_name('td')

                for i in range(len(cols)):
                    val = cols[i].text

                    if i == 0 and val == last_date:
                        continue

                    if i == 0:
                        last_date = val

                    line.append(val)

                print(' '.join(line))

