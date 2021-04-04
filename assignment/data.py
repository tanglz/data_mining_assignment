import json
import re
from urllib.parse import urlparse

import certifi
import requests
import urllib3
from bs4 import BeautifulSoup


def collect_data(outfile):
    resource = "https://www.dailyscript.com/movie.html"
    movie_page = requests.get(resource)
    soup = BeautifulSoup(movie_page.content, features="html.parser")
    items = soup.findAll("p")
    meta_list = []
    for item in items:
        a_list = item.findAll("a")
        if len(a_list) == 2:
            screenplay_href = a_list[0].get('href')
            screenplay_url = get_screen_play_url(screenplay_href)
            if len(screenplay_url) > 0 and a_list[1].text == 'imdb':
                imdb_href = a_list[1].get('href')
                imdb_id = get_imdb_id(imdb_href)
                if len(imdb_id) > 0:
                    meta = get_meta_info(imdb_id)
                    meta.update({"screenplay_url": screenplay_url})
                    meta_list.append(meta)
    with open(outfile, 'w') as outfile:
        json.dump(meta_list, outfile)
    return


def get_screen_play_url(href):
    domain = "https://www.dailyscript.com/"
    if href.endswith('.txt'):
        return domain + href
    else:
        return ""


def get_meta_info(imdb_id):
    url = "https://www.imdb.com/title/" + imdb_id
    page = requests.get(url)
    soup = BeautifulSoup(page.content, features="html.parser")
    title_block = soup.find('div', {'class': 'title_block'})
    title = title_block.find('h1').text
    meta = {'title': title, 'imdb_id': imdb_id}
    cast_list = soup.find('table', {'class': 'cast_list'})
    character_list = cast_list.findAll('td', {'class': 'character'})
    character_name_list = []
    # top 5 characters
    i = 0
    for character in character_list:
        if i >= 5:
            break
        character_name = character.find('a').text
        character_name_list.append(character_name)
        i = i + 1
    meta.update({'character_name_list': character_name_list})
    # # genres
    titleStoryLine = soup.find('div', {'id': 'titleStoryLine'})
    more = titleStoryLine.findAll('div', {'class': 'see-more'})
    genres_div = more.__getitem__(1)
    a_list = genres_div.findAll('a')
    genres = list()
    for a in a_list:
        genres.append(a.text)
    meta.update({'genres':genres})
    return meta


def get_imdb_id(url):
    imdb_id = re.search('/ev\d{7}\/\d{4}(-\d)?|(tt)\d{7}/', url)
    if imdb_id:
        imdb_id = imdb_id.group(0).strip('/')
        return imdb_id
    return ''


def batch_download(filename):
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
        for item in data:
            title = item['title']
            url = item['screenplay_url']
            download(title, url)
    return True


def download(title, url):
    url_obj = urlparse(url)
    path = url_obj.path.lower()
    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where()
    )
    resp = http.request('GET', url)
    suffix = ".txt"
    file = open("scripts/" + title + suffix, 'wb')
    file.write(resp.data)
