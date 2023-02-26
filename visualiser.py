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

print(generate_timeline())
