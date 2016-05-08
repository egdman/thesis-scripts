import yaml
import os
import fnmatch
from argparse import ArgumentParser


parser = ArgumentParser()

parser.add_argument('dir_path', metavar='DIR', type=str, help='Path to the directory with fitness data')
parser.add_argument('-o', '--output', type=str, default='integrated_fitness.csv', help='output file name')
parser.add_argument('-p', '--pattern', type=str, default='*-*.log', help='input filename pattern')
parser.add_argument('--precise', action='store_true', help='Integrate all velocities instead of just the maximum ones')


def main():
    args = parser.parse_args()

    input_dir_path = args.dir_path
    output_file_path = os.path.join(input_dir_path, args.output)

    files_and_dirs = os.listdir(input_dir_path)
    filenames = [f for f in files_and_dirs if os.path.isfile(os.path.join(input_dir_path, f)) and
            fnmatch.fnmatch(f, args.pattern)]
   

    data_to_labels = {}
    label_set = set()
    for filename in filenames:
        label = filename.split('-')[-2]
        label = float(label)
        label_set.add(label)
        if label not in data_to_labels:
            data_to_labels[label] = []

        data_to_labels[label].append(filename)
    
    labels_sorted = sorted(list(label_set))
    
    
    # with open(output_file_path, 'w') as out_file:
    #     out_file.write(labels_sorted[0])
    #     first = True
    #     for label in labels_sorted:
    #         if not first:
    #             out_file.write(",{0}".format(label))
    #         first=False

    max_lists_to_labels = {}

    for label in data_to_labels:
        max_lists_to_labels[label] = []

    # find the smallest number of evaluations to trim all data:
    min_eval_num = 88888888

    for label in labels_sorted:
        label_fnames = data_to_labels[label]
        for fname in label_fnames:
            print "input: {0}".format(fname)

            with open(os.path.join(input_dir_path, fname), 'r') as in_file:
                yaml_data = in_file.read()
            data = yaml.load(yaml_data)
            part_sum_list = []
            eval_num = 0
            for data_item in data:
                velocities = data_item['velocities']
                eval_num += len(velocities)

                if args.precise:
                    part_sum = 0
                    for vel in velocities:
                        part_sum += vel

                    part_sum_list.append((len(velocities), part_sum))

                else:
                    max_velo = max(velocities)
                    part_sum_list.append((len(velocities), max_velo*len(velocities)))

            max_lists_to_labels[label].append(part_sum_list)
            print "{0} evaluations".format(eval_num)
            if eval_num < min_eval_num:
                min_eval_num = eval_num


    print "trimming data to {0} evaluations".format(min_eval_num)

    # integrate and write results to file:
    with open(output_file_path, 'w+') as out_file:
        for label in labels_sorted:
            out_file.write(str(label))
            for lst in max_lists_to_labels[label]:
                sum = 0
                eval_num = 0
                index = 0
                while eval_num < min_eval_num:
                    eval_num += lst[index][0]
                    sum += lst[index][1]
                    index += 1
                out_file.write(",{0}".format(sum))
            out_file.write("\n")





if __name__ == '__main__':
    main()








