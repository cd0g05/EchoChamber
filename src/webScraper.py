from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime



class ReadPage:

    def get_cnn_headlines(self):
        title_classes = ["container__headline-text"]
        doc = page.get_html("https://www.cnn.com")
        return page.extract_headlines(title_classes, doc)

    def get_fox_headlines(self):
        title_classes = ["title"]
        doc = page.get_html("https://www.foxnews.com")
        return page.extract_headlines(title_classes, doc)

    def get_nyt_headlines(self):
        title_classes = ["css-xdandi","indicate-hover css-1gg6cw2","indicate-hover css-91bpc3", "indicate-hover css-11gjfuy", "indicate-hover css-1a5fuvt"]
        doc = page.get_html("https://www.nytimes.com")
        return page.extract_headlines(title_classes, doc)

    def get_nbc_headlines(self):
        title_classes = ["storyline__headline founders-cond fw6 large","related-content-tease__headline-link", "multistoryline__headline founders-cond fw6 large noBottomSpace"]
        doc = page.get_html("https://www.nbc.com")
        return page.extract_headlines(title_classes, doc)

    def get_oann_headlines(self):
        title_classes = ["slider-title","entry-title"]
        doc = page.get_html("https://www.oann.com")
        return page.extract_headlines(title_classes, doc)

    def get_npr_headlines(self):
        title_classes = ["title"]
        doc = page.get_html("https://www.npr.org")
        return page.extract_headlines(title_classes, doc)

    def get_politico_headlines(self):
        title_classes = ["headline is-standard-typeface", "headline  is-alternate-typeface", "headline track-visited", "media-item__title"]
        doc = page.get_html("https://www.politico.com")
        return page.extract_headlines(title_classes, doc)

    def get_nyp_headlines(self):
        options = Options()
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36")
        options.add_argument("--headless=new")

        service = Service(ChromeDriverManager().install())  # Auto-downloads ChromeDriver if needed
        driver = webdriver.Chrome(service=service, options=options)

        driver.set_page_load_timeout(20)  # Timeout if it takes too long
        try:
            driver.get("https://nypost.com")
            driver.implicitly_wait(5)
            doc = BeautifulSoup(driver.page_source, "html.parser")
            title_classes = ["story__headline headline headline--xl","story__headline headline headline--sm", "story__headline headline headline--xxs"]
            hl_tags = []
            for class_name in title_classes:
                hl_tags.extend(doc.find_all(True, class_=class_name))
            # hl_tags = doc.find_all("title")
            return hl_tags
        except Exception as e:
            print(f"Error loading NYP: {e}")
        finally:
            driver.quit()


    def get_html(self, url:str):
        result = requests.get(url)
        return BeautifulSoup(result.text, "html.parser")

    def extract_headlines(self, html, doc):
        hl_tags = []
        for class_name in html:
            hl_tags.extend(doc.find_all(True, class_=class_name))
        return hl_tags


    def compile_headlines(self):
        # nyp = page.get_nyp_headlines()
        news_sources = [
            page.get_cnn_headlines()[6:],
            page.get_nyt_headlines(),
            page.get_nbc_headlines(),
            page.get_fox_headlines(),
            page.get_oann_headlines(),
            page.get_npr_headlines(),
            page.get_politico_headlines()
        ] #, npy
        news_sources[3] = [headline for i, headline in enumerate(news_sources[3]) if i not in [0, 2, 4]]
        return news_sources

    def write_hl_to_file(self, flag:str, url:str, news_sources, names, timestamp):
            with open(url, flag) as file:
                news_src = 0
                if (flag == 'a'):
                    file.write(f"\n+++++++++++++++++++++\nDate: {timestamp}\n")
                for source in news_sources:
                    count = 0
                    file.write(f"\n{names[news_src]}\n--------------------\n")
                    for headline in source:
                        if count > 20:
                            break
                        text = headline.get_text(strip=True)
                        file.write(text)
                        file.write(f"\n")
                        count += 1
                    news_src += 1
    def run_prog(self, hls):
        names =  ["CNN", "New York Times", "NBC", "FOX", "OANN", "NPR", "Politico"] #, "New York Post"
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")  # Format: YYYY-MM-DD HH:MM:SS
        page.write_hl_to_file('a', '/Users/cartercripe/dev/code/projects/EchoChamber/src/allHeadlines.txt', hls, names, timestamp)
        page.write_hl_to_file('w', '/Users/cartercripe/dev/code/projects/EchoChamber/src/daysHeadlines.txt', hls, names, timestamp)


page = ReadPage()
hls = page.compile_headlines()
page.run_prog(hls)


