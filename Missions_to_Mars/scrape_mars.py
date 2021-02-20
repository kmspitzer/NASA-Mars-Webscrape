from bs4 import BeautifulSoup
import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager



#########################################
# function initializes splinter browser #
#########################################
def init_browser():
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


#############################################################
# func make_soup() scrapes page based on tag and class name #
#############################################################
def make_soup(url, tag, class_name):
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    return soup.find_all(tag, class_=class_name)


##################################################
# function steps through mars pages, scrapes and #
# populates a resultant dictionary               #
##################################################
def scrape():

    # initialize the browser #
    browser = init_browser()

    # create empty dictionary #
    mars_dict = {}

    # set url for NASA Mars News Site #
    latest_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&year=2021%3Apublish_date&category=19%2C165%2C184%2C204&blank_scope=Latest"
    
    # scrape page, pull latest news title, and add to dictionary #
    mysoup = make_soup(latest_url, "div", "content_title")
    mars_dict["news_title"] = mysoup[1].text

    # scrape same page again, pull news paragraph, and add to dictionary #
    mysoup = make_soup(latest_url, "div", "article_teaser_body")
    mars_dict["news_p"] = mysoup[0].text



    # set url for JPL Featured Space Image #
    feat_img_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"

    # scrape page, concatenate full size image path to base url, #
    # and add to dictionary                                      #
    mysoup = make_soup(feat_img_url, "a", "showimg")
    img_path = mysoup[0]["href"]
    mars_dict["featured_image_url"] = feat_img_url.replace("index.html", img_path)


    # set url for USGS Astrogeology page #
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    # scrape page #
    mysoup = make_soup(hemisphere_url, "div", "description")

    # create empty list for hemisphere titles #
    hemi_titles = []

    # loop through scraped results, render portion of results that we #
    # need, and append to list of hemisphere titles                   #
    for item in mysoup:
        temp_name = item.text.split("/")
        hemi_name = temp_name[0].replace(" Enhancedimage", "")
        hemi_titles.append(hemi_name)


    # set image base url #
    base_url = "https://astrogeology.usgs.gov"

    # create empty list for hemisphere images #
    hemi_img = []

    # set list of hemisphere image pages #
    hemi_url_list = ["https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced",
                "https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced",
                "https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced",
                "https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced"]

    
    # loop through list of hemisphere image urls #
    for hemi in hemi_url_list:
        # scrape page, pull image path, concatenate to base url, #
        # and add to list of hemisphere images                   #
        mysoup = make_soup(hemi, "img", "wide-image")
        hemi_img.append(base_url + mysoup["src"])
    
    
    # create empty list for hemisphere dictionaries #
    hemisphere_image_urls = []

    # loop through each hemisphere #
    for i in range(0, len(hemi_titles)):
        # add hemisphere dictionary to list #
        hemisphere_image_urls.append({"title": hemi_titles[i], "img_url": hemi_img[i]})
    
    # add hemisphere dictionary to resultant mars data dictionary #
    mars_dict["hemisphere_image_urls"] = hemisphere_image_urls

    # set Mars Facts url #
    tbl_url = "https://space-facts.com/mars/"

    # scrape page for table and read into dataframe #
    tables = pd.read_html(tbl_url)
    mars_df = tables[0]

    # rename columns #
    mars_df = mars_df.rename(columns={0: "Aspect", 1: "Measurement"})

    # convert dataframe to an HTML string #
    mars_tbl_str = mars_df.to_html()

    # add table to mar dictionary #
    mars_dict["mars_data_tbl"] = mars_tbl_str

    # return dictionary to calling function #
    return mars_dict

