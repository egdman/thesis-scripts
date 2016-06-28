from .common import set_axes_limits, MARKERSIZE


def plot_raw(axes, args, sorted_labels, map_data_to_labels, color_to_label, style_to_label, xlabel, ylabel, thickness=3):

	title_size = args.title_size
	label_size = args.label_size
	tick_size = args.tick_size

	for label in sorted_labels:
		graphs = map_data_to_labels[label]

		for graph in graphs:
		    axes.plot(graph['x'], graph['y'], linewidth=thickness,
		            label=label, color=color_to_label[label],
		            linestyle=style_to_label[label][0],
		            marker=style_to_label[label][1],
		            markersize=MARKERSIZE)

	axes.tick_params(axis='both', which='major', labelsize=tick_size)
	axes.set_title(args.title, fontsize=title_size, y=1.02)
	xartist = axes.set_xlabel(xlabel, fontsize=label_size)
	yartist = axes.set_ylabel(ylabel, fontsize=label_size)

	set_axes_limits(axes, args)

	return [xartist, yartist]



def plot_average(axes, args, sorted_labels, map_data_to_labels, color_to_label, style_to_label, xlabel, ylabel):

	title_size = args.title_size
	label_size = args.label_size
	tick_size = args.tick_size

	for label in sorted_labels:
		graphs = map_data_to_labels[label]
		graph_lengths = [len(graph['x']) for graph in graphs]
		mean_y = []

		num_graphs = len(graphs)
		num_points = min(graph_lengths)

		print "for label '{0}'".format(label)
		print "{0} graphs\n{1} points".format(num_graphs, num_points)

		for i in range(num_points):
		    sum = 0
		    for graph in graphs:
		        sum += graph['y'][i]
		    sum = sum / float(num_graphs)
		    mean_y.append(sum)



		axes.plot(graphs[0]['x'][:num_points], mean_y, linewidth=3,
	            label=label, color=color_to_label[label],
	            linestyle=style_to_label[label][0],
	            marker=style_to_label[label][1],
	            markersize=MARKERSIZE)


	axes.tick_params(axis='both', which='major', labelsize=tick_size)
	axes.set_title(args.title, fontsize=title_size, y=1.02)
	xartist = axes.set_xlabel(xlabel, fontsize=label_size)
	yartist = axes.set_ylabel(ylabel, fontsize=label_size)

	set_axes_limits(axes, args)

	return [xartist, yartist]