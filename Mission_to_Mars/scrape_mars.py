import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import requests

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    mars = {}
    #Mars News
    url = 'https://mars.nasa.gov/news/?page=0'
    html = requests.get(url)

    soup = BeautifulSoup(html.text, 'html.parser')

    title_results = soup.find('div', class_='content_title')
    title_results

    title = title_results.find('a')
    news_title = title.string.strip()
    news_title

    para_results = soup.find('div',class_='rollover_description_inner')
    para_results

    news_p = para_results.string.strip()
    news_p

    #Featured Image
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    
    browser = init_browser()

    browser.visit(image_url)

    target = 'a[class="button fancybox"]'
    browser.find_by_tag(target).click()

    browser.find_link_by_partial_text('more info').click()

    html2 = requests.get(browser.url)
    browser.quit()

    soup2 = BeautifulSoup(html2.text,'html.parser')

    img = soup2.find('figure', class_='lede')
    img_link = img.find('a')['href']
    final_img = f'https://www.jpl.nasa.gov{img_link}'

    #Mars Facts
    table_url='https://space-facts.com/mars/'

    table = pd.read_html(table_url)

    df = pd.DataFrame(table[0])

    html_table = df.to_html()

    #Mars Hemispheres
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    html3 = requests.get(hemisphere_url)

    hem_soup = BeautifulSoup(html3.text,'html.parser')

    hem_results = hem_soup.find_all('div', class_='item')

    hemisphere_image_urls = []


    for hem_result in hem_results:
    
        hem_items = {}

        #create the link to access each hemisphere image's page:
        base_url = 'https://astrogeology.usgs.gov'
        link = hem_result.find('a')['href']
        hem_url = f'{base_url}{link}'
    
        #open a browser using Splinter and then go to the page containing the full image and title, store       the browser information to be used in Beautiful Soup and the close the browser:
        browser2 = init_browser()
    
        browser2.visit(hem_url)
        browser2.find_link_by_partial_text('Open').click()
        html4 = requests.get(browser2.url)
        browser2.quit()

        soup3 = BeautifulSoup(html4.text,'html.parser')
        
        #find the title from the html, strip it to clean the tags and then split to remove the text after       the pipe:
        h_title = soup3.find('title')
        hem_title = h_title.string.strip()
        hemisphere_title = hem_title.split(' |')[0]
        hemisphere_title

        #the first item in the list contains the link to the full size image:
        h_li = soup3.find('li')
        hem_li = h_li.a['href']
        hem_li

        #add the title and img_url dictionary to the list of urls:
        hem_items = {'title': hemisphere_title, 'img_url': hem_li} 
        hemisphere_image_urls.append(hem_items)

    #update the dictionary with the items scraped and return it for use in app.py
    mars["news_title"] = news_title
    mars["paragraph"] = news_p
    mars["image"] = final_img
    mars["table"] = html_table
    mars["mars_hemispheres"] = hemisphere_image_urls

    return mars 