# NASA-Mars-Webscrape

# Mission to Mars

   
   For the Web Scraping Challenge, we were tasked with scraping certain elements from several Mars-related web pages, and
   displaying them on a web page of our creation.
   
   This functionality uses flask and jinja to display a web landing page.  Before the landing page is displayed, the
   script reads a mongo database to retrieve and saved Mars data and displays it on the page.  On the landing page is a button,
   when clicked, that calls a scrape function to scrape the Mars web pages for current data.  The data is then written to
   the mongo database, and the landing page is rendered with the updated data.
   
   Screenshots were taken of the resultant web page.
   
   
  Missions_to_Mars/
   app.py - Flask script that uses Jinja to display an HTML template.
   scrape_mars.py - scraping function which uses Splinter to extract data from the Mars-related web pages.
   mission_to_mars.ipynb - jupyter notebook used to develop and debgug scraping function.
   
  Mission_to_Mars/templates/
      index.html - HTML template used to format Mars data scraped from the web.
      
      
  ![image](/Missions_to_Mars/screenshots/mission_to_mars_scrnshot4.png)
      
  Missions_to_Mars/screenshots/
      mission_to_mars_scrshot1.png - screenshot of resultant web page
      mission_to_mars_scrshot2.png - screenshot of resultant web page
      mission_to_mars_scrshot3.png - screenshot of resultant web page
      mission_to_mars_scrshot4.png - screenshot of resultant web page
   
