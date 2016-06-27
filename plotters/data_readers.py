import os
import yaml
import fnmatch


def read_from_dir(dir_path):

    """
    returns a dictionary {label : list of dictionaries {'x': [list of values], 'y': [list of values]} }
    """

    files_and_dirs = os.listdir(dir_path)
    files = [f for f in files_and_dirs if os.path.isfile(os.path.join(dir_path, f)) and fnmatch.fnmatch(f, '*-*.log')]


    map_data_to_labels = {}

    for filename in files:
        file_path = os.path.join(dir_path, filename)
        print "input :  {0}".format(file_path)

        with open(file_path, 'r') as in_file:
            yaml_data = in_file.read()


        label = get_label(filename)
        print "label : '{0}'".format(label)

        data = yaml.load(yaml_data)


        data_keyword = 'data'
        if 'velocities' in data[0]:
            data_keyword = 'velocities'
        elif 'sizes' in data[0]:
            data_keyword = 'sizes'


        data_items = [(data_item['generation'], data_item[data_keyword]) for data_item in data]
        data_items = sorted(data_items, key=lambda pair: pair[0])

        generation_num = []
        evaluation_num = []
        max_val = []

        for i in range(len(data_items)):

            gen = data_items[i][0]
            data_points = data_items[i][1]
            generation_num.append(gen+1)
            evaluation_num.append((gen+1) * len(data_points))
            max_val.append(max(data_points) * 100.0)

        if label not in map_data_to_labels:
            map_data_to_labels[label] = []

        map_data_to_labels[label].append({'x': evaluation_num, 'y': max_val})

    return map_data_to_labels




def read_fitness_from_file(file_path):

    """
    returns dictionary with following keys:
    'gen', 'eval', max', 'min', 'mean', 'median'
    """

    with open(file_path, mode='r') as vel_file:
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

    return {
        'gen': generation_num,
        'eval': evaluation_num,
        'max': max_val,
        'min': min_val,
        'mean': mean_val,
        'median': med_val
        }




def read_sizes_from_file(file_path):

    """
    returns dictionary with following keys:
    'gen', 'eval', max', 'min', 'best', 'worst'
    """

    with open(file_path, mode='r') as vel_file:
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
        sizes = data_items[i][1]

        generation_num.append(gen+1)
        evaluation_num.append((gen+1) * len(sizes))


        max_val.append(max(sizes))
        min_val.append(min(sizes))
        best_val.append(sizes[0])
        worst_val.append(sizes[-1])

    return {
        'gen': generation_num,
        'eval': evaluation_num,
        'max': max_val,
        'min': min_val,
        'best': best_val,
        'worst': worst_val
        }




def get_label(filename):
    words = filename.split('-')
    del words[-1]
    label = ""
    for word in words:
        label += word
        label += "-"
    # chop off last dash
    return label[:-1]


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