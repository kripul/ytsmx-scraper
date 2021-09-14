import csv
import requests
from time import sleep
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent().random

page_start = input('Start page : ')
last_page = input('Last page : ')

torrent_720 = None
torrent_1080 = None

csv_file = open('page'+page_start+'to'+last_page+'movie_list.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['MOVIES', 'YEAR', 'GENRE','IMDB-RATING', 'DURATIONS', 'IMAGE','SCREENSHOT','TRAILER','SYNOPSIS','720p torrent','1080p torrent'])

def scrape(url):
    headers = {
        'user-agent': ua,
    }
    print("Scraping %s"%url)
    r = requests.get(url, headers=headers)
    return r.content

def parse():

    global torrent_1080
    global torrent_720
    for page in range(int(page_start), int(last_page)):
        url_page = 'https://yts.mx/browse-movies?page='+str(page)
        r_page = scrape(url_page)
        soup_p = BeautifulSoup(r_page, 'html.parser')
        movie_links = soup_p.findAll('div', class_='browse-movie-bottom' )
        for link in movie_links:
            link = link.find('a', href=True)

            data = scrape(link['href'])
            soup = BeautifulSoup(data, 'html.parser')

            try:
                title = soup.find('h1').text
                year = soup.findAll('h2')[0].text
                genre = soup.findAll('h2')[1].text
                torrent_links = soup.find('p', class_='hidden-xs hidden-sm')
                for torrent in torrent_links.findAll('a'):
                    if (torrent.text[:3] == "720"):
                        torrent_720 = torrent['href']
                    if (torrent.text[:4] == "1080"):
                        torrent_1080 = torrent['href']
                synopsis = soup.find('p', class_='hidden-sm hidden-md hidden-lg')
                sysnopsistext = synopsis.text
                artists = []
                artist = soup.findAll('span', itemprop='name')
                for i in artist:
                    artists.append(i.string)
                trailer = soup.find('a', class_='youtube cboxElement')
                trailerhref = trailer['href']
                screenshot = []
                screenshots = soup.findAll('a', class_='screenshot-group imghov cboxElement')
                for i in screenshots:
                    screenshot.append(i['href'])
                img = soup.find('img', itemprop='image')
                imgsrc = img['src']
                imdbrating = soup.find('span', itemprop='ratingValue')
                imdb = imdbrating.text
                duration = soup.findAll('div', class_='tech-spec-element col-xs-20 col-sm-10 col-md-5')[6].text

            except:
                title = None
                year = None
                genre = None
                imdbrating = None
                duration = None
                img = None
                screenshot = None
                trailer = None
                torrent_720 = None
                torrent_1080 = None

            csv_writer.writerow(
                [title, year, genre, imdb,
                 duration, imgsrc, screenshot, trailerhref, sysnopsistext,
                 torrent_720, torrent_1080])
parse()