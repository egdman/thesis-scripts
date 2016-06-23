from matplotlib import pyplot as plt
from argparse import ArgumentParser
import os

parser = ArgumentParser()
parser.add_argument('file_path', metavar='FILE', type=str, help="Path to a signal file")
parser.add_argument('-o', '--output', type=str, default='plot', help='Output file name')

parser.add_argument('--xlim', type=float, default=0.0, help='X axis limit')

def main():
	args = parser.parse_args()
	in_path = args.file_path

	base_path = os.path.dirname(in_path)

	out_path = os.path.join(base_path, args.output)

	labels = {}

	step = 0

	with open(in_path, "r") as in_file:
		for line in in_file:

			words = line.split(',')

			label = words[0]
			value = float(words[1])

			if label not in labels:
				labels[label] = ([], [])

			labels[label][0].append(step)
			labels[label][1].append(value)

			step += 1


	fig = plt.figure(figsize=(15, 10))
	ax = fig.add_subplot(111)

	for label in labels:
		data = labels[label]

		ax.plot(data[0], data[1], label=label)

	if args.xlim > 0.0:
		ax.set_xlim(0, args.xlim)
		
	plt.savefig(out_path)




if __name__ == '__main__':
	main()