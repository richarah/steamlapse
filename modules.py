import requests
import time
import csv
import os
import re

import tkinter as tk
import webbrowser
from tkinter import filedialog
from datetime import datetime, timedelta
from typing import List
import hashlib
import random
from PIL import Image, ImageDraw

# Timeline

def get_unique_strings(lists_of_strings):
    unique_strings = set()
    for lst in lists_of_strings:
        unique_strings.update(lst)
    return unique_strings

def get_intervals(default=24):
    return int(input ("Intervals (default " + str(default) + "): ") or default)

def get_csv():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(initialdir="./data")
    return file_path

def generate_timeline(file_path, num_intervals=24):

    intervals_by_day = {}

    # read CSV and fill intervals_by_day dictionary
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            game_name, timestamp = row[0], row[1]
            if not timestamp or len(timestamp.split()) < 2:
                continue
            timestamp_dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
            day = timestamp_dt.date()
            if day not in intervals_by_day:
                intervals_by_day[day] = [None] * num_intervals
            hour, minute, second = timestamp_dt.time().hour, timestamp_dt.time().minute, timestamp_dt.time().second
            interval_length = 1440 // num_intervals
            interval = hour * 60 // interval_length + minute // interval_length
            if 0 <= interval < num_intervals:
                if intervals_by_day[day][interval] is None:
                    intervals_by_day[day][interval] = {}
                if game_name.lower() == "<online>" or game_name.lower() == "<offline>":
                    intervals_by_day[day][interval]["<online>"] = [timestamp]
                else:
                    if game_name in intervals_by_day[day][interval]:
                        intervals_by_day[day][interval][game_name].append(timestamp)
                    else:
                        intervals_by_day[day][interval][game_name] = [timestamp]

    # fill in missing days with <offline> values
    earliest_day = min(intervals_by_day.keys())
    latest_day = max(intervals_by_day.keys())
    for day in sorted((earliest_day + timedelta(days=i) for i in range((latest_day - earliest_day).days + 1))):
        if day not in intervals_by_day:
            intervals_by_day[day] = [None] * num_intervals
            for i in range(num_intervals):
                intervals_by_day[day][i] = "<offline>"

    # compute max game played for each interval in each day
    max_games_by_day = []
    current_day = None
    current_day_intervals = None
    for day, intervals in sorted(intervals_by_day.items(), reverse=True):
        if current_day is None:
            current_day = day
            current_day_intervals = [None] * num_intervals
        elif current_day != day:
            max_games_by_day.append(current_day_intervals)
            current_day = day
            current_day_intervals = [None] * num_intervals

        for i, game_counts in enumerate(intervals):
            if not isinstance(game_counts, dict):
                current_day_intervals[i] = None
            else:
                if "<online>" in game_counts and "<offline>" in game_counts:
                    current_day_intervals[i] = "<online>"
                else:
                    max_game = max(game_counts, key=lambda g: (len(game_counts[g]), game_counts[g][-1]), default=None)
                    current_day_intervals[i] = max_game

    if current_day_intervals is not None:
        max_games_by_day.append(current_day_intervals)

    return max_games_by_day


# Graphics - colours

def dim_rgb(rgb, brightness=0.67):
    r = rgb[0]
    g = rgb[1]
    b = rgb[2]
    return round(r*brightness), round(g*brightness), round(b*brightness)

def string_to_rgb(s):
    # Hash the input string using SHA-256
    hash_value = hashlib.sha256(s.encode()).hexdigest()

    # Take the first 6 characters of the hash as the RGB values
    r, g, b = int(hash_value[:2], 16), int(hash_value[2:4], 16), int(hash_value[4:6], 16)

    # Randomly adjust the brightness of the color
    # brightness = random.uniform(0.5, 1.0)
    # r = int(r * brightness)
    # g = int(g * brightness)
    # b = int(b * brightness)

    # Format the RGB values as a hex color code
    color_code = "#{:02x}{:02x}{:02x}".format(r, g, b)

    return r, g, b

def string_to_color(s):
    r, g, b = string_to_rgb(s)
    # Format the RGB values as a hex color code
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


# Graphics - rendering

def antialias_img(img):
    upsampled = img.resize((img.width * 2, img.height * 2), resample=Image.NEAREST)
    return upsampled.resize((img.width // 2, img.height // 2), resample=Image.ANTIALIAS)

def draw_squares(lists_of_strings: List[List[str]]):
    # Define constants for the size and spacing of the squares
    SQUARE_SIZE = 32
    SQUARE_SPACING = 8
    SQUARE_PADDING = 64
    
    # Outline
    OUTLINE_WIDTH = 4
    OUTLINE_RADIUS = 8

    # Determine the dimensions of the image
    num_rows = len(lists_of_strings)
    num_cols = max(len(lst) for lst in lists_of_strings)
    img_width = num_cols * (SQUARE_SIZE + SQUARE_SPACING) - SQUARE_SPACING + SQUARE_PADDING*2
    img_height = num_rows * (SQUARE_SIZE + SQUARE_SPACING) - SQUARE_SPACING + SQUARE_PADDING*2

    # Create a new image
    img = Image.new("RGB", (img_width, img_height), "white")
    draw = ImageDraw.Draw(img)

    # Loop over the lists of strings and draw the squares
    for row_idx, lst in enumerate(lists_of_strings):
        for col_idx, s in enumerate(lst):
            if s is None:
                # Draw a square with a light red outline and no fill
                outline_color = (255, 128, 128)
                fill_color = None
            elif s == "<offline>":
                # Draw a square with a light gray outline and no fill
                outline_color = (192, 192, 192)
                fill_color = None
            elif s == "<online>":
                # Draw a square with a dodger blue outline and no fill
                outline_color = (30, 144, 255)
                fill_color = None
            else:
                # Convert the string to a color using the string_to_color function
                color_code = string_to_color(s)
                outline_color = color_code
                fill_color = color_code

            # Calculate the coordinates of the square
            x0 = col_idx * (SQUARE_SIZE + SQUARE_SPACING) + SQUARE_PADDING
            y0 = row_idx * (SQUARE_SIZE + SQUARE_SPACING) + SQUARE_PADDING
            x1 = x0 + SQUARE_SIZE
            y1 = y0 + SQUARE_SIZE

            # Draw the square
            draw.rounded_rectangle((x0, y0, x1, y1), fill=fill_color, outline=outline_color, radius=OUTLINE_RADIUS, width=OUTLINE_WIDTH)
            
    img = antialias_img(img)
    
    # Display the image
    img.show()


# CSS
def generate_css(row_length=24) -> str:

    # Set minimum size of a square in pixels.
    # Also a scaling factor in vw, so it won't be overrun in case of too many intervals
    scale = (32 / row_length)
    min_size=12

    # Define constants for the size and spacing of the squares
    SQUARE_SIZE = f'max({min_size}px, {scale}vw)'
    SQUARE_SPACING = f'max({min_size // 4}px, {scale / 4}vw)'
    SQUARE_PADDING = f'max({min_size}px, {scale / 4}vw)'
    
    # Outline. Must be min 2px for graphics to render as intended
    OUTLINE_WIDTH = f'max(2px, {min_size // 6}px, {scale / 6}vw)'
    OUTLINE_RADIUS = f'max(2px, {min_size // 6}px, {scale / 6}vw)'
    
    # Start the CSS string with the opening <style> tag
    css = '<style>\n'

    # Headings & text
    css += f'h1, h2, h3, h4, h5, h6, p, text {{ font-family: Helvetica, sans-serif; }}\n'
    css += f'h1, h2, h3, h4, h5, h6, p, text {{ font-family: Helvetica, sans-serif; }}\n'

    # Wrapper div. Center the chart
    css += f'.wrapper {{ white-space: nowrap; text-align: left; margin-left: 20vw; }}\n'

    # Legend
    css += f'.legend {{ white-space: nowrap; text-align: left; }}\n'
    css += f'.legend tr {{ padding: {SQUARE_SPACING}; }}\n'
    css += f'.legend text {{ font-size: {SQUARE_SIZE}; }}\n'

    # Add the CSS styles for the squares
    css += f'.square {{ border-style: solid; width: {SQUARE_SIZE}; height: {SQUARE_SIZE}; border-radius: {OUTLINE_RADIUS}; border-width: {OUTLINE_WIDTH}; margin: {SQUARE_SPACING}; padding: 0; display: inline-block; }}\n'
    css += f'.offline {{ border-color: rgb(192, 192, 192); }}\n'
    css += f'.online {{ border-color: rgb(30, 144, 255); }}\n'
    css += f'.error {{ border-color: rgb(255, 128, 128); }}\n'

    # Special case: squares in legend div
    css += f'.legend .square {{ margin: 0; padding: 0; }}\n'

    # Finish the CSS string with the closing </style> tag
    css += '</style>\n'
    
    return css


# HTML


# Return a single html div representing a square
def html_square(s):
    if s is None:
        # Add a square with a light red outline and no fill
        return f'<div class="error square"></div>'
    elif s == "<offline>":
        # Add a square with a light gray outline and no fill
        return f'<div class="offline square"></div>'
    elif s == "<online>":
        # Add a square with a dodger blue outline and no fill
        return f'<div class="online square"></div>'
    else:
        # Convert the string to a color using the string_to_color function
        # Also use a slightly dimmer tone for the outline
        rgb_fill = string_to_rgb(s)
        rgb_outline = dim_rgb(rgb_fill)
        return f'<div class="game square" style="background-color: rgb{rgb_fill}; border-color: rgb{rgb_outline};"></div>'



# Returns legend div
def html_legend(timeline):
    # Unique strings from timeline
    uniques = get_unique_strings(timeline)
    
    # Skip non-game squares
    game_states = []
    html = ''
    for s in uniques:
        square = html_square(s)
        if "game" in square:
            game_states.append(s)

    # Game states
    html += '<tr><td><text><b>Game states</b></text></td></tr>'
    for s in game_states:
        print(s)
        html += f'<tr><td>{html_square(s)}</td><td><text>{s}</text></td></tr>'
    
    # Special states
    special_states ={"<offline>" : "Offline", "<online>" : "Online", None : "N/A"} 
    html += '<tr><td><text><b>Persona states</b></text></td></tr>'
    for k in special_states.keys():
        v = special_states[k]
        html += f'<tr><td>{html_square(k)}</td><td><text>{v}</text></td></tr>'

    # Wrap the HTML code in a div and return it
    return '<table class="legend">{}</table>'.format(html)


def generate_html_chart(timeline: List[List[str]], name=None) -> str:

    # Generate internal stylesheet
    css = generate_css(len(timeline[0]))

    title = "Steamlapse"

    # Different title if name is not set
    if name is not None and type(name) == str:
        title = (name+"'s Steamlapse")
    
    # Start the HTML string
    html = f'<html><head><meta name="viewport" content="width=device-width, initial-scale=1">{css}<title>{title}</title></head><body><div class="wrapper">'

    html += f'<h1>{title}</h1>'


    # Loop over the lists of strings and add the squares to the HTML string
    for row_idx, lst in enumerate(timeline):
        for col_idx, s in enumerate(lst):
            html += html_square(s)

        # Add a line break between rows
        html += f'<br>'
        
    # Legend
    html += "<h2>Legend</h2>"
    html += html_legend(timeline)

    # End HTML wrapper div
    html += "</div>"

    # Finish the HTML string
    html += f'</body></html>'
    
    return html


# Processing

def valid_steam_id(steam_id):
    if len(steam_id) != 17:
        return False
    if not steam_id.isnumeric():
        return False
    return True


def get_time():
    # Avoid jet lag
    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())


def get_player_data(steam_id, api_key):
    url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={api_key}&steamids={steam_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None


def get_persona(player_data):
    return player_data['response']['players'][0]['personaname']


def get_game(player_data):
    if not player_data['response']['players']:
        return "<offline>"
    elif 'gameextrainfo' in player_data['response']['players'][0]:
        return player_data['response']['players'][0]['gameextrainfo']
    else:
        return '<online>'
    
def append_csv_header(file_path):
    if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
        with open(file_path, 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['game', 'timestamp'])

def append_csv_entry(file_path, player_data):
    append_csv_header(file_path)
    game = get_game(player_data)
    timestamp = get_time()
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([game, timestamp])

# Persona name and Steam ID from path
def split_filename(filename):
    pattern = r"(.+)_([0-9]{17})\.csv"
    match = re.match(pattern, filename)
    if match:
        return match
    else:
        return None

# These are not used in the same program, hence this factoring
def persona_from_path(filename):
    return os.path.basename(split_filename(filename).group(1))

def id_from_path(filename):
    return split_filename(filename).group(2)


def save_html_chart(input_path="data/data.css", output_path=None, prompt=True, persona=None, intervals=24, in_place=False): 
    
    if prompt:
        intervals = get_intervals()
        print("Spawning file dialog.")
        input_path = get_csv()
    else:
        print("Using default intervals:", intervals)
        print("Using default input:", input_path)
    
    # Persona can be set in function args for headless operations - if not set, generate from path
    if not persona:
        persona = persona_from_path(input_path)
        print("Persona not set. Using", persona)
        
    if not output_path:
        output_path = f"html/{persona}.html"
        print("Output path not set. Using", output_path)
    
    print("Generating chart for " + persona + "...")
    html = generate_html_chart(generate_timeline(input_path, intervals), persona)

    # Return HTML as a string if in_place is enabled - else, return the output path
    if in_place:
        return html
    else:
        f = open(output_path, "w")
        f.write(html)
        f.close()
        print("Saved to", output_path)
        return output_path
    

