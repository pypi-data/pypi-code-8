from argparse import ArgumentParser
from gooey import GooeyParser, Gooey

@Gooey( required_cols= 2)
def main():
    desc = '''
    This program models the light profile of a galaxy in a fits image using a Mixture-of-Gaussian model. It can use either MCMC or non-linear least squares.
    '''

    parser = ArgumentParser(description = desc)

    parser.add_argument(
        'filename',
        metavar = 'filename',
        type = str,
        help = 'Either a fits filename or a directory of files.\n NOTE: The GUI will not allow you to choose a directory. Choose a file and edit the text.')

    parser.add_argument(
        'centers',
        metavar = 'centers',
        type=str,
        help = 'Either a filename or a comma separate pair of coordinates for x,y.')

    parser.add_argument(
        'output',
        metavar = 'output',
        type = str,
        help = 'Location to store the programs output.')

    parser.add_argument(
        'modeler',
        metavar = 'modeler',
        type = str,
        choices = ['MCMC', 'NLSQ'],
        help = 'Modeler used to perform fit. Either MCMC or NLSQ.')


    p = parser.parse_args()

    print p


if __name__ == '__main__':
    main()
