from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ExpCond
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
from pprint import pprint
from pymongo import MongoClient

chrome_options = Options()

chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome()
driver.get("https://www.mvideo.ru/")
assert "М.Видео" in driver.title

element_present = ExpCond.presence_of_element_located((By.CLASS_NAME, 'sel-hits-block'))
blk = WebDriverWait(driver,15).until(element_present)

buttons = blk.find_element_by_class_name('carousel-paging').find_elements_by_tag_name('a')[1:]
for button in buttons:
    hits = blk.find_elements_by_class_name('gallery-list-item')
    print(f'Количество хитов: {len(hits)}')
    button.click()
    sleep(2)

hits = blk.find_elements_by_class_name('gallery-list-item')
print(f'Количество хитов: {len(hits)}')

client = MongoClient('localhost', 27017)
db = client['mvideo']
coll = db.hits

data_hits = []
for hit in hits:
    hit_h4 = hit.find_element_by_class_name('e-h4')
    name = hit_h4.get_attribute("title")
    price = hit.find_element_by_css_selector('div.c-pdp-price__current').get_attribute('innerHTML')
    d_hits = {}
    d_hits['name'] = name
    d_hits['price'] = int(''.join([i for i in price if i.isdigit()]))
    coll.update_one(d_hits, {'$set': d_hits}, upsert=True)
    data_hits.append(d_hits)

pprint(data_hits)

driver.quit()

