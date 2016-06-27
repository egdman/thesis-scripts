import os
import yaml

from matplotlib import pyplot as plt
from plotters import parser, plot_single, read_sizes_from_file, read_fitness_from_file


parser.add_argument('size_file', metavar='SIZE_FILE', type=str, help="Path to a size log file")
parser.add_argument('fitness_file', metavar='FITNESS_FILE', type=str, help="Path to a fitness log file")


def main():
	args = parser.parse_args()

	size_data = read_sizes_from_file(args.size_file)
	fitness_data = read_fitness_from_file(args.fitness_file)

	fig = plt.figure(figsize=(args.horsize,args.vertsize))
	ax1 = fig.add_subplot(111)

	extra_artists1 = plot_single(ax1, args, xdata=fitness_data['eval'],
	    ydata=[fitness_data['max']],
	    data_labels=["max velocity"],
	    xlabel="evaluation #",
	    ylabel="movement speed, cm/s")

	ax2 = ax1.twinx()

	extra_artists2 = plot_single(ax2, args, xdata=size_data['eval'],
	    ydata=[size_data['max']],
	    data_labels=["number of neurons"],
	    xlabel="evaluation #",
	    ylabel="number of neurons")


	if args.output == '':
	    plt.show()
	else:
	    out_file_path = os.path.join(os.path.dirname(args.fitness_file), args.output)
	    fig.savefig(out_file_path, bbox_extra_artists=extra_artists1 + extra_artists2, bbox_inches='tight')


if __name__ == '__main__':
	main()

