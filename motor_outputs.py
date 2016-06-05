from matplotlib import pyplot as plt
from argparse import ArgumentParser
import os

parser = ArgumentParser()

parser.add_argument('dir_path', metavar='DIR', type=str, help="Path to a fitness log file")
parser.add_argument('-t', '--title', type=str, default='plot title', help='Title of the plot')
parser.add_argument('-o', '--output', type=str, default='plot', help='Output file name')

parser.add_argument('--title-size', type=float, default=42, help='text size for the title')
parser.add_argument('--label-size', type=float, default=40, help='text size for the axis labels')
parser.add_argument('--legend-size', type=float, default=30, help='text size for the legend')
parser.add_argument('--tick-size', type=float, default=30, help='text size for the ticks')

parser.add_argument('--horsize', type=float, default=14, help='horizontal size of the image')
parser.add_argument('--vertsize', type=float, default=8, help='vertical size of the image')

parser.add_argument('--ylim-min', type=float, help='min Y axis limit')
parser.add_argument('--ylim-max', type=float, help='max Y axis limit')

parser.add_argument('--time-lim', type=float, default=15.0, help='time limit')
parser.add_argument('--max-signal', type=float, default=10000.0, help='max signal level to normalize')



def main():
	args = parser.parse_args()

	title_size = args.title_size
	label_size = args.label_size
	tick_size = args.tick_size
	legend_size = args.legend_size
	max_sig = args.max_signal

	dir_path = args.dir_path

	out_file_path = os.path.join(dir_path, args.output)

	files_and_dirs = os.listdir(dir_path)
	filenames = [f for f in files_and_dirs if os.path.isfile(os.path.join(dir_path, f)) and \
		f.split('.')[-1] == 'log']

	labels = [filename.split('.')[0] for filename in filenames]

	fig = plt.figure(figsize=(args.horsize, args.vertsize))
	ax = fig.add_subplot(111)


	for i in range(len(filenames)):
		label = labels[i]
		filename = filenames[i]

		file_path = os .path.join(dir_path, filename)
		print "input :  {0}".format(file_path)
		time_list = []
		sig_list = []
		with open(file_path, 'r') as in_file:
			for line in in_file:
				words = line.split(',')

				time = float(words[0])
				signal = float(words[1]) / max_sig

				if time > args.time_lim:
					break

				time_list.append(time)
				sig_list.append(signal)

		ax.plot(time_list, sig_list)

	# ax.set_ylim(-1.5, 1.5)
	ax.set_title(args.title, fontsize=title_size, y=1.02)
	plt.savefig(out_file_path)



if __name__ == '__main__':
	main()