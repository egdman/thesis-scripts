import yaml
import random
import os
import fnmatch

from matplotlib import pyplot as plt

import matplotlib.colors as colors
import matplotlib.cm as cmx

from plotters import parser, plot_raw, plot_average, sorted_nicely


parser.add_argument('dir_path', metavar='DIR', type=str, help="Path to a fitness log file")


def main():
    args = parser.parse_args()

    dir_path = args.dir_path

    out_filename = args.output
    if out_filename == '':
        out_filename = "plot"

    out_file_path = os.path.join(dir_path, out_filename)

    files_and_dirs = os.listdir(dir_path)
    files = [f for f in files_and_dirs if os.path.isfile(os.path.join(dir_path, f)) and
             fnmatch.fnmatch(f, '*-*.log')]


    map_data_to_labels = {}
    label_set = set()

    color_to_label = {} # dictionary {label:color} because we want the same labels have the same color
    style_to_label = {} # dictionary {label:linestyle}


    for filename in files:
        file_path = os .path.join(dir_path, filename)
        print "input :  {0}".format(file_path)

        with open(file_path, 'r') as in_file:
            yaml_data = in_file.read()

        # label = filename.split('-')[-2]

        label = get_label(filename)
        print "label : '{0}'".format(label)

        data = yaml.load(yaml_data)


        data_keyword = 'data'
        if 'velocities' in data[0]:
            data_keyword = 'velocities'
        elif 'sizes' in data[0]:
            data_keyword = 'sizes'


        data_items = [(data_item['generation'], data_item[data_keyword]) for data_item in data]
        data_items = sorted(data_items, key=lambda pair: pair[0])

        generation_num = []
        evaluation_num = []
        max_val = []
        best_val = []

        for i in range(len(data_items)):

            gen = data_items[i][0]
            data_points = data_items[i][1]
            generation_num.append(gen+1)
            evaluation_num.append((gen+1) * len(data_points))
            max_val.append(max(data_points) * 100.0)
            best_val.append(data_points[0])

        if label not in map_data_to_labels:
            map_data_to_labels[label] = []

        map_data_to_labels[label].append({'x': evaluation_num, 'y': max_val})
        label_set.add(label)


    # sort labels:
    sorted_labels = sorted_nicely(list(label_set))

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

    extra_artists = plot_raw(ax, args,
        sorted_labels=sorted_labels,
        map_data_to_labels=map_data_to_labels,
        color_to_label=color_to_label,
        style_to_label=style_to_label,
        xlabel="evaluation #",
        ylabel="movement speed, cm/s")

    ax.grid()

    fig.savefig(out_file_path + ".png", bbox_extra_artists=extra_artists, bbox_inches='tight')
    # ##################################################################################################


    # plot averaged data:
    fig = plt.figure(figsize=(args.horsize, args.vertsize))
    ax = fig.add_subplot(111)

    extra_artists = plot_average(ax, args,
        sorted_labels=sorted_labels,
        map_data_to_labels=map_data_to_labels,
        color_to_label=color_to_label,
        style_to_label=style_to_label,
        xlabel="evaluation #",
        ylabel="movement speed, cm/s")

    ax.grid()

    fig.savefig(out_file_path + "_mean.png", bbox_extra_artists=extra_artists, bbox_inches='tight')
    # ##################################################################################################


def get_label(filename):
    words = filename.split('-')
    del words[-1]
    label = ""
    for word in words:
        label += word
        label += "-"
    # chop off last dash
    return label[:-1]

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
