# immerda scraper
To get an overview of the amount of shifts people are doing.


# Setup

In the root directory run (make sure to have [uv](https://docs.astral.sh/uv/getting-started/installation/) installed):

`uv sync`


# Runbook

## Step 1: Create a shift overview

**Script:** `immerda_scraper/shift_overview.py`

**What it does:**

This script scrapes one or more immerda shift schedule URLs and produces a per-person overview of how many shifts they have, broken down by label (TRY_HARD, FLEXI, NORMAL). It also calculates the difference to the expected number of shifts per label (1× TRY_HARD, 1× FLEXI, 2× NORMAL).

**Command:**

```bash
uv run python immerda_scraper/shift_overview.py [URL] ...
```

Where the URL points to an immerda shift page, e.g. `https://turno.immerda.ch/s/asdasgsawfafs`

**Output files:**
- `data/schichtplan_overview.csv`
- `data/[date]_[time]_schichtplan_overview.xlsx`

Both contain the same data: one row per person with columns for shift counts and deviations.

---

## Step 2: Match registered people to the shift schedule

**Script:** `immerda_scraper/match_to_registered.py`

**What it does:**

This script compares the list of people in the shift schedule (from Step 1) against a list of registered people and reports mismatches in both directions:
- People who are **registered but not in the Schichtplan** — they signed up but have no shifts.
- People who are **in the Schichtplan but not registered** — they have shifts but aren't on the registration list.

It uses the alias mapper to reconcile known name variations so those don't get falsely flagged.

**Prerequisites:**

1. Run Step 1 first so that `data/schichtplan_overview.csv` exists.

2. Create `data/hzr.csv` with a column `name` containing the registered names (one per row). Example:

```csv
name
MÜLLER MAX
SCHMIDT ANNA
VON BERG LUKAS
```

3. Create `config/alias_mapper.json` to handle name mismatches (typos, abbreviations, umlauts, etc.) between the two data sources. Example:

```json
{
  "registered_to_schichtplan": {
    "MÜLLER MAX": ["MUELLER MAX", "MULLER MAX", "M MAX"],
    "SCHMIDT ANNA": ["SCHMITT ANNA", "SCHMIDT A"],
    "VON BERG LUKAS": ["VONBERG LUKAS", "V BERG LUKAS"]
  }
}
```

Each key is a name as it appears in the HZR registration list, and the value is a list of possible aliases as they might appear in the Schichtplan.

**Command:**

```bash
uv run python immerda_scraper/match_to_registered.py
```

**Output (stdout):**

```
Nicht im Schichtplan aber registriert: {'NAME A', 'NAME B'}
Nicht registriert aber im Schichtplan: {'NAME C', 'NAME D'}
```

---

## Step 3: Get only faulty shifts

**Script:** `immerda_scraper/get_faulty.py`

**What it does:**

This script filters the shift overview down to only people who have a deviation from the expected number of shifts. It also appends summary rows showing the total over- and under-allocation.

**Prerequisites:**

Run Step 1 first so that `data/schichtplan_overview.csv` exists.

**Command:**

```bash
uv run python immerda_scraper/get_faulty.py
```

**Output files:**
- `data/schichtplan_report.csv`
- `data/[date]_[time]_schichtplan_report.xlsx`

Both contain only the people with faulty shift counts, plus the summary rows at the bottom.
