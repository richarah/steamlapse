# steamlapse

Python program pinpointing particular pastimes perpetuating procrastination. Originally made as a practical joke for PVV @ NTNU.



#### What is this?

Steamlapse is a set of programs for collecting and visualising Steam activity data via Steam Web API, creating a GitHub-like timelapse of user activity (read: procrastination).

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

#### Note on running in background

This script has a tendency to randomly disconnect when run in the background with e.g. `python3 collect.py &`. Thus, it is strongly advisable to use `screen`, `tmux` or similar for background operation instead.

### add_csv.py

`add_csv.py` prompts for a 17-digit Steam ID and creates a CSV file linked to this ID, so `collect.py` can collect data for this Steam user.

To use `add_csv.py`, navigate to the root directory of the project and run the following command. You will then be prompted for a CSV file, located in the data directory by default.

```
python add_csv.py
```

### create_html_chart.py

Generates and saves a HTML chart (with internal CSS) from a CSV. It may then be viewed with `view_html_chart.py` (see below)

### view_html_chart.py

Prompts for a HTML chart and displays it in the default web browser.

### create_pil_chart.py (DEPRECATED)

#### Please note

`create_pil_chart.py` has been deprecated due to the inherent limitations of PIL/Pillow for this task. Please use `create_html_chart.py` instead.

Creates a timelapse of Steam activity for a specified Steam user. To use `chart.py`, navigate to the root directory of the project and run the following command:

```
python chart.py
```

This will prompt for a CSV file, and create a Github-like timelapse of Steam activity for the user linked to that file.
