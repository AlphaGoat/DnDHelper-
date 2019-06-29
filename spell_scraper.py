import requests
from bs4 import BeautifulSoup

spell_page_url = "https://www.dnd-spells.com/spells"
spell_page = requests.get(spell_page_url)

if spell_page.status_code == 200:
    spell_soup = BeautifulSoup(spell_page.text, 'html.parser')
    print(spell_soup.prettify())


