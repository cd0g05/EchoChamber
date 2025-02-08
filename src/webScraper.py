import time

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import re
import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class Newspage:
    def __init__(self, name:str, url:str, classes, allfile:str, dayfile:str, timestamp): #, flag:int
        self.name = name  # member variable
        self.url = url    # member variable
        self.classes = classes
        self.allfile = allfile
        self.dayfile = dayfile
        # self.flag = flag
        self.headlines = self.get_headlines()
        self.timestamp = timestamp
        # if flag == 1:
        #     self.html = self.get_headlines()
        # elif flag == 2:
        #     self.html = self.get_headlines()


    def get_headlines(self):
        title_classes = [self.classes]
        doc = self.get_html(self.url)
        return self.extract_headlines(title_classes, doc)

    def get_html(self, url:str):
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/537.36"
        }
        result = requests.get(url, headers=headers)
        return BeautifulSoup(result.text, "html.parser")

    def extract_headlines(self, classes, doc):
        hl_texts = set()
        for class_name in classes:
            for tag in doc.find_all(True, class_=class_name):
                text = tag.get_text(strip=True)
                if 30 < len(text) < 120:
                    hl_texts.add(text)
        return list(hl_texts)

    def write_hl_to_allfile(self):
            with open(self.allfile, 'a') as file:
                file.write(f"\n+++++++++++++++++++++\nDate: {self.timestamp}\n\n")
                count = 0
                for headline in self.headlines:
                    if count > 20:
                        break
                    file.write(headline)
                    file.write(f"\n")
                    count += 1
    def write_hl_to_dayfile(self):
        with open(self.dayfile, 'w') as file:
                count = 0
                for headline in self.headlines:
                    if count > 20:
                        break
                    file.write(headline)
                    file.write(f"\n")
                    count += 1
    def write_hl_to_files(self):
        self.write_hl_to_allfile()
        self.write_hl_to_dayfile()


class Headline:
    def __init__(self, headline:str):
        self.headline = headline
        # self.category = category

class CNN_DATA:
    def __init__(self):
        self.classes = ["container__headline-text"]
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.name = "CNN"
        self.url = "https://www.cnn.com"
        self.allfile = "/Users/cartercripe/dev/code/projects/EchoChamber/src/textHeadlines/allCnnHeadlines.txt"
        self.dayfile = "/Users/cartercripe/dev/code/projects/EchoChamber/src/textHeadlines/dayCnnHeadlines.txt"

class FOX_DATA:
    def __init__(self):
        self.classes = ["title"]
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.name = "Fox"
        self.url = "https://www.foxnews.com"
        self.allfile = "/Users/cartercripe/dev/code/projects/EchoChamber/src/textHeadlines/allFoxHeadlines.txt"
        self.dayfile = "/Users/cartercripe/dev/code/projects/EchoChamber/src/textHeadlines/dayFoxHeadlines.txt"

class NYT_DATA:
    def __init__(self):
        self.classes = ["css-xdandi","indicate-hover css-1gg6cw2","indicate-hover css-91bpc3", "indicate-hover css-11gjfuy", "indicate-hover css-1a5fuvt"]
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.name = "New York Times"
        self.url = "https://www.nytimes.com"
        self.allfile = "/Users/cartercripe/dev/code/projects/EchoChamber/src/textHeadlines/allNytHeadlines.txt"
        self.dayfile = "/Users/cartercripe/dev/code/projects/EchoChamber/src/textHeadlines/dayNytHeadlines.txt"

class NBC_DATA:
    def __init__(self):
        self.classes = ["storyline__headline founders-cond fw6 large","related-content-tease__headline-link", "multistoryline__headline founders-cond fw6 large noBottomSpace"]
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.name = "NBC"
        self.url = "https://www.nbcnews.com"
        self.allfile = "/Users/cartercripe/dev/code/projects/EchoChamber/src/textHeadlines/allNbcHeadlines.txt"
        self.dayfile = "/Users/cartercripe/dev/code/projects/EchoChamber/src/textHeadlines/dayNbcHeadlines.txt"

class OANN_DATA:
    def __init__(self):
        self.classes = ["slider-title","entry-title"]
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.name = "OANN"
        self.url = "https://www.oann.com"
        self.allfile = "/Users/cartercripe/dev/code/projects/EchoChamber/src/textHeadlines/allOannHeadlines.txt"
        self.dayfile = "/Users/cartercripe/dev/code/projects/EchoChamber/src/textHeadlines/dayOannHeadlines.txt"

class NPR_DATA:
    def __init__(self):
        self.classes = ["title"]
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.name = "NPR"
        self.url = "https://www.npr.org"
        self.allfile = "/Users/cartercripe/dev/code/projects/EchoChamber/src/textHeadlines/allNprHeadlines.txt"
        self.dayfile = "/Users/cartercripe/dev/code/projects/EchoChamber/src/textHeadlines/dayNprHeadlines.txt"

class AP_DATA:
    def __init__(self):
        self.classes = ["PagePromoContentIcons-text"]
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.name = "AP"
        self.url = "https://www.apnews.com"
        self.allfile = "/Users/cartercripe/dev/code/projects/EchoChamber/src/textHeadlines/allApHeadlines.txt"
        self.dayfile = "/Users/cartercripe/dev/code/projects/EchoChamber/src/textHeadlines/dayApHeadlines.txt"

class NEWSMAX_DATA:
    def __init__(self):
        self.classes = ["Default", "nmNewsfrontHeadLink Default", "css1"]
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.name = "Newsmax"
        self.url = "https://www.newsmax.com"
        self.allfile = "/Users/cartercripe/dev/code/projects/EchoChamber/src/textHeadlines/allNewsmaxHeadlines.txt"
        self.dayfile = "/Users/cartercripe/dev/code/projects/EchoChamber/src/textHeadlines/dayNewsmaxHeadlines.txt"

class DW_DATA:
    def __init__(self):
        self.classes = ["Homepage_topStoryTitle__vxI_h", "allPosts_textContainer__KAL9G"]
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.name = "Dailywire"
        self.url = "https://www.dailywire.com"
        self.allfile = "/Users/cartercripe/dev/code/projects/EchoChamber/src/textHeadlines/allDailywireHeadlines.txt"
        self.dayfile = "/Users/cartercripe/dev/code/projects/EchoChamber/src/textHeadlines/dayDailywireHeadlines.txt"

class WT_DATA:
    def __init__(self):
        self.classes = ["article-headline"]
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.name = "Washington Times"
        self.url = "https://www.washingtontimes.com"
        self.allfile = "/Users/cartercripe/dev/code/projects/EchoChamber/src/textHeadlines/allWashTimesHeadlines.txt"
        self.dayfile = "/Users/cartercripe/dev/code/projects/EchoChamber/src/textHeadlines/dayWashTimesHeadlines.txt"

class WP_DATA:
    def __init__(self):
        self.classes = ["headline relative gray-darkest pb-xs", "wpds-c-iiQaMf wpds-c-iiQaMf-ihMULTC-css"]
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.name = "Washington Post"
        self.url = "https://www.washingtonpost.com"
        self.allfile = "/Users/cartercripe/dev/code/projects/EchoChamber/src/textHeadlines/allWashPostHeadlines.txt"
        self.dayfile = "/Users/cartercripe/dev/code/projects/EchoChamber/src/textHeadlines/dayWashPostHeadlines.txt"

news_sources = [
    CNN_DATA, FOX_DATA, NYT_DATA, NBC_DATA, OANN_DATA,
    NPR_DATA, AP_DATA, NEWSMAX_DATA, DW_DATA, WT_DATA, WP_DATA
]

count = 1
for source in news_sources:
    data = source()  # Instantiate the class
    news = Newspage(data.name, data.url, data.classes, data.allfile, data.dayfile, data.timestamp)
    news.write_hl_to_files()

    print(count)
    count += 1