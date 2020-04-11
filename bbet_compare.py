import requests
from requests_html import HTMLSession

url = 'https://www.bbet.com.au/sports/football'
doc = requests.get(url)

session = HTMLSession()
resp = session.get(url)

resp.html.render()
with open('transfer.txt', 'w') as f:
    f.write(resp.html.html)