from __future__ import print_function

import csv
import matplotlib.pyplot as plt
import random as rd
import sys
from scipy import stats


def expressPull(file_list, mean_values, set_list):
    '''
    Pulls expression values for a defined list of specific genes.
    Each gene is displayed along with the value for every array.
    '''

    # Creates a dictionary with normalized values for the dataset.
    def norm_dict(array, gene):
        array_name = {genes: values for genes, values in
                      zip([v for i, (j, k) in set_list[array - 1:array]
                           for v in j], mean_values)}
        return round(array_name.get(gene, 0), 3)

    # Pulls normalized expression values for putative genes for all arrays.
    genes_of_interest = ['ERG', 'ETV1', 'ETV4', 'ETV5']
    for gene in genes_of_interest:
        print('\n{}:'.format(gene))
        for i, file in enumerate(file_list, 1):
            print('{}: {}'.format(file, norm_dict(i, gene)))


def graph(file_list, array_final_list, array_values_list):
    '''
    Plots four graphs combined, a box plot and histogram each for both
    values and normalized values.
    '''
    def mean(n):
        return sum(n) / len(n)

    # Computes histogram bin size and number using d' choice.
    def freedDiac(values):
        bin_numbers = []
        for array in values:
            iqr = (stats.scoreatpercentile(array, 75) -
                   stats.scoreatpercentile(array, 25))
            mid = pow(len(array), -(1.0/3.0))
            bin_size = 2*iqr*mid
            L = max(array) - min(array)
            bin_number = (L/bin_size)
            bin_numbers.append(bin_number)
        bin_number = round(mean(bin_numbers), 0)
        return bin_number

    bin_number = freedDiac(array_values_list)

    # Plot an overlayed histogram of raw data.
    fig = plt.figure(figsize=(12, 12))
    fig.add_subplot(221)

    array_graph_list_raw = [[i for i in array_value] for array_value in
                            array_values_list]

    color_list = [tuple((rd.uniform(0, 1), rd.uniform(0, 1),
                         rd.uniform(0, 1))) for i in range(0, len(file_list))]

    for graph, color, file in zip(array_graph_list_raw, color_list,
                                  file_list):
        plt.hist(graph, bins=bin_number, histtype='stepfilled',
                 normed=True, color=color, alpha=0.5, label=file)

    plt.title('Microarray Expression Frequencies')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.legend()

    # Plot an overlayed histogram of normalized data.
    fig.add_subplot(222)
    array_graph_list = [[j for i, j in array_final] for array_final in
                        array_final_list]

    for graph, color, file in zip(array_graph_list, color_list, file_list):
        plt.hist(graph, bins=bin_number, histtype='stepfilled',
                 normed=True, color=color, alpha=0.5, label=file)

    plt.title('Microarray Expression Frequencies (normalized)')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.legend()

    # Plot box plots of raw data.
    fig.add_subplot(223)
    plt.title('Microarray Expression Values')
    plt.hold = True
    boxes = [graph for graph in array_graph_list_raw]
    plt.boxplot(boxes, vert=1)

    # Plot box plots of normalized data.
    fig.add_subplot(220)
    plt.title('Microarray Expression Values (normalized)')
    plt.hold = True
    boxes = [graph for graph in array_graph_list]
    plt.boxplot(boxes, vert=1)

    plt.savefig('figures.pdf')
    plt.savefig('figures.png')


def main():
    if (len(sys.argv) > 1):
        file_paths = sys.argv[1:]
    else:
        print('Usage: quantile_normalization.py csv_files')
        sys.exit()

    # Parse csv files for arrays, creating lists of gene names and expression
    # values.
    set_dict = {}
    for path in file_paths:
        with open(path) as stream:
            has_header = csv.Sniffer().has_header(stream.read(1024))
            stream.seek(0)
            if has_header:
                next(stream)
                data = list(csv.reader(stream, delimiter='\t'))
            else:
                data = list(csv.reader(stream, delimiter='\t'))
        data = sorted([(i, float(j)) for i, j in data], key=lambda v: v[1])
        array_genes = [i for i, j in data]
        array_values = [j for i, j in data]
        set_dict[path] = (array_genes, array_values)

    quantileNorm(set_dict, file_paths)


def quantileNorm(set_dict, file_paths):
    '''
    Makes the distribution for each array statistically identical.
    '''

    # Create sorted list of genes and values for all datasets.
    set_list = [x for x in set_dict.items()]
    set_list.sort(key=lambda (x, y): file_paths.index(x))
#    set_list = [x for x in list(set_dict.items())] # Python 3.3
#    set_list.sort(key = lambda x_y: file_paths.index(x_y[0])) # Python 3.3

    # Compute row means.
    L = len(file_paths)
    all_sets = [[i] for i in set_list[0:L+1]]
    array_values_list = [[v for i, (j, k) in A for v in k] for A in all_sets]
    mean_values = [sum(p) / L for p in zip(*array_values_list)]

    # Provide corresponding gene names for mean values and replace original
    # data values by corresponding means.
    array_genes_list = [[v for i, (j, k) in A for v in j] for A in all_sets]
    array_final_list = [sorted(zip(sg, mean_values)) for sg in
                        array_genes_list]

    # Truncate full path name to yield filename only.
    file_list = [file[file.rfind('/') + 1:file.rfind('.csv')] for file in
                 file_paths]

    expressPull(file_list, mean_values, set_list)

    graph(file_list, array_final_list, array_values_list)


if __name__ == '__main__':
    main()
