from modules import *
import math

from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def plot_legend(names, *, ncols=4):

    cell_width = 212
    cell_height = 22
    swatch_width = 48
    margin = 12

    n = len(names)
    nrows = math.ceil(n / ncols)

    width = cell_width * 4 + 2 * margin
    height = cell_height * nrows + 2 * margin
    dpi = 72

    fig, ax = plt.subplots(figsize=(width / dpi, height / dpi), dpi=dpi)
    fig.subplots_adjust(margin/width, margin/height,
                        (width-margin)/width, (height-margin)/height)
    ax.set_xlim(0, cell_width * 4)
    ax.set_ylim(cell_height * (nrows-0.5), -cell_height/2.)
    ax.yaxis.set_visible(False)
    ax.xaxis.set_visible(False)
    ax.set_axis_off()

    for i, name in enumerate(names):
            if name is None:
                # Draw a square with a light red outline and no fill
                outline_color = (255, 128, 128)
                fill_color = None
            elif name == "<offline>":
                # Draw a square with a light gray outline and no fill
                outline_color = (192, 192, 192)
                fill_color = None
            elif name == "<online>":
                # Draw a square with a dodger blue outline and no fill
                outline_color = (30, 144, 255)
                fill_color = None
            else:
        
        row = i % nrows
        col = i // nrows
        y = row * cell_height

        swatch_start_x = cell_width * col
        text_pos_x = cell_width * col + swatch_width + 7

        ax.text(text_pos_x, y, name, fontsize=14,
                horizontalalignment='left',
                verticalalignment='center')

        ax.add_patch(
            Rectangle(xy=(swatch_start_x, y-9), width=swatch_width,
                      height=18, facecolor=string_to_color(name), edgecolor='0.7')
        )

    return fig

def draw_legend():
    timeline = generate_timeline()
    uniques = get_unique_strings(timeline)
    plot_legend(uniques)

    
draw_legend()
