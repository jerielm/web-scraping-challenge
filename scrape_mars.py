from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests
import pymongo
from webdriver_manager.chrome import ChromeDriverManager


def scrape(): 

    #NASA - MARS NEWS######################
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_title = soup.find('div', class_='content_title').text
    paragraph_text = soup.find('div', class_= 'article_teaser_body').text



    #JPL MARS IMAGES#############
    image_url ='https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(image_url)
    jpl_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'
    html= browser.html
    soup = BeautifulSoup(html,'html.parser')

    featured_image_url = soup.find('img', class_ = 'headerimage fade-in')['src']
    full_url = jpl_url + featured_image_url
    print(jpl_url + featured_image_url)




    #MARS FACTS ############
    facts_url = 'https://space-facts.com/mars/'
    mars_facts = pd.read_html(facts_url)
    mars_df = mars_facts[0]
    mars_df.columns = ['Description', 'Value']
    mars_df

    mars_string = mars_df.to_html(index=False, header= False)
    mars_string


    #MARS HEMISPHERES
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hemi_main_url = 'https://astrogeology.usgs.gov'
    browser.visit(hemi_url)

    html = browser.html
    soup = BeautifulSoup(html,'html.parser')

    items = soup.find_all('div',class_ = 'item')
    hemisphere_image_urls = []

    for i in items:
        title = i.find('h3').text
        hemi_href_url = i.find('a', class_='itemLink product-item')['href']
        #print(hemi_main_url + hemi_href_url)
        browser.visit(hemi_main_url + hemi_href_url)
        img_html = browser.html
        soup = BeautifulSoup(img_html, 'html.parser')
        img_url = hemi_main_url + soup.find('img', class_='wide-image')['src']
        hemisphere_image_urls.append({'title' : title, 'img_url':img_url})
        
    hemisphere_image_urls


    scrapeoutput = {
        "news_title": news_title,
        "paragraph_text": paragraph_text,
        "full_url": full_url,
        "mars_string":mars_string,
        "hemisphere_image_urls": hemisphere_image_urls
        }



    return scrapeoutput