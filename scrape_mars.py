# Scraping Mars Web Data

# Dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
import time

def scrape():
    # Set up path and browser
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)


    # NASA Mars News Site
    # Pulls latest news title and paragraph text
    # Source: https://mars.nasa.gov/news/

    # Define URL
    news_url = 'https://mars.nasa.gov/news/'

    # Visit url and retrieve html
    browser.visit(news_url)
    time.sleep(1)
    news_html = browser.html
    time.sleep(1)
    soup = BeautifulSoup(news_html, 'html.parser')

    # Pull first news headline and description
    news_title = soup.find('div', class_='bottom_gradient').find('h3').text
    news_p = soup.find('div', class_='article_teaser_body').text

    # JPL Mars Space Images
    # Pulls URL for featured Mars image (full size jpg image)
    # Source: https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars

    # Set up url
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    # Navigate to website 
    browser.visit(jpl_url)
    time.sleep(1)

    # Navigate to featured image
    browser.links.find_by_partial_text('FULL IMAGE').click()
    time.sleep(1)

    # Navigate to page that has full-sized image
    browser.links.find_by_partial_text('more info').click()
    time.sleep(1)

    # Pull html and store image url
    jpl_html = browser.html
    soup = BeautifulSoup(jpl_html, 'html.parser')
    image_url = soup.find('img', class_='main_image')['src']
    featured_image_url = 'https://www.jpl.nasa.gov' + image_url

    # Mars Facts
    # Pulls table containing facts about the planet
    # Source: https://space-facts.com/mars/

    # Scrape tables from webpage using Pandas
    facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(facts_url)
    mars_facts = tables[0].rename(columns={0: '', 1: ' '}).set_index('')

    # Use Pandas to convert to HTML table string
    mars_facts_html = mars_facts.to_html()

    # Mars Hemispheres
    # Pulls high resolution images of each of Mar's hemispheres
    # * Source: https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars

    # Set up url
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # List of hemispheres
    hemispheres = ['Valles Marineris Hemisphere', 'Cerberus Hemisphere', 'Schiaparelli Hemisphere', 'Syrtis Major Hemisphere']

    # Empty list to store image urls
    hemisphere_image_urls = []

    # Open up webpage
    browser.visit(hemi_url)

    # For each hemisphere, pull image url and store with associated hemisphere name
    for hemi in hemispheres: 
        hemi_dict = {}
        try:
            # Click on hemisphere link
            browser.links.find_by_partial_text(hemi).click()
            time.sleep(1)
            # Click on 'Open' to get to full image stored on page
            browser.links.find_by_partial_text('Open').click()
            time.sleep(1)
            
            # Pull html
            hemi_html = browser.html
            soup = BeautifulSoup(hemi_html, 'html.parser')
            
            # Pull full-sized image url
            image_url = soup.find('img', class_='wide-image')['src']
            
            # Go back to main page
            browser.back()
            
            # Store image link in dictionary and append to list
            full_image_url = 'https://astrogeology.usgs.gov' + image_url
            hemi_dict['title'] = hemi
            hemi_dict['img_url'] = full_image_url
            hemisphere_image_urls.append(hemi_dict)
        except:
            print('Webpage not found')

    browser.quit()

    # Store all scraped data in one dictionary
    mars_data = {
        'news_t': news_title,
        'news_p': news_p,
        'feat_img_url': featured_image_url,
        'mars_facts_table': mars_facts_html,
        'hemi_img_urls': hemisphere_image_urls
    }

    return mars_data