import os
from argparse import ArgumentParser
from matplotlib import pyplot as plt

parser = ArgumentParser("plot_trajectory.py")

parser.add_argument('file_path', metavar='PATH', type=str, help="Path to a trajectory file")
parser.add_argument('-t', '--title', type=str, default='plot title', help='Title of the plot')
parser.add_argument('-o', '--output', type=str, default='', help='Output file name')


def main():
    args = parser.parse_args()

    fig = plt.figure(figsize=(16, 16))
    axes = fig.add_subplot(111)
    axes.set_aspect('equal', 'datalim')
    axes.tick_params(labelsize=30)
    axes.set_title(args.title, fontsize=40, y=1.02)
    xartist = axes.set_xlabel('x, cm', fontsize=40)
    yartist = axes.set_ylabel('y, cm', fontsize=40)

    axes.grid()


    dir_path = os.path.dirname(args.file_path)
    out_file_path = os.path.join(dir_path, args.output)

    with open(args.file_path, 'r') as in_file:
        x1=x2=0
        y1=y2=0
        for line in in_file:
            words = line.split(',')

            x1 = float(words[0])
            y1 = float(words[1])

   #         axes.plot([x2,x1], [y2,y1], linewidth=1, linestyle = "-",color = 'red', ms=10, markevery=100)

            x2 = float(words[2])
            y2 = float(words[3])
    
            axes.plot([x1,x2], [y1,y2], linewidth=1, linestyle = "-",color = 'green', ms=10, markevery=100)


    if args.output == '':
        fig.show()
    else:
        fig.savefig(out_file_path, bbox_extra_artists=(xartist, yartist), bbox_inches='tight')


if __name__ == '__main__':
    main()
