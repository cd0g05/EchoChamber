from bs4 import BeautifulSoup
import requests
from selenium import webdriver


class ReadPage:

    def get_cnn_headlines(self):
        # with open ("https://www.cnn.com", "r") as f:
        result = requests.get("https://www.cnn.com")
        doc = BeautifulSoup(result.text, "html.parser")
        hl_tags = doc.find_all(class_="container__headline-text")

        return hl_tags

    def get_fox_headlines(self):
        # with open ("https://www.cnn.com", "r") as f:
        result = requests.get("https://www.foxnews.com")
        doc = BeautifulSoup(result.text, "html.parser")
        hl_tags = doc.find_all(class_="title")

        return hl_tags

    def get_nyt_headlines(self):
        # with open ("https://www.cnn.com", "r") as f:
        result = requests.get("https://www.nytimes.com")
        doc = BeautifulSoup(result.text, "html.parser")
        title_classes = ["indicate-hover css-91bpc3", "indicate-hover css-11gjfuy", "indicate-hover css-1a5fuvt"]
        hl_tags = []
        for class_name in title_classes:
            hl_tags.extend(doc.find_all(True, class_=class_name))

        return hl_tags

    def get_nbc_headlines(self):
        # with open ("https://www.cnn.com", "r") as f:
        result = requests.get("https://www.nbcnews.com")
        doc = BeautifulSoup(result.text, "html.parser")
        title_classes = ["storyline__headline founders-cond fw6 large","related-content-tease__headline-link", "multistoryline__headline founders-cond fw6 large noBottomSpace"]
        hl_tags = []
        for class_name in title_classes:
            hl_tags.extend(doc.find_all(True, class_=class_name))

        return hl_tags

    def get_oann_headlines(self):
        result = requests.get("https://www.oann.com")
        doc = BeautifulSoup(result.text, "html.parser")
        title_classes = ["slider-title","entry-title"]
        hl_tags = []
        for class_name in title_classes:
            hl_tags.extend(doc.find_all(True, class_=class_name))

        return hl_tags

    def get_nyp_headlines(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run in headless mode
        driver = webdriver.Chrome(options=options)
        driver.get("https://nypost.com")
        driver.implicitly_wait(5)
        doc = BeautifulSoup(driver.page_source, "html.parser")
        title_classes = ["story__headline headline headline--xl","story__headline headline headline--sm", "story__headline headline headline--xxs"]
        hl_tags = []
        for class_name in title_classes:
            hl_tags.extend(doc.find_all(True, class_=class_name))
        # hl_tags = doc.find_all("title")
        return hl_tags

    def test_nyp(self):
        url = "https://nypost.com/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(url, headers=headers)
        print(response.text[:1000])


page = ReadPage()

cnn = page.get_cnn_headlines()
nyt = page.get_nyt_headlines()
nbc = page.get_nbc_headlines()

fox = page.get_fox_headlines()
oann = page.get_oann_headlines()
nyp = page.get_nyp_headlines()

# page.test_nyp()
# print(nyp)
for headline in nyp:
    text = headline.get_text(strip=True)
    print(text)
# print(cnn)


