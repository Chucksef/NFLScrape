<h1>NFLScrape</h1>

This NFLScrape project's goal is to build an unmonitored service that extracts data from pro-football-reference.com and saves it in a firebase realtime database. Essentially, this project is made of three components:
* scrapeToJSON.py
* processStats.py
* populateFirebase.py

These componenets are all launched from within main.py, and perform the tasks their names suggest.

The NFLScrape project runs on a Raspberry-Pi and is scheduled to run from the months of September to January:
* Every 30 minutes on Sundays from 1pm - 10:30pm
* Mondays and Thursdays at 10:30pm

This project is only designed to ensure that the firebase database possesses up-to-date data. Other projects will make copious use of this data, but they are not within the scope of this project.

<h2>Changelog</h2>

* Edited color scheme to fit the following format:
    * Color[0] = Primary Color
    * Color[1] = Text Color that will show up well on Primary
    * Color[2] = Seconday Color
    * Color[3] = Text Color that will show up well on Secondary
    * Color[4] = Tertiary Color
    * Color[5] = Quarternary Color
    * Color[6] = etc...