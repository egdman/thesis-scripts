import os
import yaml
from argparse import ArgumentParser
from matplotlib import pyplot as plt

parser = ArgumentParser("plot_fitness.py")

parser.add_argument('file_path', metavar='PATH', type=str, help="Path to a fitness log file")
parser.add_argument('-t', '--title', type=str, default='plot title', help='Title of the plot')
parser.add_argument('-o', '--output', type=str, default='', help='Output file name')
parser.add_argument('--ylabel', type=str, help='Y axis label')
parser.add_argument('--all', action='store_true', help='Plot every fitness value')

parser.add_argument('--title-size', type=float, default=42, help='text size for the title')
parser.add_argument('--label-size', type=float, default=40, help='text size for the axis labels')
parser.add_argument('--legend-size', type=float, default=30, help='text size for the legend')
parser.add_argument('--tick-size', type=float, default=30, help='text size for the ticks')

parser.add_argument('--horsize', type=float, default=12, help='horizontal size of the image')
parser.add_argument('--vertsize', type=float, default=12, help='vertical size of the image')

parser.add_argument('--ylim-min', type=float, help='min Y axis limit')
parser.add_argument('--ylim-max', type=float, help='max Y axis limit')


def main():
    args = parser.parse_args()

    title_size = args.title_size
    label_size = args.label_size
    tick_size = args.tick_size
    legend_size = args.legend_size

    input_filename = os.path.basename(args.file_path)

    # derive labl of y axis:
    if args.ylabel is None:
        y_axis_label = "size"
        if "neuron" in input_filename:
            y_axis_label = "number of neurons"
        elif "connection" in input_filename:
            y_axis_label = "number of connections"
    else:
        y_axis_label = args.ylabel



    with open(args.file_path, mode='r') as vel_file:
        yaml_data = vel_file.read()

    data = yaml.load(yaml_data)
    
    data_items = [(data_item['generation'], data_item['sizes']) for data_item in data]

    data_items = sorted(data_items, key=lambda pair: pair[0])

    generation_num = []
    evaluation_num = []
    max_val = []
    min_val = []
    best_val = []
    worst_val = []

    eval_num_all = []
    fit_val_all = []

    for i in range(len(data_items)):

        gen = data_items[i][0]
        velocities = data_items[i][1]

        generation_num.append(gen+1)

        evaluation_num.append((gen+1) * len(velocities))


        max_val.append(max(velocities))
        min_val.append(min(velocities))
        best_val.append(velocities[0])
        worst_val.append(velocities[-1])

        if args.all:
            eval_num_all.extend([num for num in range
                (
                    len(velocities)*(gen),
                    len(velocities)*(gen+1)
                )
            ])
            fit_val_all.extend(reversed(velocities))





        #print(values2)
    fig = plt.figure(figsize=(args.horsize,args.vertsize))
    ax = fig.add_subplot(111)
    ax.plot(evaluation_num, max_val, linewidth=3, label="max", linestyle='--', color = 'red', ms=10, markevery=100)
    ax.plot(evaluation_num, best_val, linewidth=3, label="best", linestyle = "-",color = 'green', ms=10, markevery=100)
    ax.plot(evaluation_num, worst_val, linewidth=3, label="worst", linestyle=':', color = 'black', ms=10, markevery=100)
    ax.plot(evaluation_num, min_val, linewidth=3, label="min", linestyle='--', color = 'blue', ms=10, markevery=100)

    if args.all:
        ax.plot(eval_num_all, fit_val_all, linewidth=1, label="all", alpha=0.3)

#   set size of the legend like this: 'size':number
    ax.legend(loc=0, prop={'size': legend_size})

    ax.tick_params(axis='both', which='major', labelsize=tick_size)
    ax.set_title(args.title, fontsize=title_size, y=1.02)
    xartist = ax.set_xlabel('evaluation #', fontsize=label_size)
    yartist = ax.set_ylabel(y_axis_label, fontsize=label_size)

    if args.ylim_min is not None or args.ylim_max is not None:
        ax.set_ylim(args.ylim_min, args.ylim_max)

    ax.grid()
    if args.output == '':
        plt.show()
    else:
        out_file_path = os.path.join(os.path.dirname(args.file_path), args.output)
        fig.savefig(out_file_path, bbox_extra_artists=(xartist,yartist), bbox_inches='tight')


if __name__ == '__main__':
    main()
