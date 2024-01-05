'''
This file builds upon another allrecipe scraper to extract the review frequencies on the page.

The orignial scrapper can be found here: https://github.com/sudhanvalalit/ML_projects/blob/master/all_recipes/allRecipesScraper.py

This project modifies on the previous scraper by adding the following features: 
1. Reads from a CSV list 
2. Scrapes each allrecipe link in CSV list 
3. Creates a new CSV of the original CSV list with review frequencies for each allrecipe page

'''
import urllib.request
import urllib.parse
import re
from bs4 import BeautifulSoup
import requests

import random

import soupsieve as sv # use soupsieve directly

import pandas as pd
import time

import os

headers_browser = {'Connection': 'close',"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
"Accept-Encoding": "gzip","Accept-Language": "en-US,en;q=0.9,es;q=0.8", "Upgrade-Insecure-Requests": "1","User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"}


urlsDataFrame = pd.read_csv('urls.csv')
# urls = urls.head() # uncomment to restrict to 5 lines of urls
urls = urlsDataFrame.values.tolist()

# print('number of urls', len(urlsDataFrame), 'typeof', type(urlsDataFrame))
cookieFile = "starReviewFrequenciesOfPeanutButterCookieRecipes.csv"
failedCookieFile = "cookieRecipesWithoutReviews.csv"

def deleteFile(fileName):
    if os.path.exists(fileName):
        os.remove(fileName)
        print("Successfully! The File has been removed")
    else:
        print("Can not delete the file as it doesn't exists")

deleteFile(cookieFile)
fileStream = open(cookieFile, "a")
deleteFile(failedCookieFile)
fileStreamFailedUrls = open(failedCookieFile, "a")

class Scraper:
    links = []
    names = []

    def __init__(self, query_dict):
        self.query_dict = query_dict

    def get_url(self, link):
        # url = requests.get(url).text
        for i in range(10): # loop the try-part (i.e. opening the link) until it works, but only try it 4 times at most#
            try: #try the following:#
                # random_sleep_link = random.uniform(10, 15) #sleep for a random chosen amount of seconds between 10 and 15 seconds#
                # time.sleep(random_sleep_link)
                url = requests.get(link,headers= headers_browser) #access the URL using the header settings defined earlier#
                print('url', link)
            except requests.exceptions.RequestException as e: #if anything weird happens...#
                print('e', e)
                random_sleep_except = random.uniform(60,120)
                print("I've encountered an error! I'll pause for"+str(random_sleep_except/60) + " minutes and try again \n")
                time.sleep(random_sleep_except) #sleep the script for x seconds and....#
                continue #...start the loop again from the beginning#
            else: #if the try-part works...#
                break #...break out of the loop#
        else: #if x amount of retries on the try-part don't work...#
            fileStreamFailedUrls.write(link + ' Failed to get\n')
            raise Exception("Something really went wrong here... I'm sorry.") #...raise an exception and stop the script#
            # if the script survived this part...#
        self.soup = BeautifulSoup(url.text, 'lxml')
            # bsObj = BeautifulSoup(url.text,"lxml") #this means we're good to go and can parse the page into BeautifulSoup!#

    def print_info(self):
        # self.links = '\n'.split(urls)
        self.get_data()
        return

    def get_data(self):
        self.ingredientsList = []
        self.instructionsList = []
        for i, [link] in enumerate(urls):
            print('current item is index', i, 'link is:', link)
            self.get_url(link)

            # Grab rating count total
            if not self.soup.find('div', class_="recipeRatingsList"):
                fileStreamFailedUrls.write(link + ' No reviews list\n')
                continue
            else:
                print('found recipeRatingsList!')
            ratingCount = self.soup.select('.recipeRatingsList .recipeRatingsList__count')[0]
            ratingCountStr = ratingCount.string
            ratingCountNum = ratingCountStr.split(' ')[0]

            ratingCountRowUl = self.soup.select('.recipeRatingsList ul')[0]
            # Attempt to use sv to extract li from the ul
            # quickSoup = BeautifulSoup(ratingCountRowUl)
            bsRatingLines = sv.select('li', ratingCountRowUl)
            starFrequencies = [link]
            for bsRatingLine in bsRatingLines:
                bsRating = sv.select('.rating-stars', bsRatingLine)[0]
                bsRatingCount = sv.select('.rating-count', bsRatingLine)[0]

                textOfRating = bsRating.get_text()
                textOfRatingCount = bsRatingCount.get_text().strip()

                starNumStr = textOfRating.split(' ')[0].strip()
                starFrequencies.append(textOfRatingCount)
            starFrequencies.append(ratingCountNum)
            result = ','.join(starFrequencies)
            fileStream.write(result + '\n')
        fileStream.close()
        fileStreamFailedUrls.close()
def main():
    recipeName = "peanut butter cookie"
    ingIncl = ""
    ingExcl = ""
    query_dict = {
        "search": recipeName,     # Query keywords
        # 'Must be included' ingrdients (optional)
        "ingIncl": ingIncl,
        # 'Must not be included' ingredients (optional)
        "ingExcl": ingExcl,
        # Sorting options : 're' for relevance,\
        #  'ra' for rating, 'p' for popular (optional)
        "sort": "re"
    }
    scrap = Scraper(query_dict)
    scrap.print_info()

if __name__ == '__main__':
    main()