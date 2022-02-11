from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import concurrent.futures
import functools
import random

urls = [
        'http://www.yandex.ru',
        'http://www.google.com',
        'http://www.bbc.com',
        'http://www.facebook.com',
        'http://www.cnn.com',
        'http://lenta.ru',
        'http://www.stepic.ru',
        'http://www.python.org',
        ]

MAX_WORKERS = 3

def timer(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        t_start = time.time()
        result = f(*args, **kwargs)
        t_finish = time.time()
        t_diff = t_finish - t_start
        print(f"Time cost: {t_diff} sec.")
        return result
    return wrapper

class MyException(Exception):
    pass

class Task:
    _running = True

    def __init__(self, url):
        self.url = url

    def terminate(self):
        self._running = False

    @timer
    def run(self):
        size, title = 0, ''
        if self._running:
            print(f"Openning url: {self.url}")
            options = Options()
            browser = webdriver.Chrome(options=options)
            browser.get(self.url)
            browser.implicitly_wait(10)
            print(f"Done url: {self.url}")
            time.sleep(1)
            size, title = len(browser.page_source), browser.title
            browser.quit()
            if (random.randint(1,3)==2):
                print(f"Url: {self.url} generated exception")
                raise MyException
            print(f"Exited url: {self.url}")
        else:
            print(f"Canceled url: {self.url}")
        return size, title

def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers = MAX_WORKERS) as executor:
        tasks = [Task(url) for url in urls]
        future_to_url = {executor.submit(t.run): t.url for t in tasks}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                size, title = future.result()
            except MyException as exc:
                print(f'{url} generated an exception: {exc}')
                for task in tasks:
                    task.terminate()
                print([t._running for t in tasks])
                #for f in future_to_url:
                #    f.cancel()
                #    print(f"{future_to_url[f]}: {f.running()} {f.done()} {f.cancelled()}")
            except Exception as exc:
                print(f'{url} generated an exception: {exc}')
            else:
                print(f'{url} returned: Page {title} of {size} bytes')

if __name__ == "__main__":
    main()
