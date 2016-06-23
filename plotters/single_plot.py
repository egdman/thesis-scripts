def plot_single(axes, args, xdata, ydata, data_labels, xlabel, ylabel):
	
    if len(ydata) != len(data_labels):
    	print "Error: Number of plots must be equal to number of data labels"
    	return None

    title_size = args.title_size
    label_size = args.label_size
    tick_size = args.tick_size
    legend_size = args.legend_size

    ax = axes
    styles = ['--', '-', ':', '--']
    colors = ['red', 'green', 'black', 'blue']

    for i in range(len(ydata)):
    	ax.plot(xdata, ydata[i], linewidth=3, label=data_labels[i], linestyle=styles[i%4],
    		color=colors[i%4], ms=10, markevery=100)


    ax.legend(loc=0, prop={'size': legend_size})

    ax.tick_params(axis='both', which='major', labelsize=tick_size)
    ax.set_title(args.title, fontsize=title_size, y=1.02)
    xartist = ax.set_xlabel(xlabel, fontsize=label_size)
    yartist = ax.set_ylabel(ylabel, fontsize=label_size)

    if args.ylim_min is not None or args.ylim_max is not None:
        ax.set_ylim(args.ylim_min, args.ylim_max)

    # ax.grid()
    return [xartist, yartist]