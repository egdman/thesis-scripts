from argparse import ArgumentParser
import re

import matplotlib.lines as mlines


parser = ArgumentParser()

parser.add_argument('-t', '--title', type=str, default='plot title', help='Title of the plot')
parser.add_argument('-o', '--output', type=str, default='', help='Output file name')

parser.add_argument('--title-size', type=float, default=42, help='text size for the title')
parser.add_argument('--label-size', type=float, default=40, help='text size for the axis labels')
parser.add_argument('--legend-size', type=float, default=30, help='text size for the legend')
parser.add_argument('--tick-size', type=float, default=30, help='text size for the ticks')

parser.add_argument('--horsize', type=float, default=14, help='horizontal size of the image')
parser.add_argument('--vertsize', type=float, default=12, help='vertical size of the image')

parser.add_argument('--ylim-min', type=float, help='min Y axis limit')
parser.add_argument('--ylim-max', type=float, help='max Y axis limit')

parser.add_argument('--xlim-min', type=float, help='min X axis limit')
parser.add_argument('--xlim-max', type=float, help='max X axis limit')

parser.add_argument('-lt', '--legend-title', type=str, default='', help='The title of the legend')

MARKERSIZE = 6

def sorted_nicely( l ):
    """ Sort the given iterable in the way that humans expect.
        by Mark Byers: http://stackoverflow.com/questions/2669059/how-to-sort-alpha-numeric-set-in-python
    """
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(l, key = alphanum_key)



def set_axes_limits(axes, args):
	if args.ylim_min is not None or args.ylim_max is not None:
	    axes.set_ylim(args.ylim_min, args.ylim_max)

	if args.xlim_min is not None or args.xlim_max is not None:
	    axes.set_xlim(args.xlim_min, args.xlim_max)



def get_handles_labels(ordered_labels, color_to_label, style_to_label=None):

    legend_handles = []
    legend_labels = []
    for label in ordered_labels:
        color = color_to_label[label]

        if style_to_label is not None:
            style = style_to_label[label]
        else:
            style = ('-', '')

        hnd = mlines.Line2D([],[], color=color,
            linestyle=style[0],
            marker=style[1],
            markersize=MARKERSIZE,
            linewidth=4)

        legend_handles.append(hnd)
        legend_labels.append(label)
    return legend_handles, legend_labels



def draw_legend(axes, args, sorted_labels, color_to_label, style_to_label):
	legend_fontsize = args.legend_size
	hnd, lab = get_handles_labels(sorted_labels, color_to_label, style_to_label)
	lgd = axes.legend(hnd, lab, loc=0, prop={'size': legend_fontsize}, framealpha=0.5)
	if args.legend_title is not None:
	    lgd.set_title(args.legend_title, prop={'size': legend_fontsize})



def get_default_colors(labels):
    colors = ['red', 'green', 'black', 'blue']
    num_colors = len(colors)
    return {labels[i]: colors[i%num_colors] for i in range(len(labels))}


def get_default_styles(labels):
    styles = [('--', ''), ('-', ''), (':', ''), ('--', '')]
    num_styles = len(styles)
    return {labels[i]: styles[i%num_styles] for i in range(len(labels))}