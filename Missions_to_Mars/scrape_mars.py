from bs4 import BeautifulSoup
import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

# Setup splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# URL of page to be scraped
latest_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&year=2021%3Apublish_date&category=19%2C165%2C184%2C204&blank_scope=Latest"
browser.visit(latest_url)

html = browser.html
soup = BeautifulSoup(html, 'html.parser')

latest_soup = soup.find_all("div", class_="content_title")
news_title = latest_soup[1].text
print(news_title)

teaser_soup = soup.find_all("div", class_="article_teaser_body")
news_p = teaser_soup[0].text
print(news_p)

feat_img_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
browser.visit(feat_img_url)

html = browser.html
soup = BeautifulSoup(html, "html.parser")

img_soup = soup.find_all("a", class_="showimg")

picfile = img_soup[0]["href"]

featured_image_url = feat_img_url.replace("index.html", picfile)
print(featured_image_url)

tbl_url = "https://space-facts.com/mars/"
tables = pd.read_html(tbl_url)
mars_df = tables[0]
mars_df

mars_df = mars_df.rename(columns={0: "Aspect", 1: "Measurement"})
mars_df

mars_tbl_str = mars_df.to_html()
mars_tbl_str

hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(hemisphere_url)

html = browser.html
soup = BeautifulSoup(html, "html.parser")

hemisphere_soup = soup.find_all("div", class_="description")

hemi_titles = []

for item in hemisphere_soup:
    temp_name = item.text.split("/")
    hemi_name = temp_name[0].replace(" Enhancedimage", "")
    hemi_titles.append(hemi_name)
    
print(hemi_titles)

base_url = "https://astrogeology.usgs.gov"
hemi_img = []

hemi_url_list = ["https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced",
                "https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced",
                "https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced",
                "https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced"]

for url in hemi_url_list:
    browser.visit(url)
    
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    
    hemi_soup = soup.find("img", class_="wide-image")   
    
    hemi_img.append(base_url + hemi_soup["src"])
    
    
print(hemi_img)

hemisphere_image_urls = []

for i in range(0, len(hemi_titles)):
    hemisphere_image_urls.append({"title": hemi_titles[i], "img_url": hemi_img[i]})
    
hemisphere_image_urls