# -*- coding: utf-8 -*-
"""
This modules packages methods to create graphs useful in Exploratory Data Analysis.

Methods included:

 : plot_bar_chart
     Plot barplot showing the distribution of a categorical variable (for one or multiple series of data). 
 
 : plot_dataframe_profile
     Plot a grid of subplots in which each subplot shows the distribution of a variable of the data frame. For
     numerical variabels a histogram is shown. For categorical, a barplot whose bars lengths are proportional
     to the percentage of each category in the column.

"""


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

from matplotlib.gridspec import GridSpec



def _is_numeric(series):
    """ Determine if the pandas.core.series.Series is numeric """
    return series.dtype == 'int' or series.dtype == 'float'
    
def _is_categorical(series):
    """ Determine if the pandas.core.series.Series is categorical """
    return pd.core.categorical._is_categorical(series)
    
def _get_percentage_of_categorical(series):
    """ Return a Pandas series with the percents of each categy, indexed by the categries names """
    counts = series.value_counts()
    porcentagens = 100 * (counts / sum(counts))
    return porcentagens


def plot_bar_chart(data, cmap='Accent', color=None, xlabel='', ylabel='', title='', width=0.9, xticks_rotation=0, series_legends=None, legend=True, ax=None):
    """
    Plot barplot showing the distribution of a categorical variable (for one or multiple series of data). 
    
    Parameters
    ----------
    
        data : list or pandas.core.series.Series
            Pandas series (with categorical data) or list of series. For multiple series, each categories are grouped together.
            
        cmap : matplotlib.colors.LinearSegmentedColormap
            Colormap to use for determing each category color. Defualt is 'Accent'.
            
        color : color to use in the graph (overrides colormap colors). Default is None, which means not to overide colormap colors.
        
        xlabel, ylabel, title : guess what...
        
        width : float
            Width of each bar. Default is 0.9
                    
        xticks_rotation : float
            Degrees to rotate x labels.            
        
        series_legends : list
            Legends to identify each series.
            
        legend : boolean
            Whether to show or not the legend box.
            
        ax : matplotlib.axes_subplots.AxesSubplot
            Axes in which to plot the graph
    
    Returns
    -------
    
        ax : matplotlib.axes_subplots.AxesSubplot
            Axes where the figure has been plotted.
    
    """
    
    # In the case a unique series is passed as parameters, wrap it in a list
    if not isinstance(data, list):
        data = [data]
    
    # Number of series
    num_de_series = len(data)
        
    # Extract categories names (the returned order is the order used for bars)
    categorias = data[0].cat.categories # We assume here that the first series has all categories (BUG: it can be wrong!!!)
    
    # Number of different categories
    num_de_categorias = len(categorias)
    
    # Colormap to use in the graph
    colors = plt.cm.get_cmap(cmap, num_de_series)     
    
    # Position of each category
    x_locations = np.arange(num_de_categorias)
    
    # Create figure
    if ax == None:
        fig, ax = plt.subplots()
    
    # For each series
    for idx, series in enumerate(data):
        
       
        # Compute the porcentage of each category
        porcentagens = _get_percentage_of_categorical(series)      
        porcentagens = porcentagens[categorias] # Assure that percentages will be returned in the same order as the legend
        
        # Determine color to use in this series
        color = color if color != None else colors(idx)        
        
        # Plot bars
        ax.bar(x_locations + idx*width, porcentagens, width, color=color)

    # Plot texts of the graphs
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.set_title(title)
    
    # Add legend
    if legend:
        ax.legend(categorias, loc='best')
            
    # Overwrite legend labels, if as specified
    if series_legends != None:
        ax.set_xticks(x_locations + width/2)
        ax.set_xticklabels(series_legends, rotation=xticks_rotation)
    else:
    # Otherwise, use category names
        ax.set_xticks(x_locations + width/2)
        ax.set_xticklabels(categorias, rotation=xticks_rotation)

    # Add some small gap before the first and after the last category
    ax.set_xlim(min(x_locations) - width/9, max(x_locations) + width + width/9)

    # Return the axes in which the graph was plotted
    return ax

''''''''''''''''''''''''''''''''''''''''''''

def plot_dataframe_profile(data_frame, include_cols=None, exclude_cols=None, shape = None, hspace=0.2, wspace=0.2, xticks_rotation={}, colors={}, color='blue', bins=30):
    """
    Plot a grid of subplots in which each subplot shows the distribution of a variable of the data frame. For
    numerical variabels a histogram is shown. For categorical, a barplot whose bars lengths are proportional
    to the percentage of each category in the column.
    
    The subplots are drawn in the default column order in the dataframe, or in the order specified in include_cols.
    
    Parameters
    ----------
    
        data_frame : pandas.Dataframe
            The Pandas data frame whose columns will be plotted.
            
        include_cols : list
            A list with the column names that should be included in the plot. Default is None, which means all columns. If this
            parameter is used, just the columns specified are included, in the given order.
            
        remove_cols :
            
        shape : tuple
            A (rows, columns) tuples indicating the shape of the grid.
            
        hspace : float
            Vertical space between subplots.
            
        wspace : float
            Horizontal space betwwn subplots.
            
        xticks_rotation : dict
            Dictionary associating column names to xtick label oriantation (in degrees).

        color : str
            Default color name for all graphs.
            
        colors : dict
            Dictionary associating column names to colors (override defaults color).
            
    
    Return
    -------
    
        gs : GridSpec
            Return the GridSpec created with the subplots.
    
    """

    # Keep just specified columns, if it is the case
    if include_cols != None:
        #data_frame = data_frame[include_cols]
        columns_kept = include_cols
    else:
        columns_kept = data_frame.columns
        
    # Remove cols specified
    if exclude_cols != None:
        columns_kept = [x for x in columns_kept if x not in exclude_cols]
            
    # Get number of columns
    num_of_columns = len(columns_kept)
    
    # Get the number of rows and cols
    if shape != None:
        rows, cols = shape  # Unpack tuple passed as parameter
    else:
        
        # Number of columns in the plot (as the square root (rounded) of the number of variables )
        cols = int(math.ceil(math.sqrt(num_of_columns)))             
        
        # Number or rows in the plot (the necessary to put all variables)
        rows = int(math.ceil(num_of_columns / float(cols)))
    
    # Create a grid with rows x cols subplots
    gs = GridSpec(rows, cols, hspace=hspace, wspace=wspace)        
    
    # For each column
    for col_idx, column_name in enumerate(columns_kept):        
        
        # Create the subplot
        ax = plt.subplot(gs[col_idx])        
        
        # Determine the rotation of xticks for this plot                
        rotation = xticks_rotation[column_name] if column_name in xticks_rotation else 0            

        # Determine the color
        new_color = colors[column_name] if column_name in colors else color
        
        # Is is categorical
        if _is_categorical(data_frame[column_name]):                      
            
            # Plot barplot
            plot_bar_chart(data_frame[column_name], ax=ax, legend=False, title=column_name, xticks_rotation=rotation, color=new_color)         
        
        # If is numeric
        if _is_numeric(data_frame[column_name]):
            
            # Calculate the weiths used to transform data in percents
            weigths = (np.zeros_like(data_frame[column_name]) + 100.) / len(data_frame[column_name])
            
            # Plot histogram
            ax.hist(data_frame[column_name], weights=weigths, color=new_color, bins=bins)
            ax.set_title(column_name)
            ax.grid()
            
    # Return the GridSpec with subplots
    return gs

if __name__=='__main__':
    
   
    plot_dataframe_profile(a.df, include_cols=['timestamp','Data','Hora','km',u'Combustível', 'metros'], wspace=0.1, hspace=0.5, xticks_rotation={'Acelerador':90, 'Cabsignal':90}, colors={'Acelerador':'red', 'Cabsignal':'black'})
    #plot_bar_chart(a.df.Acelerador)
    plt.show()
