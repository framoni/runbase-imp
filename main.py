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
import time
from twilio.rest import Client

#-------------------------------------------------------------------------------

# PARAMETERS

# url to be scraped
ar_url = 'https://www.adidas.it/adidasrunners/community/milano'
# request header
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
# message
message = 'Le iscrizioni agli eventi Adidas Runners di questa settimana sono state effettuate. runbase-imp'
# twilio data
with open("runbase-imp-param.json") as j:
     for line in j:
             td = json.loads(line)
# set webdriver options
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument(f'user-agent={user_agent}')

#-------------------------------------------------------------------------------

# FUNCTIONS

# function to scrape event url
def scrape_event_url(event_name):
    browser.get(ar_url)
    event_url = browser.find_element_by_xpath('//a[contains(div//div//h3, "{}") and contains(., "SENZA spogliatoio")]'.format(event_name)).get_attribute("href")
    return event_url

# function to sign up to an event
def event_signup(event_name, do_login):
    print("Event: {}".format(event_name))
    event_url = scrape_event_url(event_name)
    # go to event page
    browser.get(event_url)
    # login
    if do_login:
        login()
    # wait 10 seconds to bypass a UI visual bug (?) showing a second login form
    time.sleep(10)
    # sign up to the event
    button_signup = browser.find_element_by_xpath('//*[@title="Iscriviti"]')
    browser.execute_script("arguments[0].click();", button_signup)

# function to login to the portal
def login():
    # click on login button
    button_login = browser.find_element_by_xpath('//*[@title="Accedi"]')
    browser.execute_script("arguments[0].click();", button_login)
    # send username, password and confirm
    browser.find_element_by_id('email').send_keys(td['email'])
    browser.find_element_by_id('password').send_keys(td['pass'])
    button_send = browser.find_element_by_xpath('//*[@title="Invia"]')
    browser.execute_script("arguments[0].click();", button_send)
    return

#-------------------------------------------------------------------------------

# SCRAPING

# create a new driver
browser = webdriver.Chrome(chrome_options=options)
browser.implicitly_wait(60)

print("Signing up to the Adidas Runners events... ")

# sign up to events of interest
event_signup('MONDAY HEROES', True)
event_signup('ROAD TO YOUR BEST', False)

# close the driver
browser.quit()

# send a SMS to notify
print("Notifying via SMS... ")
client = Client(td['twilio_client'], td['twilio_token'])
client.messages.create(to=td['phone_to'], from_=td['phone_from'], body=message)

print("Job done. ")
