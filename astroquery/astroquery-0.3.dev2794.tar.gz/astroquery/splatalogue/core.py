# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Module to search Splatalogue.net via splat, modeled loosely on
ftp://ftp.cv.nrao.edu/NRAO-staff/bkent/slap/idl/

:author: Adam Ginsburg <adam.g.ginsburg@gmail.com>
"""
import warnings
from astropy.io import ascii
from astropy import units as u
from ..query import BaseQuery
from ..utils import commons, async_to_sync
from ..utils.docstr_chompers import prepend_docstr_noreturns
from . import conf
from . import load_species_table

__all__ = ['Splatalogue', 'SplatalogueClass']

# example query of SPLATALOGUE directly:
# http://www.cv.nrao.edu/php/splat/c.php?sid%5B%5D=64&sid%5B%5D=108&calcIn=&data_version=v2.0&from=&to=&frequency_units=MHz&energy_range_from=&energy_range_to=&lill=on&tran=&submit=Search&no_atmospheric=no_atmospheric&no_potential=no_potential&no_probable=no_probable&include_only_nrao=include_only_nrao&displayLovas=displayLovas&displaySLAIM=displaySLAIM&displayJPL=displayJPL&displayCDMS=displayCDMS&displayToyaMA=displayToyaMA&displayOSU=displayOSU&displayRecomb=displayRecomb&displayLisa=displayLisa&displayRFI=displayRFI&ls1=ls1&ls5=ls5&el1=el1


@async_to_sync
class SplatalogueClass(BaseQuery):

    SLAP_URL = conf.slap_url
    QUERY_URL = conf.query_url
    TIMEOUT = conf.timeout
    LINES_LIMIT = conf.lines_limit
    versions = ('v1.0', 'v2.0')
    # global constant, not user-configurable
    ALL_LINE_LISTS = ('Lovas', 'SLAIM', 'JPL', 'CDMS', 'ToyoMA', 'OSU',
                      'Recomb', 'Lisa', 'RFI')
    TOP20_LIST = ('comet', 'planet', 'top20', 'ism_hotcore', 'ism_darkcloud',
                  'ism_diffusecloud')
    FREQUENCY_BANDS = {"any":"Any",
                       "alma3":"ALMA Band 3 (84-116 GHz)",
                       "alma4":" ALMA Band 4 (125-163 GHz)",
                       "alma5":" ALMA Band 5 (163-211 GHz)",
                       "alma6":"ALMA Band 6 (211-275 GHz)",
                       "alma7":"ALMA Band 7 (275-373 GHz)",
                       "alma8":"ALMA Band 8 (385-500 GHz)",
                       "alma9":"ALMA Band 9 (602-720 GHz)",
                       "alma10":"ALMA Band 10 (787-950 GHz)",
                       "pf1":"GBT PF1 (0.29-0.92 GHz)",
                       "pf2":"GBT PF2 (0.91-1.23 GHz)",
                       "l":"GBT/VLA L (1-2 GHz)",
                       "s":"GBT/VLA S (1.7-4 GHz)",
                       "c":"GBT/VLA C (3.9-8 GHz)",
                       "x":"GBT/VLA X (8-12 GHz)",
                       "ku":" GBT/VLA Ku (12-18 GHz)",
                       "kfpa":"GBT KFPA (18-27.5 GHz)",
                       "k":"VLA K (18-26.5 GHz)",
                       "ka":" GBT/VLA Ka (26-40 GHz)",
                       "q":"GBT/VLA Q (38-50 GHz)",
                       "w":"GBT W (67-93.3 GHz)",
                       "mustang":"GBT Mustang (80-100 GHz)", }

    def __init__(self, **kwargs):
        """
        Initialize a Splatalogue query class with default arguments set.
        Frequency specification is required for *every* query, but any
        default keyword arguments (see `query_lines`) can be overridden
        here.
        """
        self.data = self._default_kwargs()
        self.set_default_options(**kwargs)

    def set_default_options(self, **kwargs):
        """
        Modify the default options.
        See `query_lines`
        """
        self.data.update(self._parse_kwargs(**kwargs))

    def get_species_ids(self, restr=None, reflags=0):
        """
        Get a dictionary of "species" IDs, where species refers to the molecule
        name, mass, and chemical composition.

        Parameters
        ----------
        restr : str
            String to compile into an re, if specified.   Searches table for
            species whose names match
        reflags : int
            Flags to pass to `re`.
        """
        # loading can be an expensive operation and should not change at runtime:
        # do it lazily
        if not hasattr(self, '_species_ids'):
            self._species_ids = load_species_table.species_lookuptable()

        if restr is not None:
            return self._species_ids.find(restr, reflags)
        else:
            return self._species_ids

    def _default_kwargs(self):
        kwargs = dict(min_frequency=0 * u.GHz,
                      max_frequency=100 * u.THz,
                      chemical_name='',
                      line_lists=self.ALL_LINE_LISTS,
                      line_strengths=('ls1', 'ls3', 'ls4', 'ls5'),
                      energy_levels=('el1', 'el2', 'el3', 'el4'),
                      exclude=('potential', 'atmospheric', 'probable'),
                      version='v2.0',
                      only_NRAO_recommended=None,
                      export=True,
                      export_limit=self.LINES_LIMIT,
                      noHFS=False, displayHFS=False, show_unres_qn=False,
                      show_upper_degeneracy=False, show_molecule_tag=False,
                      show_qn_code=False, show_lovas_labref=False,
                      show_lovas_obsref=False, show_orderedfreq_only=False,
                      show_nrao_recommended=False,)
        return self._parse_kwargs(**kwargs)

    def _parse_kwargs(self, min_frequency=None, max_frequency=None,
                      band='any', top20=None, chemical_name=None,
                      chem_re_flags=0, energy_min=None, energy_max=None,
                      energy_type=None, intensity_lower_limit=None,
                      intensity_type=None, transition=None, version=None,
                      exclude=None, only_NRAO_recommended=None,
                      line_lists=None, line_strengths=None, energy_levels=None,
                      export=None, export_limit=None, noHFS=None,
                      displayHFS=None, show_unres_qn=None,
                      show_upper_degeneracy=None, show_molecule_tag=None,
                      show_qn_code=None, show_lovas_labref=None,
                      show_lovas_obsref=None, show_orderedfreq_only=None,
                      show_nrao_recommended=None):
        """
        The Splatalogue service returns lines with rest frequencies in the
        range [min_frequency, max_frequency]

        Parameters
        ----------
        min_frequency : `astropy.units`
        max_frequency : `astropy.units`
            Minimum and maximum frequency (or any spectral() equivalent)
        band : str
            The observing band.  If it is not 'any', it overrides
            minfreq/maxfreq.

        Other Parameters
        ----------------
        top20: str
            One of ``'comet'``, ``'planet'``, ``'top20'``, ``'ism_hotcore'``,
            ``'ism_darkcloud'``, ``'ism_diffusecloud'``.
            Overrides chemical_name
        chemical_name : str
            Name of the chemical to search for. Treated as a regular expression.
            An empty set ('', (), [], {}) will match *any* species.
            Example:
            ``'H2CO'`` - 13 species have H2CO somewhere in their formula.
            ``'Formaldehyde'`` - There are 8 isotopologues of Formaldehyde (e.g., H213CO).
            ``'formaldehyde'`` - Thioformaldehyde,Cyanoformaldehyde.
            ``'formaldehyde',flags=re.I`` - Formaldehyde,thioformaldehyde, and Cyanoformaldehyde.
            ``' H2CO '`` - Just 1 species, H2CO.  The spaces prevent including others.
        chem_re_flags : int
            See the `re` module
        energy_min : `None` or float
        energy_max : `None` or float
            Energy range to include.  See energy_type
        energy_type : ``'el_cm1'``, ``'eu_cm1'``, ``'eu_k'``, ``'el_k'``
            Type of energy to restrict.  L/U for lower/upper state energy,
            cm/K for *inverse* cm, i.e. wavenumber, or K for Kelvin
        intensity_lower_limit : `None` or float
            Lower limit on the intensity.  See intensity_type
        intensity_type : `None` or ``'sij'``, ``'cdms_jpl'``, ``'aij'``
            The type of intensity on which to place a lower limit
        transition : str
            e.g. 1-0
        version : ``'v1.0'`` or ``'v2.0'``
            Data version
        exclude : list
            Types of lines to exclude.  Default is:
            (``'potential'``, ``'atmospheric'``, ``'probable'``)
            Can also exclude ``'known'``
        only_NRAO_recommended : bool
            Show only NRAO recommended species?
        line_lists : list
            Options:
            Lovas, SLAIM, JPL, CDMS, ToyoMA, OSU, Recomb, Lisa, RFI
        line_strengths : list
            CDMS/JPL Intensity : ls1
            Sij : ls3
            Aij : ls4
            Lovas/AST : ls5
        energy_levels : list
            E_lower (cm^-1) : el1
            E_lower (K) : el2
            E_upper (cm^-1) : el3
            E_upper (K) : el4
        export : bool
            Set up arguments for the export server (as opposed to the HTML
            server)?
        export_limit : int
            Maximum number of lines in output file
        noHFS : bool
            No HFS Display
        displayHFS : bool
            Display HFS Intensity
        show_unres_qn : bool
            Display Unresolved Quantum Numbers
        show_upper_degeneracy : bool
            Display Upper State Degeneracy
        show_molecule_tag : bool
            Display Molecule Tag
        show_qn_code : bool
            Display Quantum Number Code
        show_lovas_labref : bool
            Display Lab Ref
        show_lovas_obsref : bool
            Display Obs Ref
        show_orderedfreq_only : bool
            Display Ordered Frequency ONLY
        show_nrao_recommended : bool
            Display NRAO Recommended Frequencies

        Returns
        -------
        Dictionary of the parameters to send to the SPLAT page
        payload : dict
            A dictionary of keywords
        """

        payload = {'submit': 'Search',
                   'frequency_units': 'GHz',
                   }

        if band != 'any':
            if band not in self.FREQUENCY_BANDS:
                raise ValueError("Invalid frequency band.")
            if min_frequency is not None or max_frequency is not None:
                warnings.warn("Band was specified, so the frequency specification is overridden")
            payload['band'] = band
        elif min_frequency is not None and max_frequency is not None:
            # allow setting payload without having *ANY* valid frequencies set
            min_frequency = min_frequency.to(u.GHz, u.spectral())
            max_frequency = max_frequency.to(u.GHz, u.spectral())
            if min_frequency > max_frequency:
                min_frequency, max_frequency = max_frequency, min_frequency

            payload['from'] = min_frequency.value
            payload['to'] = max_frequency.value

        if top20 is not None:
            if top20 in self.TOP20_LIST:
                payload['top20'] = top20
            else:
                raise ValueError("Top20 is not one of the allowed values")
        elif chemical_name in ('', {}, (), [], set()):
            # include all
            payload['sid[]'] = []
        elif chemical_name is not None:
            species_ids = self.get_species_ids(chemical_name, chem_re_flags)
            if len(species_ids) == 0:
                raise ValueError("No matching chemical species found.")
            payload['sid[]'] = list(species_ids.values())

        if energy_min is not None:
            payload['energy_range_from'] = float(energy_min)
        if energy_max is not None:
            payload['energy_range_to'] = float(energy_max)
        if energy_type is not None:
            payload['energy_range_type'] = energy_type

        if intensity_type is not None:
            payload['lill'] = 'lill_' + intensity_type
            if intensity_lower_limit is not None:
                payload[payload['lill']] = intensity_lower_limit

        if transition is not None:
            payload['tran'] = transition

        if version in self.versions:
            payload['version'] = version
        elif version is not None:
            raise ValueError("Invalid version specified.  Allowed versions are {vers}".format(vers=str(self.versions)))

        if exclude is not None:
            for e in exclude:
                payload['no_' + e] = 'no_' + e

        if only_NRAO_recommended:
            payload['include_only_nrao'] = 'include_only_nrao'

        if line_lists is not None:
            if type(line_lists) not in (tuple, list):
                raise TypeError("Line lists should be a list of linelist names.  See Splatalogue.ALL_LINE_LISTS")
            for L in self.ALL_LINE_LISTS:
                kwd = 'display' + L
                if L in line_lists:
                    payload[kwd] = kwd
                else:
                    payload[kwd] = ''

        if line_strengths is not None:
            for LS in line_strengths:
                payload[LS] = LS

        if energy_levels is not None:
            for EL in energy_levels:
                payload[EL] = EL

        for b in "noHFS,displayHFS,show_unres_qn,show_upper_degeneracy,show_molecule_tag,show_qn_code,show_lovas_labref,show_orderedfreq_only,show_lovas_obsref,show_nrao_recommended".split(","):
            if locals()[b]:
                payload[b] = b

        # default arg, unmodifiable...
        payload['jsMath'] = 'font:symbol,warn:0'
        payload['__utma'] = ''
        payload['__utmc'] = ''

        if export:
            payload['submit'] = 'Export'
            payload['export_delimiter'] = 'colon'  # or tab or comma
            payload['export_type'] = 'current'
            payload['offset'] = 0
            payload['range'] = 'on'
            if export_limit is not None:
                payload['limit'] = export_limit
            else:
                payload['limit'] = self.LINES_LIMIT

        return payload

    def _validate_kwargs(self, min_frequency=None, max_frequency=None,
                         band='any', **kwargs):
        """
        Check that either min_frequency + max_frequency or band are specified
        """
        if band == 'any':
            if min_frequency is None or max_frequency is None:
                raise ValueError("Must specify either min/max frequency or a valid Band.")

    @prepend_docstr_noreturns("\n" + _parse_kwargs.__doc__)
    def query_lines_async(self, min_frequency=None, max_frequency=None, **kwargs):
        """
        Returns
        -------
        response : `requests.Response`
            The response of the HTTP request.
        """
        # have to chomp this kwd here...
        get_query_payload = (kwargs.pop('get_query_payload')
                             if 'get_query_payload' in kwargs
                             else False)
        self._validate_kwargs(min_frequency=min_frequency,
                              max_frequency=max_frequency, **kwargs)

        if hasattr(self, 'data'):
            data_payload = self.data.copy()
            data_payload.update(self._parse_kwargs(min_frequency=min_frequency,
                                                   max_frequency=max_frequency,
                                                   **kwargs))
        else:
            data_payload = self._default_kwargs()
            data_payload.update(self._parse_kwargs(min_frequency=min_frequency,
                                                   max_frequency=max_frequency,
                                                   **kwargs))

        if get_query_payload:
            return data_payload

        response = commons.send_request(
            self.QUERY_URL,
            data_payload,
            self.TIMEOUT)

        self.response = response

        return response

    def _parse_result(self, response, verbose=False):
        """
        Parse a response into an `~astropy.table.Table`
        """

        try:
            result = ascii.read(response.text.split('\n'),
                                delimiter=':',
                                format='basic')
        except TypeError:
            # deprecated
            result = ascii.read(response.text.split('\n'),
                                delimiter=':',
                                Reader=ascii.Basic)

        return result

    def get_fixed_table(self, columns=None):
        """
        Convenience function to get the table with html column names made human
        readable.  It returns only the columns identified with the ``columns``
        keyword.  See the source for the defaults.
        """
        if columns is None:
            columns = ('Species', 'Chemical Name', 'Resolved QNs', 'Freq-GHz',
                       'Meas Freq-GHz', 'Log<sub>10</sub> (A<sub>ij</sub>)',
                       'E_U (K)')
        table = self.table[columns]
        long_to_short = {'Log<sub>10</sub> (A<sub>ij</sub>)':'log10(Aij)',
                         'E_U (K)':'EU_K',
                         'E_U (cm^-1)':'EU_cm',
                         'E_L (K)':'EL_K',
                         'E_L (cm^-1)':'EL_cm',
                         'Chemical Name':'Name',
                         'Lovas/AST Intensity':'Intensity',
                         'Freq-GHz':'Freq',
                         'Freq Err':'eFreq',
                         'Meas Freq-GHz':'MeasFreq',
                         'Meas Freq Err':'eMeasFreq',
                         'Resolved QNs':'QNs'}
        for cn in long_to_short:
            if cn in table.colnames:
                table.rename_column(cn, long_to_short[cn])
        return table


Splatalogue = SplatalogueClass()
