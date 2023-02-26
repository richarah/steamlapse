from modules import *

# Example usage
# lists_of_strings = [
#    ["foo", "bar", "baz", "<offline>", "<online>", None],
#    ["qux", "<online>", "quux"],
#    ["corge", "grault", "garply", "waldo", "fred"]
#]
#draw_squares(lists_of_strings)

def get_intervals(default=24):
    user_input = input ("Intervals (default " + str(default) + "): ") or default
    return int(user_input)

draw_squares(generate_timeline(get_intervals()))
