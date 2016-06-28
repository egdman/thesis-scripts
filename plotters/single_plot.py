from .batch_plot import plot_raw
from .common import get_default_styles, get_default_colors



def plot_single(axes, args, xdata, ydata, data_labels, xlabel, ylabel, colors=None, styles=None):
	
    if len(ydata) != len(data_labels):
    	print "Error: Number of plots must be equal to number of data labels"
    	return None

    if styles is None:
        styles = get_default_styles(data_labels)
  

    if colors is None:
        colors = get_default_colors(data_labels)
      

    data_map = {data_labels[i]: [{'x': xdata, 'y': ydata[i]}] for i in range(len(ydata))}
    

    extra_artists = plot_raw(axes, args,
        sorted_labels=data_labels,
        map_data_to_labels=data_map,
        color_to_label=colors,
        style_to_label=styles,
        xlabel=xlabel,
        ylabel=ylabel
    )

   
    return extra_artists

