import yaml
import random
import os
import fnmatch
from argparse import ArgumentParser
from matplotlib import pyplot as plt
import matplotlib.lines as mlines
import matplotlib.colors as colors
import matplotlib.cm as cmx


parser = ArgumentParser()

parser.add_argument('dir_path', metavar='DIR', type=str, help="Path to a genotype directory")
parser.add_argument('-o', '--output', type=str, default='.', help='Output directory name')


def main():
    args = parser.parse_args()

    dir_path = args.dir_path
    out_dir_path = os.path.join(dir_path, args.output)

    neuron_file_path = os.path.join(out_dir_path, 'num_neurons.log')
    connection_file_path = os.path.join(out_dir_path, 'num_connections.log')

    files_and_dirs = os.listdir(dir_path)
    files = [f for f in files_and_dirs if os.path.isfile(os.path.join(dir_path, f)) and
             fnmatch.fnmatch(f, 'gen_*_genotypes.log')]

    files = sorted(files, key=lambda item: int(item.split('_')[1]))

    generation_nums = []
    # eval_nums = []

    # best_neurons = []
    # best_connections = []

    # worst_neurons = []
    # worst_connections = []

    # max_neurons = []
    # max_connections = []

    # min_neurons = []
    # min_connections = []


    # with open(out_file_path, 'w+') as out_file:
    #     out_file.write("generation,evaluation,neurons,connections\n")

    for filename in files:
        file_path = os.path.join(dir_path, filename)
        print "input :  {0}".format(file_path)


        with open(file_path, 'r') as in_file:
            yaml_data = in_file.read()
        data = yaml.load(yaml_data)
        num_brains = len(data)

        num_neurons = []
        num_connections = []

        for br in data:
            num_neurons.append(len(br['neurons']))
            num_connections.append(len(br['connections']))


        # best_brain = data[0]
        # worst_brain = data[-1]

        gen_num = int(filename.split('_')[1])
        # eval_num = gen_num * num_brains
        print "size: {0}".format(num_brains)
        print "generation: {0}".format(gen_num)

        # best_neurons.append(len(best_brain['neurons']))
        # best_connections.append(len(best_brain['connections']))

        # worst_neurons.append(len(worst_brain['neurons']))
        # worst_connections.append(len(worst_brain['connections']))

        # max_neurons.append(max(num_neurons))
        # min_neurons.append(min(num_neurons))

        # max_connections.append(max(num_connections))
        # min_connections.append(min(num_connections))

        generation_nums.append(gen_num)
        # eval_nums.append(eval_num)

        # produce output yaml:

        neuron_string = "- generation: {0}\n  sizes:\n".format(gen_num)
        connection_string = "- generation: {0}\n  sizes:\n".format(gen_num)

        for num_n in num_neurons:
            neuron_string += "  - {0}\n".format(num_n)
        for num_c in num_connections:
            connection_string += "  - {0}\n".format(num_c)

        with open(neuron_file_path, 'a') as n_file:
            n_file.write(neuron_string)

        with open(connection_file_path, 'a') as c_file:
            c_file.write(connection_string)


            # out_file.write("{0},{1},{2},{3}\n".format(gen_num, eval_num, num_neurons, num_connections))


if __name__ == '__main__':
    main()
