
# import dependancies
import time
import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser

def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=True)

def scrape ():
 #Scrapes various websites for information about Mars, and returns data in a dictionary
    browser = init_browser()
    mars_data = {}

    # visit the NASA Mars News site and scrape headlines
    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)
    time.sleep(1)
    nasa_html = browser.html
    nasa_soup = BeautifulSoup(nasa_html, 'html.parser')

    news_list = nasa_soup.find('ul', class_='item_list')
    first_item = news_list.find('li', class_='slide')
    nasa_headline = first_item.find('div', class_='content_title').text
    nasa_teaser = first_item.find('div', class_='article_teaser_body').text
    mars_data["nasa_headline"] = nasa_headline
    mars_data["nasa_teaser"] = nasa_teaser

    # visit the JPL website and scrape the featured image
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    time.sleep(1)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(1)
    try:
        expand = browser.find_by_css('a.fancybox-expand')
        expand.click()
        time.sleep(1)

        jpl_html = browser.html
        jpl_soup = BeautifulSoup(jpl_html, 'html.parser')

        img_relative = jpl_soup.find('img', class_='fancybox-image')['src']
        image_path = f'https://www.jpl.nasa.gov{img_relative}'
        mars_data["feature_image_src"] = image_path
    except ElementNotVisibleException:
        image_path = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA22076_hires.jpg'
        mars_data["feature_image_src"] = image_path



# visit mars weather report twitter and scrape the latest tweet
    mars_weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(mars_weather_url)
    time.sleep(1)
    mars_weather_html = browser.html
    mars_weather_soup = BeautifulSoup(mars_weather_html,'html.parser')

#    latest_tweet = mars_weather_soup.find('div', class_='tweet')
    latest_tweet = mars_weather_soup.find('ol', class_='stream-items')
    latest_tweet_text = latest_tweet.find('p',class_ = "tweet-text").text
    mars_data["weather_summary"] = latest_tweet_text

# Visit space facts and scrape the Mars fact table
    mars_facts_url = 'https://space-facts.com/mars/'
    browser.visit(mars_facts_url)
    time.sleep(1)

    mars_facts_html = browser.html
    mars_facts_soup = BeautifulSoup(mars_facts_html,'html.parser')
    facts_table = mars_facts_soup.find('table', class_ ='tablepress tablepress-id-mars')

    column1 = facts_table.find_all('td', class_ = 'column-1')
    column2 = facts_table.find_all('td', class_ ='column-2')

    facets = []
    values = []

    for row in column1:
        facet = row.text.strip()
        facets.append(facet)

    for row in column2:
        value = row.text.strip()
        values.append(value)

        # Creating df
    mars_facts = pd.Dataframe({"Parameters":facets, "Value":values})
    mars_facts_html = mars_facts.to_html(header = False, index = False)
    mars_data["fact_table"] = mars_facts_html

    # Visiting and scraping hemsiphere images of Mars from USGS site
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hemi_dicts = []

    for i in range(1,9,2):
        hemi_dict = {}

        browser.visit(hemi_url)
        hemi_html = browser.html
        hemi_soup = BeautifulSoup(hemi_html,'html.parser')
        hemi_name_links = hemi_soup.find_all('a', class_ ='product-item')
        hemi_name = hemi_name_links[i].text.strip('Enhanced')
        detail_links = browser.find_by_css('a.product-item')
        detail_links[i].click()
        time.sleep(1)
        browser.find_link_by_text('Sample').first.click()
        time.sleep(1)
        browser.windows.current = browser.wondows[-1]
        hemi_img_html = browser.html

        browser.windows.curret = browser.windows[0]
        browser.windows[-1].close()

        hemi_img_soup = BeautifulSoup(hemi_img_html,'html.parser')
        hemi_img_path = hemi_img_soup.find('img')['src']
        hemi_dict['title'] = hemi_name.strip()
        hemi_dict['img_url'] = hemi_img_path
        hemi_dicts.append(hem_dict)

    mars_data["hemisphere_images"] = hemi_dicts

    browser.quit()

    return mars_data
