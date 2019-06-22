"""

RUNBASE-IMP

HTML scraping bot for monitoring Adidas events

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
message = 'Le iscrizioni agli eventi Adidas di questa settimana sono aperte. runbase-imp'

# twilio data
with open("runbase-imp-param.json") as j:
     for line in j:
             td = json.loads(line)

# set webdriver options
options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument(f'user-agent={user_agent}')
options.add_argument('incognito')

# create a new webdriver and scrape HTML until events are found
flag = False
attempt = 1
while flag == False:
    try:
        browser.quit()
    except:
        pass
    print("Attempt ", attempt)
    attempt += 1
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(url)
    innerHTML = browser.execute_script("return document.body.innerHTML")
    with open("content.txt", "w") as f:
        f.write(innerHTML)
        # look for events
        flag = "MONDAY HEROES" in innerHTML

try:
    # click on event button
    button_event = browser.find_element_by_xpath('//div[contains(.//div//h3, "MONDAY HEROES") and contains(., "CON spogliatoio")]/child::button')
    button_event.click()
    # click on event button
    button_signup = browser.find_element_by_xpath('//*[@title="Iscriviti"]').click()
except:
    # print("Button not found!")
    pass
finally:
    input()
    browser.quit()

# send a SMS to notify
# for tag in tree.xpath('//div[@class="description-2dxZCuD"]//h3'):
#     if 'MONDAY HEROES' in tag.text_content() or 'ROAD TO YOUR BEST' in tag.text_content():
#         # send SMS alarm
#         client = Client(td['twilio_client'], td['twilio_token'])
#         client.messages.create(to=td['phone_to'], from_=td['phone_from'], body=message)
