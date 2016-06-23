from argparse import ArgumentParser
import re


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



def sorted_nicely( l ):
    """ Sort the given iterable in the way that humans expect.
        by Mark Byers: http://stackoverflow.com/questions/2669059/how-to-sort-alpha-numeric-set-in-python
    """
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(l, key = alphanum_key)