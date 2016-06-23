import os
import yaml

from matplotlib import pyplot as plt
from plotters import parser, plot_single


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

    fig = plt.figure(figsize=(args.horsize,args.vertsize))
    ax = fig.add_subplot(111)

    extra_artists = plot_single(ax, args, xdata=evaluation_num,
        ydata=[max_val, best_val, worst_val, min_val],
        data_labels=["max", "best", "worst", "min"],
        xlabel="evaluation #",
        ylabel=y_axis_label)

    ax.grid()

    if args.output == '':
        plt.show()
    else:
        out_file_path = os.path.join(os.path.dirname(args.file_path), args.output)
        fig.savefig(out_file_path, bbox_extra_artists=extra_artists, bbox_inches='tight')


if __name__ == '__main__':
    main()
