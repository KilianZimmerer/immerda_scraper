# immerda scraper
To get an overview of the amount of shifts people are doing.


# Setup

In the root directory run (make sure to have poetrys installed):

`poetry install`


# Analysis


1. Create an overview of the shifts by running:

`poetry run python immerda_scraper/shift_overview.py [URL_TO_SHIFTS]`

Where `[URL]` is the url to the immerda website e.g. https://turno.immerda.ch/s/asdasgsawfafs

The above will create a file "data/schichtplan_overview.csv" as well as a "xlsx" file "data/[date]_[time]_schichtplan_overview.xlsx". These files store the amount of shifts per person and the mismatch to what shifts are expected.

2. Check if registered people match the shift schedule

First create a file "data/hzr.csv" with a column "name" and fill it with names that are registered.

Then run:

`poetry run python immerda_scraper/match_to_registered.py`

The output will show you the mismatch.

3. To only get faulty shifts

First run step 1 as explain above.

Then run:

`poetry run python immerad_scraper/get_faulty.py`

The above will create a file "data/schichtplan_report.csv" as well as a "xlsx" file "data/[date]_[time]_schichtplan_report.xlsx". These files only show the faulty shits.