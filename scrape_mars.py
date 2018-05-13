# Dependencies
import os
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import time
import random

#failsafe
from splinter.exceptions import ElementDoesNotExist

# Create a Beautiful Soup object & load chromedriver
def init_browser():
    executable_path = {'executable_path': 'chromedriver'}
    return Browser('chrome', **executable_path, headless=True)

def scrape():
    # creating variables for all URL's needed 
    nasa_url= 'https://mars.nasa.gov/news/'
    nasa_jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    mars_twitter_url = 'https://twitter.com/marswxreport?lang=en'
    space_facts_url = 'http://space-facts.com/mars/'
    astrogeology_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    #creating empty Mars Dictionary
    mars = {}
    browser = init_browser()
    #NASA Mars news url
    browser.visit(nasa_url)
    news_title = browser.find_by_css('.content_title').first.text
    news_p = browser.find_by_css('.article_teaser_body').first.text
    print(news_title, "\n" + news_p)
    
    #Featured Image
    browser.visit(nasa_jpl_url)
    browser.find_by_id('full_image').click()
    featured_image_url = browser.find_by_css('.fancybox-image').first['src']
    print(featured_image_url)
    

	#Get tweet from Mars weather Twitter account
    browser.visit(mars_twitter_url)
    for text in browser.find_by_css('.tweet-text'):
        if text.text.partition(' ')[0] == 'Sol':
            mars_weather = text.text
            break
    print(mars_weather)

    #Scrape for Mars trivia/facts
    

    #convert to df for converting to html table
    mars_df=  pd.read_html (space_facts_url, attrs = {'id': 'tablepress-mars'})[0]
    mars_df = mars_df.set_index(0).rename(columns={1:"value"})
    del mars_df.index.name
    mars_df=mars_df.rename(columns = {'value':""})
    mars_facts = mars_df.to_html()
    print(mars_facts) #- in html form to put in the webpage later
    mars_df
    #Grab Mars hemispheres photos
    browser.visit(astrogeology_url)

    mars_pic_1 = browser.find_by_tag('h3')[0].text
    mars_pic_2 = browser.find_by_tag('h3')[1].text
    mars_pic_3 = browser.find_by_tag('h3')[2].text
    mars_pic_4 = browser.find_by_tag('h3')[3].text

    browser.find_by_css('.thumb')[0].click()
    first_img = browser.find_by_text('Sample')['href']
    browser.back()

    browser.find_by_css('.thumb')[1].click()
    second_img = browser.find_by_text('Sample')['href']
    browser.back()

    browser.find_by_css('.thumb')[2].click()
    third_img = browser.find_by_text('Sample')['href']
    browser.back()

    browser.find_by_css('.thumb')[3].click()
    fourth_img = browser.find_by_text('Sample')['href']

    hemisphere_image_urls = [
    {'title': mars_pic_1, 'img_url': first_img},
    {'title': mars_pic_2, 'img_url': second_img},
    {'title': mars_pic_3, 'img_url': third_img},
    {'title': mars_pic_4, 'img_url': fourth_img}
    ]

    print(hemisphere_image_urls)

    #set up dictionary for flask
    mars['headline'] = news_title
    mars['paragraph_text'] = news_p
    mars['featured_image'] = featured_image_url
    mars['weather'] = mars_weather
    mars['facts'] = mars_facts
    mars['hemispheres'] = hemisphere_image_urls

    return mars