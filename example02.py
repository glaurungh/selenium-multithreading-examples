from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import threading
from queue import Queue

urls = [
        'http://www.yandex.ru',
        'http://www.google.com',
        'http://www.bbc.com',
        'http://www.facebook.com',
        'http://www.cnn.com',
        ]

MAX_WORKERS = 3

def open_url_worker(queue):
    url = queue.get()
    print(f"Openning url: {url}")
    options = Options()
    browser = webdriver.Chrome(options=options)
    browser.get(url)
    browser.implicitly_wait(10)
    print(f"Done url: {url}")
    time.sleep(30)
    browser.quit()
    queue.task_done()
    print(f"Exited url: {url}")

def getQueue():
    q = Queue()
    for url in urls:
        q.put(url)
    return q


def main():
    queue = getQueue()
    count = 1
    while not queue.empty():
        if threading.active_count() <= MAX_WORKERS:
            t = threading.Thread(target = open_url_worker, args=(queue,), name=f"Openner-{count}")
            count += 1
            print(f"Thread {t.name} created")
            t.start()

if __name__ == "__main__":
    main()
