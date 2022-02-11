from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import concurrent.futures
import functools

urls = [
        'http://www.yandex.ru',
        'http://www.google.com',
        'http://www.bbc.com',
        'http://www.facebook.com',
        'http://www.cnn.com',
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

@timer
def open_url_worker(url):
    print(f"Openning url: {url}")
    options = Options()
    browser = webdriver.Chrome(options=options)
    browser.get(url)
    browser.implicitly_wait(10)
    print(f"Done url: {url}")
    time.sleep(1)
    size, title = len(browser.page_source), browser.title
    browser.quit()
    print(f"Exited url: {url}")
    return size, title

def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers = MAX_WORKERS) as executor:
        future_to_url = {executor.submit(open_url_worker, url): url for url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                size, title = future.result()
            except Exception as exc:
                print(f'{url} generated an exception: {exc}')
            else:
                print(f'{url} returned: Page {title} of {size} bytes')

if __name__ == "__main__":
    main()
