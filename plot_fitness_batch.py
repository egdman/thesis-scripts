import yaml
import random
import os
import fnmatch

from matplotlib import pyplot as plt

import matplotlib.colors as colors
import matplotlib.cm as cmx

from plotters import parser, plot_raw, plot_average, sorted_nicely, read_from_dir, draw_legend


parser.add_argument('dir_path', metavar='DIR', type=str, help="Path to a fitness log directory")


def main():
    args = parser.parse_args()

    dir_path = args.dir_path

    out_filename = args.output
    if out_filename == '':
        out_filename = "plot"

    out_file_path = os.path.join(dir_path, out_filename)

    color_to_label = {} # dictionary {label:color} because we want the same labels have the same color
    style_to_label = {} # dictionary {label:linestyle}


    # get data from directory:
    map_data_to_labels = read_from_dir(dir_path)

    # sort labels:
    sorted_labels = sorted_nicely(list(map_data_to_labels.keys()))

    # assign colors to labels:
    colmap = get_colormap(len(sorted_labels))
    for i, label in enumerate(sorted_labels):
        # color_to_label[label] = colmap(i)
        color_to_label[label] = 'black'


    # assign styles to labels:
    stylemap = get_stylemap(len(sorted_labels))
    for i, label in enumerate(sorted_labels):
        style_to_label[label] = stylemap[i]
   #     style_to_label[label] = ('-', '')


    # plot raw data:
    fig = plt.figure(figsize=(args.horsize, args.vertsize))
    ax = fig.add_subplot(111)

    # draw plots:
    extra_artists = plot_raw(ax, args,
        sorted_labels=sorted_labels,
        map_data_to_labels=map_data_to_labels,
        color_to_label=color_to_label,
        style_to_label=style_to_label,
        xlabel="evaluation #",
        ylabel="movement speed, cm/s",
        thickness=2)

    # draw grid:
    ax.grid()

    # draw legend:
    draw_legend(ax, args, sorted_labels, color_to_label, style_to_label)

    # save figure to file:
    fig.savefig(out_file_path + ".png", bbox_extra_artists=extra_artists, bbox_inches='tight')
    # ##################################################################################################


    # plot averaged data:
    fig = plt.figure(figsize=(args.horsize, args.vertsize))
    ax = fig.add_subplot(111)

    # draw plots:
    extra_artists = plot_average(ax, args,
        sorted_labels=sorted_labels,
        map_data_to_labels=map_data_to_labels,
        color_to_label=color_to_label,
        style_to_label=style_to_label,
        xlabel="evaluation #",
        ylabel="movement speed, cm/s")

    # draw grid:
    ax.grid()

     # draw legend:
    draw_legend(ax, args, sorted_labels, color_to_label, style_to_label)

    # save figure to file:
    fig.savefig(out_file_path + "_mean.png", bbox_extra_artists=extra_artists, bbox_inches='tight')
    # ##################################################################################################


def get_stylemap(N):
    styles = ['-', '--', '-.', ':']
    markers = ['', 's', '^']
    combinations = []
    for marker in markers:
        for style in styles:   
            combinations.append((style, marker))

    stylemap = [combinations[i % len(combinations)] for i in range(0, N)]
    return stylemap


def get_colormap(N):
    '''Returns a function that maps each index in 0, 1, ... N-1 to a distinct
    RGB color.'''
    color_norm  = colors.Normalize(vmin=0, vmax=N-1)
    scalar_map = cmx.ScalarMappable(norm=color_norm, cmap='jet') # hsv
    def map_index_to_rgb_color(index):
        return scalar_map.to_rgba(index)
    return map_index_to_rgb_color



if __name__ == '__main__':
    main()
