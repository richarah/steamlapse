from modules import *

path = get_csv()
display_html_in_browser(generate_html(generate_timeline(path, get_intervals()), persona_from_path(path)))
