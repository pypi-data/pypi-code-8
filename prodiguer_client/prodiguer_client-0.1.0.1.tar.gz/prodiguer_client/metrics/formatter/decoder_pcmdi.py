# -*- coding: utf-8 -*-

"""
.. module:: prodiguer_client/metrics/formatter/decoder_pcmdi.py
   :copyright: @2015 IPSL (http://ipsl.fr)
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Decodes metrics in 'pcmdi' format.

.. moduleauthor:: Insitut Pierre Simon Laplace (IPSL)


"""
import os



def _get_variable(fpath):
    """Returns variable name extracted from a metrics filename.

    """
    return os.path.basename(fpath).split("_")[0]


def _get_models(data):
    """Returns set of models defined within an input file.

    """
    result = set()
    for key, val in data.iteritems():
        try:
            val['SimulationDescription']
        except (TypeError, KeyError):
            pass
        else:
            result.add(key)

    return result


def _get_reference_types(data):
    """Returns set of reference types defined within an input file.

    """
    result = set(data['References'].keys())
    if 'default' in result:
        result.add('defaultReference')
        result.remove('default')

    return result


def _get_simulations(data):
    """Returns set of simulations defined within an input file.

    """
    result = set()
    for model in _get_models(data):
        for name in ['Realization', 'SimName']:
            if name in data[model]['SimulationDescription']:
                result.add(data[model]['SimulationDescription'][name])
                break

    return result


def _get_maskings(data):
    """Returns set of regional maskings defined within an input file.

    """
    result = set()
    for model in _get_models(data):
        for reference_type in _get_reference_types(data):
            for simulation in _get_simulations(data):
                result.update(data[model][reference_type][simulation].keys())

    return result


def _get_groups(data, variable):
    """Returns set of metric groups defined within an input file.

    """
    result = []
    for reference_type in _get_reference_types(data):
        for model in _get_models(data):
            for simulation in _get_simulations(data):
                for masking in _get_maskings(data):
                    try:
                        result.append((
                            reference_type,
                            model,
                            simulation,
                            masking,
                            variable,
                            data[model][reference_type][simulation][masking]
                            ))
                    except KeyError:
                        pass

    return result


def decode(fpath, data):
    """Decodes set of metrics files.

    :param str fpath: Path to file from which metrics data was loaded.
    :param list data: Raw metrics data in pcmdi format.

    :returns: Input data to be transformed.
    :rtype: list

    """
    return (data, _get_groups(data, _get_variable(fpath)))
