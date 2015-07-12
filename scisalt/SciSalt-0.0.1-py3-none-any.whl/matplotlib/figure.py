import os as _os
on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:
    from matplotlib.pyplot import figure as _figure


def figure(title=None, **kwargs):
    fig = _figure(**kwargs)
    if title is not None:
        fig.canvas.set_window_title(title)
    return fig
