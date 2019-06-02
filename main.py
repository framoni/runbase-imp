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
options.add_argument('headless')
options.add_argument(f'user-agent={user_agent}')

# create webdriver and scrape HTML
browser = webdriver.Chrome(chrome_options=options)
browser.get(url)
innerHTML = browser.execute_script("return document.body.innerHTML")
browser.quit()

# look for events
tree = html.fromstring(innerHTML)
for tag in tree.xpath('//div[@class="description-2dxZCuD"]//h3'):
    if 'MONDAY HEROES' in tag.text_content() or 'ROAD TO YOUR BEST' in tag.text_content():
        # send SMS alarm
        client = Client(td['twilio_client'], td['twilio_token'])
        client.messages.create(to=td['phone_to'], from_=td['phone_from'], body=message)
