# -*- coding: utf-8 -*-
"""
Methods to create useful graphs for ploting distributions o single variables. Methods included:

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
    """ Return a Pandas series with the percents of each category, indexed by the categries names """
    counts = series.value_counts()
    porcentagens = 100 * (counts / sum(counts))
    return porcentagens


def plot_bar_chart(data, cmap='Accent', color=None, xlabel='', ylabel='', title='', width=0.9, xticks_rotation=0, series_legends=None, ax=None):
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
        
    # Determine series type (pandas can represent categorical data with at least three different classes!)
    first_series = data[0]   
  
    # If the Series is of "objects" (usually strings)
    if first_series.dtype == 'O':
        
        # Get list of different strings
        categorias = np.unique(data)
        
    # If it is a series create by pd.Series([...], dtype='category') or equivalent (e.g. pd.Series(pd.Categorical([...], [...])) )
    elif first_series.dtype == 'category':             
        
        # Get list of categories
        categorias = data[0].cat.categories # We assume here that the first series has all categories (BUG: it can be wrong!!!)
        
    else:
        raise Exception('Invalid data type %s' % data[0].dtype )
    
    # Number of different categories
    num_de_categorias = len(categorias)
    
    # Number of series
    num_de_series = len(data)
    
    # Colormap to use in the graph
    colors = plt.cm.get_cmap(cmap, num_de_series)     
    
    # Position of each category
    x_locations = np.arange(num_de_categorias) * num_de_series
    
    # Create figure
    if ax == None:
        fig, ax = plt.subplots()
    
    # Create series names, if not provided    
    if series_legends == None:    
        series_legends = ['Series %i' % i for i in range(1, num_de_series + 1)]    
    
    # For each series
    for idx, series in enumerate(data):
               
        # Compute the porcentage of each category
        porcentagens = _get_percentage_of_categorical(series)      
        porcentagens = porcentagens[categorias] # Assure that percentages will be returned in the same order as the legend
        
        # Determine color to use in this series
        new_color = color if color != None else colors(idx)      
        print idx, color
        
        # Plot bars
        ax.bar(x_locations + idx*width, porcentagens, width, color=new_color, label=series_legends[idx])

    # Plot title and axis labels
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.set_title(title)    
            
    # If there is more than one series
    if num_de_series > 1:
        
        # Show legend
        ax.legend(loc='best')
        
        # Draw categories names
        #...        
        
    # If there is just one series
    else:
        
        # Draw categories names
        ax.set_xticks(x_locations + width/2)
        ax.set_xticklabels(categorias, rotation=xticks_rotation)
    
    
    # Add some small gap before the first and after the last category
    ax.set_xlim(min(x_locations) - width/9, max(x_locations) + width*num_de_series + width/9)

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
    
   # Test series with categorical data
   d1 = pd.Series(pd.Categorical(['c', 'a', 'c', 'a', 'c', 'b'], ['c','b','a']))
   plot_bar_chart(d1)
   
   # Test series with string data
   d2 = pd.Series(['b', 'b', 'b', 'a', 'b', 'c'])
   plot_bar_chart(d2)
   
   # Test both series at the same time
   plot_bar_chart([d1, d2])
        