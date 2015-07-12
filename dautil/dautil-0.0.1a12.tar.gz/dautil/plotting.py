from itertools import cycle


def embellish(axes, legends=None):
    for i, ax in enumerate(axes):
        ax.grid(True)

        if legends is None:
            ax.legend(loc='best')
        elif i in legends:
            ax.legend(loc='best')


def hide_axes(axes):
    if len(axes) > 0:
        flat_axes = axes.ravel()
    else:
        axes = flat_axes

    for ax in flat_axes:
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)


class CyclePlotter():
    def __init__(self, ax):
        self.STYLES = cycle(["-", "--", "-.", ":"])
        self.LW = cycle([1, 2])
        self.ax = ax

    def plot(self, x, y, *args, **kwargs):
        self.ax.plot(x, y, next(self.STYLES),
                     lw=next(self.LW), *args, **kwargs)
