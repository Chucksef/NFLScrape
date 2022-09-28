#NFLScrape

This NFLScrape project's goal is to build an unmonitored service that extracts data from pro-football-reference.com and saves it in a firebase realtime database. Essentially, this project is made of three components:
* scrapeToJSON.py
* processStats.py
* populateFirebase.py

These componenets are all launched from within main.py, and perform the tasks their names suggest.

The NFLScrape project runs on a Raspberry-Pi and is scheduled to run from the months of September to January:
* Every 30 minutes on Sundays from 1pm - 10:30pm
* Mondays and Thursdays at 10:30pm