from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ExpCond
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from pprint import pprint
from pymongo import MongoClient

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(options=chrome_options)
driver.get('https://mail.ru/')
assert 'Mail.ru' in driver.title

element_present = ExpCond.presence_of_element_located((By.ID, 'mailbox:login'))
username = WebDriverWait(driver,10).until(element_present)
#username = driver.find_element_by_id('mailbox:login')
username.send_keys('study.ai_172')
username.send_keys(Keys.RETURN)

element_present = ExpCond.element_to_be_clickable((By.ID, 'mailbox:password'))
input_password = WebDriverWait(driver,10).until(element_present)
#input_password = driver.find_element_by_id('mailbox:password')
input_password.click()
input_password.send_keys('*********')
input_password.send_keys(Keys.RETURN)

element_present = ExpCond.presence_of_element_located((By.CLASS_NAME, "dataset__items"))
dataset = WebDriverWait(driver,60).until(element_present)
elements = dataset.find_elements_by_tag_name("a")

all_el = len(elements)
print(f'Всего {all_el} писем.')
letters = []
k = 1
for letter in elements:
    try:
        l_url = letter.get_attribute("href")
        l_from = letter.find_element_by_class_name('ll-crpt').get_attribute("title")
        l_subj = letter.find_element_by_class_name('ll-sj__normal').text
        letters.append({'from': l_from, 'subj': l_subj, 'link': l_url})
        k += 1
        if k > 10:
            break
    except Exception  as e:
        print(e)

pprint(letters)
print('----------------------')

client = MongoClient('localhost', 27017)
db = client['mail']
coll = db.mail_ru

for letter in letters:
    driver.get(letter['link'])
    element_present = ExpCond.presence_of_element_located((By.CLASS_NAME, 'letter-body'))
    WebDriverWait(driver,15).until(element_present)
    l_text = driver.find_element_by_class_name('letter-body').text.strip()
    l_date = driver.find_element_by_class_name('letter__date').text
    letter['date'] = l_date
    letter['body'] = l_text
    coll.update_one(letter, {'$set': letter}, upsert=True)
    pprint(letter)
    print('======================')

driver.find_element_by_id('PH_logoutLink').click()
driver.close()
