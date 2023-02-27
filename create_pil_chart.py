from modules import *

# NOTE: create_pil.py has been deprecated due to the drawbacks of PIL/Pillow for this task.
# Please use create_html instead.

def main():
    path = get_csv()
    draw_squares(generate_timeline(path, get_intervals()))

if __name__ == '__main__':
    main()
