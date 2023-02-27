from modules import *

# TODO: argparse
def main():
    path = None
    if not type(path) == str:
        path = filedialog.askopenfilename(filetypes=[('HTML Documents', '*.html')], initialdir="./html")
    webbrowser.open('file://' + path)

if __name__ == '__main__':
    main()
