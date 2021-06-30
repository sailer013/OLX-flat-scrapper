import requests
from bs4 import BeautifulSoup
import time
import random
import re
import sqlite3
import sys
# TODO dodać listę url
url = 'https://www.olx.pl/nieruchomosci/stancje-pokoje/wroclaw/' \
      '?search%5Bfilter_float_price%3Ato%5D=750&search%5Bfilter_enum_roomsize%5D%5B0%5D=one&page='


con = sqlite3.connect('flats.db')
cur = con.cursor()


def soup_find(urls, tag, class_html, f_all=True):
    r = requests.get(urls)
    print(r.status_code)
    soup = BeautifulSoup(r.text, 'html.parser')
    if f_all:
        find = soup.find_all(tag, class_=class_html)
    else:
        find = soup.find(tag, class_=class_html)
    return find, soup


def web_links(soup_find_a):
    links_list = []
    for link in soup_find_a:
        link = link.get('href')
        links_list.append(link)
    return links_list


def regex(pattern, adv_text):
    ptrn = re.compile(pattern, re.IGNORECASE)
    search = re.findall(ptrn, adv_text)
    return search

def search_offer(links_list):
    for link in links_list:
        print(link)
        compare_db = cur.execute('SELECT * FROM flats WHERE Link=(?);', (link,)).fetchone()
        if link.startswith('https://www.otodom'):
            print('Pass URL')
            continue
        elif compare_db:
            sys.exit()
        sec = random.uniform(1, 3)
        print(f'Wait: {sec}')
        time.sleep(sec)
        adv_text, l_soup = soup_find(link, tag='div', class_html='css-g5mtbi-Text', f_all=False)
        try:
            text = adv_text.get_text()
        except AttributeError:
            print('Attr err')
            continue
        price_tag = l_soup.find('h3', class_='css-8kqr5l-Text eu5v0x0')
        price_text = price_tag.get_text()
        price = ''.join(regex(r'\d{3}', price_text))
        other_prices = ' '.join(regex(r'[\d]+\s?zł', text))
        print(f'{price} zł')
        print(text, '\n', other_prices, '\n', link)
        con.execute(f'''INSERT INTO flats VALUES (?,?,?,?);''', (link, text, int(price), other_prices))
        con.commit()


def main():
    # Make URLs for 10 pages
    urls = [url + str(nr) for nr in range(1, 11)]  # First 10 pages
    for link in urls:
        html_link, _ = soup_find(link, tag='a', class_html=['marginright5 link linkWithHash detailsLinkPromoted',
                                                            'marginright5 link linkWithHash detailsLink'])
        links = web_links(html_link)  # List of links
        search_offer(links)


main()
con.close()
