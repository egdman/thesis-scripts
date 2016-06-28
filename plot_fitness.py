import os
import yaml

from matplotlib import pyplot as plt
from plotters import parser, plot_single, read_fitness_from_file, get_default_colors, get_default_styles, draw_legend

parser.add_argument('file_path', metavar='PATH', type=str, help="Path to a fitness log file")


def main():
    args = parser.parse_args()

    fitness_data = read_fitness_from_file(args.file_path)
    evaluation_num = fitness_data['eval']
    max_values = fitness_data['max']
    min_values = fitness_data['min']
    mean_values = fitness_data['mean']
    median_values = fitness_data['median']

    data_labels = ["max", "mean", "median", "min"]
    ydata = [max_values, mean_values, median_values, min_values]


    default_colors = get_default_colors(data_labels)
    default_styles = get_default_styles(data_labels)


    fig = plt.figure(figsize=(args.horsize,args.vertsize))
    ax = fig.add_subplot(111)
    

    extra_artists = plot_single(ax, args, xdata=evaluation_num,
        ydata=ydata,
        data_labels=data_labels,
        xlabel="evaluation #",
        ylabel="movement speed, cm/s",
        colors=default_colors,
        styles=default_styles
        )


    ax.grid()

    draw_legend(ax, args, data_labels, default_colors, default_styles)

    if args.output == '':
        plt.show()
    else:
        out_file_path = os.path.join(os.path.dirname(args.file_path), args.output)
        fig.savefig(out_file_path, bbox_extra_artists=extra_artists, bbox_inches='tight')


if __name__ == '__main__':
    main()
