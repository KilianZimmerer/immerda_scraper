# immerda scraper
To get an overview of the amount of shifts people are doing.


# Setup

In the root directory run (make sure to have poetrys installed):

`poetry install`


# Run Script

To scrape the immerda shifts run in the project root:

`poetry run python immerda_scraper/scraper.py [URL_TO_SHIFTS]`

Where `[URL]` is the url to the immerda website e.g. https://turno.immerda.ch/s/asdasgsawfafs

The above will create a file "data/shifts.csv" storing the amount of shifts per person.

# Run Analysis

To compare people of the shift plan from immerda with a predefinied list of registered people run in the project root:

```shell
poetry run python immerda_scraper/scraper.py [URL_TO_SHIFTS]
poetry run python analysis/analysis.py "data/shifts.csv" [FILEPATH_OF_REGISTERED_PEOPLE]
```

This will create a file "data/shifts_registered_people.csv" as a starting point for further manual analysis.