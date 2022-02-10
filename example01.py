from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import threading

urls = [
        'http://www.yandex.ru',
        'http://www.google.com',
        'http://www.bbc.com',
        ]

def open_url(url):
    print(f"Openning url: {url}")
    options = Options()
    browser = webdriver.Chrome(options=options)
    browser.get(url)
    browser.implicitly_wait(10)
    print(f"Done url: {url}")
    time.sleep(30)
    browser.quit()
    print(f"Exited url: {url}")

for url in urls:
    t = threading.Thread(target = open_url, args=(url,), name=f"Openner-{url}")
    t.start()


