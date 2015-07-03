__all__ = ['E200_dataset2str']


def E200_dataset2str(dataset):
    return ''.join(dataset.view('S2'))
