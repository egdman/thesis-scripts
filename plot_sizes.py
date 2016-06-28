import os
import yaml

from matplotlib import pyplot as plt
from plotters import parser, plot_single, read_sizes_from_file, get_default_colors, get_default_styles, draw_legend


parser.add_argument('file_path', metavar='PATH', type=str, help="Path to a size log file")


def main():
    args = parser.parse_args()

    input_filename = os.path.basename(args.file_path)

    # derive label of y axis:
    y_axis_label = "size"
    if "neuron" in input_filename:
        y_axis_label = "number of neurons"
    elif "connection" in input_filename:
        y_axis_label = "number of connections"


    # read sizes data from file:
    sizes_data = read_sizes_from_file(args.file_path)
    evaluation_num = sizes_data['eval']
    max_val = sizes_data['max']
    min_val = sizes_data['min']
    best_val = sizes_data['best']
    worst_val = sizes_data['worst']

    data_labels = ["max", "best", "worst", "min"]
    ydata = [max_val, best_val, worst_val, min_val]

    default_colors = get_default_colors(data_labels)
    default_styles = get_default_styles(data_labels)

    fig = plt.figure(figsize=(args.horsize,args.vertsize))
    ax = fig.add_subplot(111)

    extra_artists = plot_single(ax, args,
        xdata=evaluation_num,
        ydata=ydata,
        data_labels=data_labels,
        xlabel="evaluation #",
        ylabel=y_axis_label,
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
