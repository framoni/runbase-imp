"""

RUNBASE-IMP

HTML scraping bot for monitoring Adidas Runners events

Author: Francesco Ramoni
        francesco[dot]ramoni@email.it
        https://github.com/framoni/

"""

import json
from lxml import html
from selenium import webdriver
from twilio.rest import Client

# PARAMETERS

# url to be scraped
url = 'https://www.adidas.it/adidasrunners/community/milano'

# request header
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'

# message
message = 'Le iscrizioni agli eventi Adidas di questa settimana sono state effettuate. runbase-imp'

# twilio data
with open("runbase-imp-param.json") as j:
     for line in j:
             td = json.loads(line)

# set webdriver options
options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument(f'user-agent={user_agent}')
# options.add_argument('incognito')

# CODE

# function to scrape events page until events are found
def scrape_for_events():
    print("Scraping HTML... ")
    flag = False
    while flag == False:
        try:
            browser.quit()
        except:
            pass
        browser = webdriver.Chrome(chrome_options=options)
        browser.get(url)
        innerHTML = browser.execute_script("return document.body.innerHTML")
        flag = "MONDAY HEROES" in innerHTML
    return browser

# function to login to the portal
def login(browser):
    print("Logging in... ")
    # click on login button
    button_access = browser.find_element_by_xpath('//*[@title="Accedi"]')
    browser.execute_script("arguments[0].click();", button_access)
    # send username, password and confirm
    browser.find_element_by_id('email').send_keys(td['email'])
    browser.find_element_by_id('password').send_keys(td['pass'])
    button_signin = browser.find_element_by_xpath('//*[@title="Invia"]')
    browser.execute_script("arguments[0].click();", button_signin)
    return browser

# scrape the events page
browser = scrape_for_events()
# login
browser = login(browser)

print("Signing up to the events... ")
# click on event button
event_url = browser.find_element_by_xpath('//a[contains(div//div//h3, "MONDAY HEROES") and contains(., "SENZA spogliatoio")]').get_attribute("href")
while True:
    try:
        browser.get(event_url)
        button_signup = browser.find_element_by_xpath('//*[@title="Iscriviti"]')
        browser.execute_script("arguments[0].click();", button_signup)
        break
    except Exception as e:
         print(e)
         continue

browser.quit()

# rescrape the events page
browser = scrape_for_events()
# login
browser = login(browser)

# find the second event
event_url = browser.find_element_by_xpath('//a[contains(div//div//h3, "ROAD TO YOUR BEST") and contains(., "SENZA spogliatoio")]').get_attribute("href")
while True:
    try:
        browser.get(event_url)
        button_signup = browser.find_element_by_xpath('//*[@title="Iscriviti"]').click()
    except:
         continue
    else:
         break

print("Notifying via SMS... ")

# send a SMS to notify
client = Client(td['twilio_client'], td['twilio_token'])
client.messages.create(to=td['phone_to'], from_=td['phone_from'], body=message)

print("Job done. ")
