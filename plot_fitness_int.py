import yaml
import random
import os
import math
from argparse import ArgumentParser
from matplotlib import pyplot as plt
import matplotlib.lines as mlines
import matplotlib.colors as colors
import matplotlib.cm as cmx


parser = ArgumentParser()

parser.add_argument('file_path', metavar='DIR', type=str, help="Path to an integrated fitness file")
parser.add_argument('-t', '--title', type=str, default='plot title', help='Title of the plot')
parser.add_argument('-o', '--output', type=str, default='plot', help='Output file name')

parser.add_argument('--title-size', type=float, default=42, help='text size for the title')
parser.add_argument('--label-size', type=float, default=40, help='text size for the axis labels')
parser.add_argument('--legend-size', type=float, default=30, help='text size for the legend')
parser.add_argument('--tick-size', type=float, default=30, help='text size for the ticks')


def mean(values_list):
    return float(sum(values_list)) / float(len(values_list)) if len(values_list) > 0 else float('nan')

def median(values_list):
    num = len(values_list)
    if num % 2 == 0:
        val1 = values_list[num/2 - 1]
        val2 = values_list[num/2]
        median = float(val1 + val2) / 2.0
    else:
        median = values_list[(num-1) / 2]
    return median



def st_dev(values_list):
    variance = 0
    sample_mean = mean(values_list)
    for value in values_list:
        variance += (value - sample_mean)*(value - sample_mean)
    variance /= float(len(values_list) - 1.0)
    return math.sqrt(variance)


def main():
    args = parser.parse_args()

    title_size = args.title_size
    label_size = args.label_size
    tick_size = args.tick_size
    legend_size = args.legend_size

    in_file_path = os.path.abspath(args.file_path)
    dir_path = os.path.dirname(in_file_path)
    out_file_path = os.path.join(dir_path, args.output)

    print "input  : {0}".format(in_file_path)
    print "output : {0}".format(out_file_path)




    data_to_labels = {}

    points_x = []
    points_y = []
    mean_points_x = []
    mean_points_y = []

    st_dev_plus = []
    st_dev_minus = []

    y_data_bins = []
    x_data_labels = []

    with open(in_file_path, 'r') as in_file:
        for line in in_file:
            items = line.split(',')
            label = float(items[0])
            data_bin = []

            if label not in data_to_labels:
                data_to_labels[label] = []

            del items[0]
            for item in items:
                points_x.append(label)
                points_y.append(float(item))
                data_to_labels[label].append(float(item))
                data_bin.append(float(item))

            y_data_bins.append(data_bin)
            x_data_labels.append(label)

    for label in data_to_labels:
        values = data_to_labels[label]
        mean_points_x.append(label)
        mean_points_y.append(mean(values))
        st_dev_plus.append(mean(values) + st_dev(values))
        st_dev_minus.append(mean(values) - st_dev(values))




    # plot scatter:
    fig = plt.figure(figsize=(14, 8))
    ax = fig.add_subplot(111)

 #   ax.boxplot(y_data_bins) # box plots suck
    ax.scatter(points_x, points_y, s=50)
    ax.scatter(mean_points_x, mean_points_y, marker='+', s=3000, edgecolors='black')
    ax.scatter(mean_points_x, st_dev_plus, marker='_', s=3000, edgecolors='black')
    ax.scatter(mean_points_x, st_dev_minus, marker='_', s=3000, edgecolors='black')


    ax.tick_params(axis='both', which='major', labelsize=tick_size)
    ax.set_title(args.title, fontsize=title_size, y=1.02)
    xartist = ax.set_xlabel('population size', fontsize=label_size)
    yartist = ax.set_ylabel('integrated fitness', fontsize=label_size)
    ax.grid()
    fig.savefig(out_file_path + ".png", bbox_extra_artists=(xartist, yartist), bbox_inches='tight')
    # ##################################################################################################

   

if __name__ == '__main__':
    main()
