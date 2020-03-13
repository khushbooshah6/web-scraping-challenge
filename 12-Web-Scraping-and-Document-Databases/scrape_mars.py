import pandas as pd
from bs4 import BeautifulSoup as bs
import splinter as sp
from splinter import Browser
from bs4 import BeautifulSoup
import os
import time
import datetime as dt


executable_path = {"executable_path": "/usr/local/Caskroom/chromedriver/80.0.3987.106/chromedriver"}
browser = Browser("chrome", **executable_path, headless=False)

class scrape():

    def getsoup(url,sleep):
        browser.visit(url)
        time.sleep(int(sleep))
        html=browser.html
        soup = bs(html, "html.parser")
        return soup

    def marsnews():
        nasa_url = "https://mars.nasa.gov/news/"
        soup = scrape.getsoup(nasa_url,"10")
        ntitle=""
        ncontent=""
        try:
            ntitle=soup.find('div', class_='content_title').text
            ncontent=soup.find('div', class_='article_teaser_body').text

            titlenews=[]
            All_Titles_Collection = soup.find_all("div", class_='list_text')
            for T in Titles_Collection:
                SepDIV=T.find_all('div', class_='content_title')
                for S in SepDIV:
                    titlenews.append(S.a.text)


            contentnews=[]
            All_Content_Collection = soup.find_all("div", class_='article_teaser_body')
            for T in All_Titles_Collection:
                Sep_div=T.find_all("div", class_='article_teaser_body')
                for S in Sep_div:
                    contentnews.append(S.text)
            output=[titlenews,contentnews]
        except NameError:
            print(NameError)
        return ntitle,ncontent

    def mars_image():
        Mars_Image_URL="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
        msoup = scrape.getsoup(Mars_Image_URL,"2")
        Image_URL = msoup.find("img", class_="thumb")["src"]
        featured_url = "https://www.jpl.nasa.gov" + Image_URL
        return featured_url

    def twitter_url():
        twitter_url = 'https://twitter.com/marswxreport?lang=en'
        tsoup = scrape.getsoup(twitter_url,"5")
        allspan = tsoup.body.find_all('span')

        mars_weather=""
        for tweet in allspan:
            mars_weathertweet = tweet.text
            if 'sol' and 'pressure' in mars_weathertweet:
                mars_weather=mars_weathertweet
                return mars_weather
                break
            else:
                pass
        return mars_weather

    def mars_facts():
        mars_facts="https://space-facts.com/mars"
        browser.visit(mars_facts)
        tables=pd.read_html(mars_facts)
        mars_data = pd.DataFrame(tables[0])
        mars_facts = mars_data.to_html(header = False, index = False)
        return mars_facts

    def mars_hemisphere():
        mars_image="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        mh_soup = scrape.getsoup(mars_image,"3")
        hemisphere_image_urls = []

        result = mh_soup.find("div", class_ = "result-list" )
        hemispheres = result.find_all("div", class_="item")


        for h in hemispheres:
            title= h.h3.text.replace("Enhanced","")
            subpage="https://astrogeology.usgs.gov" + h.a["href"]
            subbrowser = Browser("chrome", **executable_path, headless=False)
            subbrowser.visit(subpage)
            time.sleep(3)
            subhtml=subbrowser.html
            subsoup=bs(subhtml,"html5lib")
            getdownloads=subsoup.find('div',class_='downloads')
            fullimage=getdownloads.find("a")["href"]
            hemisphere_image_urls.append({"title":title,"img_url":fullimage})
            subbrowser.quit()
        return hemisphere_image_urls

    def scrape_data():
        mars_news=scrape.marsnews()
        all_data = {
            'titlenews' :  mars_news[0],
            'contentnews' :  mars_news[1],
            'featured_url' : scrape.mars_image(),
            'mars_weather' : scrape.twitter_url(),
            'mars_facts' : scrape.mars_facts(),
            'hemisphere_image_urls' : scrape.mars_hemisphere(),
            'timestamp' : dt.datetime.now()
            }
        browser.quit()
        return all_data
