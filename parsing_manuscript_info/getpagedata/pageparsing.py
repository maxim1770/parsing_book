import os
import datetime
import time
import json
import csv
from bs4 import BeautifulSoup

from pagerequests import PageRequests


class PageParsing:

    def __init__(self, src):
        self.src = src
        self.data = {}

        self.soup = BeautifulSoup(self.src, "lxml")

    def get_data(self):
        return self.data

    def collect_data(self):
        title = self.soup.find('div', class_="hero-content").find("h1").text

        self.data['title'] = title

    def collect_data_table(self):

        table = self.soup.find('div', class_="book-info")

        table_rows = table.find_all('div', class_="book-info-table")

        for row in table_rows:
            pass
