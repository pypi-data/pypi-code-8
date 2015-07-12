import os as _os
on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:
    import matplotlib.pyplot as _plt
    from matplotlib import gridspec as _gridspec


def setup_figure(gridspec_x=1, gridspec_y=1):
    """
    Returns :code:`fig, gs`:

    * *fig*: :class:`matplotlib.figure.Figure` instance
    * *gs*: :class:`matplotlib.gridspec.GridSpec` instance with *gridspec_x* rows and *gridspec_y* columns
    """
    fig = _plt.figure()
    gs = _gridspec.GridSpec(gridspec_x, gridspec_y)

    return fig, gs
