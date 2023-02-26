import hashlib
import random
from PIL import Image, ImageDraw
from typing import List
import tkinter as tk
from tkinter import filedialog
import csv
from datetime import datetime
from modules import *

# Example usage
# lists_of_strings = [
#    ["foo", "bar", "baz", "<offline>", "<online>", None],
#    ["qux", "<online>", "quux"],
#    ["corge", "grault", "garply", "waldo", "fred"]
#]
#draw_squares(lists_of_strings)

draw_squares(generate_timeline())
