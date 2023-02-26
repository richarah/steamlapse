from modules import *

from tempfile import NamedTemporaryFile
import webbrowser

# Example usage
# lists_of_strings = [
#    ["foo", "bar", "baz", "<offline>", "<online>", None],
#    ["qux", "<online>", "quux"],
#    ["corge", "grault", "garply", "waldo", "fred"]
#]
#draw_squares(lists_of_strings)

def display_html_string(html_string):
    with NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
        f.write(html_string)
        webbrowser.open(f.name)

def get_intervals(default=24):
    user_input = input ("Intervals (default " + str(default) + "): ") or default
    return int(user_input)

print(generate_css())
print(draw_squares_html(generate_timeline(get_intervals())))
