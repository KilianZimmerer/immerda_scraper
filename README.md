# immerda scraper
To get an overview of the amount of shifts people are doing.


# Setup

In the root directory run (make sure to have poetrys installed):

`poetry install`


# Run Script

To scrape the immerda shifts run in the project root:

`poetry run python immerda_scraper/scraper.py [URL_TO_SHIFTS]`

Where `[URL]` is the url to the immerda website e.g. https://turno.immerda.ch/s/asdasgsawfafs

The above will create a file "data/schichtplan_report.csv" storing the amount of shifts per person and the missing shifts.