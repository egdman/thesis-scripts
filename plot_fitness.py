import os
import yaml

from matplotlib import pyplot as plt
from plotters import parser, plot_single


parser.add_argument('file_path', metavar='PATH', type=str, help="Path to a fitness log file")


def mean(values_list):
    return float(sum(values_list)) / float(len(values_list)) if len(values_list) > 0 else float('nan')

def median(values_list):
    num = len(values_list)
    if num % 2 == 0:
        val1 = values_list[num/2 - 1]
        val2 = values_list[num/2]
        median = float(val1 + val2) / 2.0
    else:
        median = values_list[(num-1) / 2]
    return median


def main():
    args = parser.parse_args()

    with open(args.file_path, mode='r') as vel_file:
        yaml_data = vel_file.read()

    data = yaml.load(yaml_data)

    data_items = [(data_item['generation'], data_item['velocities']) for data_item in data]

    data_items = sorted(data_items, key=lambda pair: pair[0])

    generation_num = []
    evaluation_num = []
    mean_val = []
    st_dev = []
    med_val = []
    max_val = []
    min_val = []

    eval_num_all = []
    fit_val_all = []

    for i in range(len(data_items)):

        gen = data_items[i][0]

        # multiply by 100 to convert to cm/s
        velocities = [value*100.0 for value in data_items[i][1]]

        generation_num.append(gen+1)

        evaluation_num.append((gen+1) * len(velocities))

        mean_val.append(mean(velocities))
        max_val.append(max(velocities))
        min_val.append(min(velocities))
        med_val.append(median(velocities))

    
    fig = plt.figure(figsize=(args.horsize,args.vertsize))
    ax = fig.add_subplot(111)


    extra_artists = plot_single(ax, args, xdata=evaluation_num,
        ydata=[max_val, mean_val, med_val, min_val],
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
