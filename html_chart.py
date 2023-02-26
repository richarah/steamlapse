from modules import *

# Example usage
# lists_of_strings = [
#    ["foo", "bar", "baz", "<offline>", "<online>", None],
#    ["qux", "<online>", "quux"],
#    ["corge", "grault", "garply", "waldo", "fred"]
#]
#draw_squares(lists_of_strings)

display_html_in_browser(generate_html(generate_timeline(get_intervals())))
