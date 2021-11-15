""" scrap books database """
from bs4 import BeautifulSoup
import requests

#import pymongo
# from pymongo import MongoClient
# from dotenv import load_dotenv
# load_dotenv()

# mongoURI = os.getenv('mongoURI')
# cluster = MongoClient(mongoURI)

from mongo_connection import mongodb_conn

cluster = mongodb_conn()
db = cluster['MoviesAndTVTracker']
collection = db['basedOnBook']

#iterate through these params on based url
params = ['0-9', 'a', 'b', 'c', 'd', 'e', 'f', 'h', 'i',
 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'x', 'y','z']

def format_media_title(title):
    title = title.replace('Find It', '').replace('Buy it on Amazon', '').replace("Check The Catalog", '').replace('(', '').replace(')', '').replace('series', '').strip()
    if', The'  in title:
        title = title.replace(', The', '')
        title = f'The {title}'
        return title
    if', An'  in title:
        title = title.replace(', An', '')
        title = f'An {title}'
        return title
    if', A'  in title:
        title = title.replace(', A', '')
        title = f'A {title}'
        return title
    return title

def format_book_info(book):
    name = format_media_title(book)
    all_info_array = name.split('/')
    return all_info_array

def getInfo():
    for param in params:
        page = requests.get(f'https://apps.mymcpl.org/botb/movie/browse/{param}')
        soup = BeautifulSoup(page.text, 'html.parser')
        movies = soup.find_all('td', class_='views-field-title-4')
        for movie in movies:
            media_type = ''
            if'series' in movie.getText():
                media_type = 'Tv'
            else:
                media_type = 'Movie'

            movie_name = format_media_title(movie.getText())
            release_year =  list(map(int, filter(str.isdigit, movie_name.split())))[-1]
            movie_name = movie_name.replace(str(release_year), '')

            book_info = movie.find_next_sibling("td")
            amazon_link = book_info.find_all('li')[-1].a.get('href')
            book_name = format_book_info(book_info.getText())[0]
            book_author = format_book_info(book_info.getText())[-1].strip()
            #print(movie_name, release_year, book_name, book_author)
            #save to database and check that it does not exist first

            found = collection.find_one({"movie_name": movie_name, "year": release_year, "book_autor": book_author})
            if(not found):
                book = {
                'movie_name': movie_name,
                'year': release_year,
                "media_type": media_type,
                "book_name": book_name,
                "book_author": book_author,
                "amazon_link": amazon_link
                }
                collection.insert_one(book)

getInfo()
