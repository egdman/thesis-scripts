import os
import yaml

from matplotlib import pyplot as plt
from plotters import parser, plot_single, read_fitness_from_file


parser.add_argument('file_path', metavar='PATH', type=str, help="Path to a fitness log file")


def main():
    args = parser.parse_args()

    fitness_data = read_fitness_from_file(args.file_path)
    evaluation_num = fitness_data['eval']
    max_values = fitness_data['max']
    min_values = fitness_data['min']
    mean_values = fitness_data['mean']
    median_values = fitness_data['median']
    
    fig = plt.figure(figsize=(args.horsize,args.vertsize))
    ax = fig.add_subplot(111)


    extra_artists = plot_single(ax, args, xdata=evaluation_num,
        ydata=[max_values, mean_values, median_values, min_values],
        data_labels=["max", "mean", "median", "min"],
        xlabel="evaluation #",
        ylabel="movement speed, cm/s")

    ax.grid()

    if args.output == '':
        plt.show()
    else:
        out_file_path = os.path.join(os.path.dirname(args.file_path), args.output)
        fig.savefig(out_file_path, bbox_extra_artists=extra_artists, bbox_inches='tight')


if __name__ == '__main__':
    main()
