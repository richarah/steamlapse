# steamlapse



Originally made as a practical joke for PVV @ NTNU, but ended up growing into something much bigger...



#### What is this?

Steamlapse is a Python project for visualising Steam activity data, creating a GitHub-like timelapse of user activity (read: procrastination).

## Prerequisites

To use Steamlapse, you will need to have Python 3 installed, in addition to Pillow and a few ancillary libraries - these may be installed as follows:

```
pip install -r requirements.txt
```

You will also need to [obtain a Steam API key](https://steamcommunity.com/dev/apikey) and set it in a `.env` file in the root directory of the project:

```
STEAM_API_KEY=<your Steam API key>
```

## Usage

There are three main Python scripts in the project:

### collect.py

`collect.py` collects timestamps and persona states for each CSV file located in the `./data` directory.

To use `collect.py`, navigate to the root directory of the project and run the following command:

```
python collect.py
```

This will periodically query the Steam API and update each CSV file in the `./data` directory with the latest Steam activity data.

### add_csv.py

`add_csv.py` prompts for a 17-digit Steam ID and creates a CSV file linked to this ID, so `collect.py` can collect data for this Steam user.

To use `add_csv.py`, navigate to the root directory of the project and run the following command. You will then be prompted for a CSV file, located in the data directory by default.

```
python add_csv.py
```

### chart.py

**Please note:** This may be (mostly) phased out in the future in favour of html_chart.py when the latter is complete and stable.

`chart.py` creates a timelapse of Steam activity for a specified Steam user. To use `chart.py`, navigate to the root directory of the project and run the following command:

```
python chart.py
```

This will prompt for a CSV file, and create a Github-like timelapse of Steam activity for the user linked to that file.

### html_chart.py

**Please note: This is a work in progress!**

Similar to `chart.py`, except generates a HTML page (with internal CSS) instead of a PIL image.
