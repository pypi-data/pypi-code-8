def scatterplot(inst, start, stop, labelx, labely, data_label, datalim, xlim=None, ylim=None):
    """Return a scatterplot over a season.

    Arguments:
        Start: Start Date(s) - datetime object
        Stop: Stop Date(s) - datetime object
        labelx: string identifying data product for x-axis
        labely: string identifying data product for y-axis
        data_label: string identifying data product to be scatter plotted
        datalim: np array with plot limits for data_label

    Summary:
        Returns a scatter plot of data_label as a function of label1 and label2 over the season delineated by start and stop datetime objects."""

    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import cm
    import matplotlib.colors as colors

    #interactive plotting off
    plt.ioff()
    
    # do loop to iterate over given days
    # start data in start, end day in stop
    season = pysat.getDateArray(start, stop, freq='D')
    
    #create figures for plotting
    figs = []
    axs = []
    
    #check if doing multiple data quantities
    if type(data_label) is str:
        #max of one data type
        figs.append( plt.figure() )
        ax1 = figs[0].add_subplot(211, projection='3d')
        ax2 = figs[0].add_subplot(212)
        axs.append((ax1, ax2))
        plt.suptitle(data_label)
        if xlim is not None:
            ax1.set_xlim(xlim)
	    ax2.set_xlim(xlim)	
        if ylim is not None:
            ax1.set_ylim(ylim)
	    ax2.set_ylim(ylim)	
        data_label = [data_label]
        plt.hold(True)
    else:
        #multiple data to be plotted
        for i in np.arange(len(data_label)):
            figs.append( plt.figure() )
            ax1 = figs[i].add_subplot(211, projection='3d')
            ax2 = figs[i].add_subplot(212)
            axs.append((ax1, ax2))
            #axs.append( figs[i].add_subplot(111, projection='3d') )
            plt.suptitle(data_label[i])              
            if xlim is not None:
               ax1.set_xlim(xlim)
	       ax2.set_xlim(xlim)
            if ylim is not None:
               ax1.set_ylim(ylim)
	       ax2.set_ylim(ylim)
            plt.hold(True)
                
                
    #norm method so that data may be scaled to colors appropriately
    norm = colors.Normalize(vmin=datalim[0], vmax=datalim[1])    
    p=[i for i in np.arange(len(figs))]    
    for i,date in enumerate(season):
        #load data
        inst.getData(date=date)
        for j, (fig, ax) in enumerate(zip(figs, axs)):
            if len(inst.data) > 0:
                if ((len(inst.data[labelx]) > 0) & (len(inst.data[labely]) > 0) & (len(inst.data[data_label[j]]) > 0)):
                    p[j]=ax[0].scatter(inst.data[labelx], inst.data[labely], inst.data[data_label[j]], zdir='z', c=inst.data[data_label[j]], cmap=cm.jet, norm=norm, linewidth='0', edgecolors=None)
                    ax[1].scatter(inst.data[labelx], inst.data[labely], c=inst.data[data_label[j]], cmap=cm.jet, norm=norm, linewidth=0.00000000001, alpha=0.5, edgecolor=None)
                
    for j, (fig, ax) in enumerate(zip(figs, axs)):
	try:
            cbar = plt.colorbar(p[j],ax=ax[0], label='Amplitude (m/s)')
        except:
            print 'Tried colorbar but failed, thus no colorbar.'
        ax[0].elev=30.
    #interactive plotting back on    
    plt.ion()
    
    return figs