import requests
import time
import csv
import os
import re

import tkinter as tk
from tkinter import filedialog
from datetime import datetime
from typing import List
import hashlib
import random
from PIL import Image, ImageDraw

# WIP - interval adjustment

# Timeline

def get_unique_strings(lists_of_strings):
    unique_strings = set()
    for lst in lists_of_strings:
        unique_strings.update(lst)
    return unique_strings


def generate_timeline(num_intervals=96):

    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(initialdir="./data")

    intervals_by_day = {}

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

    max_games_by_day = []
    current_day = None
    current_day_intervals = None
    for day, intervals in sorted(intervals_by_day.items()):
        if current_day is None:
            current_day = day
            current_day_intervals = [None] * num_intervals
        elif current_day != day:
            max_games_by_day.append(current_day_intervals)
            current_day = day
            current_day_intervals = [None] * num_intervals

        for i, game_counts in enumerate(intervals):
            if game_counts is None:
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


# Graphics

def antialias_img(img):
    upsampled = img.resize((img.width * 2, img.height * 2), resample=Image.NEAREST)
    return upsampled.resize((img.width // 2, img.height // 2), resample=Image.ANTIALIAS)


def string_to_color(s):
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

    return color_code


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
    elif player_data['response']['players'][0]['personastate'] == 1:
        return "<online>"
    else:
        return player_data['response']['players'][0]['gameextrainfo']

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
        
def id_from_path(filename):
    pattern = r"(.+)_([0-9]{17})\.csv"
    match = re.match(pattern, filename)
    if match:
        return match.group(2)
    else:
        return None
