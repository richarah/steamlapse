import hashlib
import random
from PIL import Image, ImageDraw
from typing import List
import tkinter as tk
from tkinter import filedialog
import csv
from datetime import datetime


def generate_timeline():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename()

    intervals_by_day = {}

    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if len(row) < 2:
                continue
            game_name, timestamp = row[0], row[1]
            if not timestamp or len(timestamp.split()) < 2:
                continue
            timestamp_dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
            day = timestamp_dt.date()
            if day not in intervals_by_day:
                intervals_by_day[day] = [None] * 96
            hour, minute, second = timestamp_dt.time().hour, timestamp_dt.time().minute, timestamp_dt.time().second
            interval = hour * 4 + minute // 15
            if 0 <= interval < 96:
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
            current_day_intervals = [None] * 96
        elif current_day != day:
            max_games_by_day.append(current_day_intervals)
            current_day = day
            current_day_intervals = [None] * 96

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
    SQUARE_SIZE = 8
    SQUARE_SPACING = 2
    SQUARE_PADDING = 16

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
            draw.rounded_rectangle((x0, y0, x1, y1), fill=fill_color, outline=outline_color, radius=2)

    # Display the image
    img.show()


# Example usage
# lists_of_strings = [
#    ["foo", "bar", "baz", "<offline>", "<online>", None],
#    ["qux", "<online>", "quux"],
#    ["corge", "grault", "garply", "waldo", "fred"]
#]
#draw_squares(lists_of_strings)

draw_squares(generate_timeline())
