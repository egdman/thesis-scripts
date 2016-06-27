import matplotlib.lines as mlines

MARKERSIZE = 6


# def mean(values_list):
#     return float(sum(values_list)) / float(len(values_list)) if len(values_list) > 0 else float('nan')



def plot_raw(axes, args, sorted_labels, map_data_to_labels, color_to_label, style_to_label, xlabel, ylabel):

	title_size = args.title_size
	label_size = args.label_size
	tick_size = args.tick_size
	legend_size = args.legend_size

	for label in sorted_labels:
		graphs = map_data_to_labels[label]

		for graph in graphs:
		    axes.plot(graph['x'], graph['y'], linewidth=2,
		            label=label, color=color_to_label[label],
		            linestyle=style_to_label[label][0],
		            marker=style_to_label[label][1],
		            markersize=MARKERSIZE)

	hnd, lab = get_handles_labels(sorted_labels, color_to_label, style_to_label)
	lgd = axes.legend(hnd, lab, loc=0, prop={'size': legend_size}, framealpha=0.5)
	if args.legend_title is not None:
	    lgd.set_title(args.legend_title, prop={'size': legend_size})

	axes.tick_params(axis='both', which='major', labelsize=tick_size)
	axes.set_title(args.title, fontsize=title_size, y=1.02)
	xartist = axes.set_xlabel(xlabel, fontsize=label_size)
	yartist = axes.set_ylabel(ylabel, fontsize=label_size)

	if args.ylim_min is not None and args.ylim_max is not None:
	    axes.set_ylim(args.ylim_min, args.ylim_max)

	if args.xlim_min is not None and args.xlim_max is not None:
	    axes.set_xlim(args.xlim_min, args.xlim_max)

	return [xartist, yartist]



def plot_average(axes, args, sorted_labels, map_data_to_labels, color_to_label, style_to_label, xlabel, ylabel):

	title_size = args.title_size
	label_size = args.label_size
	tick_size = args.tick_size
	legend_size = args.legend_size

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

	hnd, lab = get_handles_labels(sorted_labels, color_to_label, style_to_label)
	lgd = axes.legend(hnd, lab, loc=0, prop={'size': legend_size}, framealpha=0.5)
	if args.legend_title is not None:
	    lgd.set_title(args.legend_title, prop={'size': legend_size})

	axes.tick_params(axis='both', which='major', labelsize=tick_size)
	axes.set_title(args.title, fontsize=title_size, y=1.02)
	xartist = axes.set_xlabel(xlabel, fontsize=label_size)
	yartist = axes.set_ylabel(ylabel, fontsize=label_size)


	if args.ylim_min is not None and args.ylim_max is not None:
	    axes.set_ylim(args.ylim_min, args.ylim_max)

	if args.xlim_min is not None and args.xlim_max is not None:
	    axes.set_xlim(args.xlim_min, args.xlim_max)

	return [xartist, yartist]



def get_handles_labels(ordered_labels, color_to_label, style_to_label=None):

    legend_handles = []
    legend_labels = []
    for label in ordered_labels:
        color = color_to_label[label]

        if style_to_label is not None:
            style = style_to_label[label]
        else:
            style = ('-', '')

        hnd = mlines.Line2D([],[], color=color,
            linestyle=style[0],
            marker=style[1],
            markersize=MARKERSIZE,
            linewidth=5)

        legend_handles.append(hnd)
        legend_labels.append(label)
    return legend_handles, legend_labels