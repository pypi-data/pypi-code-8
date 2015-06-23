import re
from netCDF4  import Dataset as netCDF4_Dataset
from operator import mul
from json     import loads as json_loads
from ast      import literal_eval as ast_literal_eval
from struct   import unpack as struct_unpack
from struct   import error  as struct_error


from numpy import dtype       as numpy_dtype
from numpy import result_type as numpy_result_type

from ..ancillaryvariables  import AncillaryVariables
from ..coordinate          import DimensionCoordinate, AuxiliaryCoordinate
from ..coordinatebounds    import CoordinateBounds
from ..cellmeasure         import CellMeasure
from ..coordinatereference import CoordinateReference
from ..field               import Field
from ..cellmethods         import CellMethods
from ..fieldlist           import FieldList
from ..units               import Units
from ..functions           import abspath, dirname, pathjoin

from ..data.data import Data

from .functions import _open_netcdf_file
from .filearray import NetCDFFileArray

def read(filename, fmt=None, verbose=False):
    ''' 

Read fields from an input netCDF file on disk or from an OPeNDAP
server location.

The file may be big or little endian.

NetCDF dimension names are stored in the `nc_dimensions` attribute of
a field's domain and netCDF variable names are stored in the `ncvar`
attributes of the field and its domain components (coordinates,
coordinate bounds, cell measures and coordinate referencess).

:Parameters:

    filename : str or file
        A string giving the file name or OPenDAP URL, or an open file
        object, from which to read fields. Note that if a file object
        is given it will be closed and reopened.

    fmt : str, optional
        Only read the file if it is the given format. Valid formats
        are ``'NETCDF'`` for a CF-netCDF file and ``'CFA'`` for
        CFA-netCDF file. By default a file of any of these formats is
        read.

:Returns:

    out : FieldList
        The fields in the file.

:Examples:

>>> f = cf.netcdf.read('file.nc')
>>> type(f)
<class 'cf.field.FieldList'>
>>> f
[<CF Field: pmsl(30, 24)>,
 <CF Field: z-squared(17, 30, 24)>,
 <CF Field: temperature(17, 30, 24)>,
 <CF Field: temperature_wind(17, 29, 24)>]

>>> cf.netcdf.read('file.nc')[0:2]
[<CF Field: pmsl(30, 24)>,
 <CF Field: z-squared(17, 30, 24)>]

>>> cf.netcdf.read('file.nc', units='K')
[<CF Field: temperature(17, 30, 24)>,
 <CF Field: temperature_wind(17, 29, 24)>]

>>> cf.netcdf.read('file.nc')[0]
<CF Field: pmsl(30, 24)>

'''
    if isinstance(filename, file):
        name = filename.name
        filename.close()
        filename = name
    #--- End: if
    
    filename = abspath(filename)

    # Read the netCDF file 
    nc = _open_netcdf_file(filename, 'r') 

    # Set of all of the netCDF variable names in the file.
    #
    # For example:
    # >>> variables
    # set(['lon','lat','tas'])
    variables = set(map(str, nc.variables))

    # ----------------------------------------------------------------
    # Put the file's global attributes into the global
    # 'global_attributes' dictionary
    # ----------------------------------------------------------------
    global_attributes = {}
    for attr in map(str, nc.ncattrs()):
        try:
            value = nc.getncattr(attr)
            if isinstance(value, basestring):
                try:
                    global_attributes[attr] = str(value)
                except UnicodeEncodeError:
                    global_attributes[attr] = value.encode(errors='ignore')          
            else:
                global_attributes[attr] = value     
        except UnicodeDecodeError:
            pass
    #--- End: for
        
    # Find out if this is a CFA file
    cfa = 'CFA' in global_attributes.get('Conventions', [])

    if (fmt and 
        (not cfa and fmt == 'CFA') or (cfa and fmt == 'NETCDF')):
        # Return an empty field list
        return FieldList()

    # ----------------------------------------------------------------
    # Create a dictionary keyed by nc variable names where each key's
    # value is a dictionary of that variable's nc
    # attributes. E.g. attributes['tas']['units']='K'
    # ----------------------------------------------------------------
    attributes = {}
    for ncvar in variables:
        attributes[ncvar] = {}
        for attr in map(str, nc.variables[ncvar].ncattrs()):
            try:
                attributes[ncvar][attr] = nc.variables[ncvar].getncattr(attr)
                if isinstance(attributes[ncvar][attr], basestring):
                    try:
                        attributes[ncvar][attr] = str(attributes[ncvar][attr])
                    except UnicodeEncodeError:
                        attributes[ncvar][attr] = attributes[ncvar][attr].encode(errors='ignore')
            except UnicodeDecodeError:
                pass
        #--- End: for  

        # Check for bad units
        try:
            Units(attributes[ncvar].get('units', None), 
                  attributes[ncvar].get('calendar', None))
        except (ValueError, TypeError):
            # Units in file have been set to unknown units so 1) give
            # a warning, 2) set the 'nonCF_units' property to the bad
            # units and 3) remove the offending units.
            attributes[ncvar]['nonCF_Units'] = \
                attributes[ncvar].pop('units', '')
            attributes[ncvar]['nonCF_Units'] += \
                ' '+attributes[ncvar].pop('calendar', '')
            if verbose:
                print(
"WARNING: Moving unsupported units to 'nonCF_Units': %s" % attributes[ncvar]['nonCF_Units'])
    #--- End: for

    # ----------------------------------------------------------------
    # Remove everything bar data variables from the list of
    # variables. I.e. remove dimension and auxiliary coordinates,
    # their bounds and grid_mapping variables
    # ----------------------------------------------------------------
    for ncvar in variables.copy():

        # Remove dimension coordinates and their bounds
        if ncvar in map(str, nc.dimensions):

            if ncvar in variables:
                variables.discard(ncvar)
                for attr in ('bounds', 'climatology'):
                    if attr not in attributes[ncvar]:
                        continue
                
                    # Check the dimensionality of the coordinate's
                    # bounds. If it is not right, then it can't be a
                    # bounds variable and so promote to an independent
                    # data variable
                    bounds = attributes[ncvar][attr]
                    if bounds in nc.variables:
                        if nc.variables[bounds].ndim == nc.variables[ncvar].ndim+1:
                            variables.discard(bounds)
                        else:
                            del attributes[ncvar][attr]

                        break
                    else:
                        del attributes[ncvar][attr]
                        if verbose:
                            print(
"WARNING: Missing bounds variable '%(bounds)s' in %(filename)s" %
locals())
                #--- End: for
            #--- End: if

            continue
        #--- End: if

        # Still here? Then remove auxiliary coordinates and their
        # bounds
        if 'coordinates' in attributes[ncvar]:
            # Allow for (incorrect) comma separated lists
            for aux in re.split('\s+|\s*,\s*', attributes[ncvar]['coordinates']):
                if aux in variables:
                    variables.discard(aux)
                    for attr in ('bounds', 'climatology'):
                        if attr not in attributes[aux]:
                            continue

                        # Check the dimensionality of the coordinate's
                        # bounds. If it is not right, then it can't be
                        # a bounds variable and so promote to an
                        # independent data variable.
                        bounds = attributes[aux][attr]
                        if bounds in nc.variables:
                            if nc.variables[bounds].ndim == nc.variables[aux].ndim+1:
                                variables.discard(bounds)
                            else:
                                del attributes[aux][attr]

                            break
                        else:
                            del attributes[aux][attr]
                            if verbose:
                                print(
"WARNING: Missing bounds variable '%(bounds)s' in %(filename)s" %
locals())
                    #--- End: for
                #--- End: if
            #--- End: for
        #--- End: if
    
        # Remove grid mapping variables
        if 'grid_mapping' in attributes[ncvar]:
            variables.discard(attributes[ncvar]['grid_mapping'])

        # Remove cell measure variables
        if 'cell_measures' in attributes[ncvar]:
            cell_measures = re.split('\s*(\w+):\s*',
                                     attributes[ncvar]['cell_measures'])
            for ncvar in cell_measures[2::2]:
                variables.discard(ncvar)
        #--- End: if

    #--- End: for

    # ----------------------------------------------------------------
    # Everything left in the variables set is now a proper data
    # variable, so make a list of fields, each of which contains one
    # data variable and the relevant shared metadata.
    # ----------------------------------------------------------------

    # Dictionary mapping netCDF variable names of domain components to
    # their cf Variables.
    #
    # For example:
    # >>> seen_in_file
    # {'lat': <CF Coordinate: (73)>}
    seen_in_file = {}

#    # Dictionary of ?
#    #
#    # For example:
#    # >>> formula_terms
#    #
#    formula_terms = {}

    # Set
    #
    # For example:
    # >>> 
    #
    coordref_field_pointers = set()

    ancillary_variables = set()
    fields_in_file      = FieldList()

    for data_var in variables:
        # Don't turn private CFA variables into fields
        if _is_cfa_private_variable(nc.variables[data_var], cfa):
            continue

        f = _create_Field(filename,
                          nc,
                          data_var,
                          attributes,
                          seen_in_file,
                          ancillary_variables, 
                          coordref_field_pointers,
                          global_attributes,
                          cfa=cfa,
                          verbose=verbose)
        
        fields_in_file.append(f)
    #--- End: for

    # ----------------------------------------------------------------
    # Find which fields are being pointed to from coordinate
    # references
    # ----------------------------------------------------------------
    ncvar_to_field = {}
    if coordref_field_pointers:
        i = 0        
        while i < len(fields_in_file):
            f = fields_in_file[i]
            ncvar = f.ncvar            
            if ncvar in coordref_field_pointers:
                # Remove coordinate references from a field which is
                # pointed to from a coordinate reference and also
                # remove the field from the list of output fields
                for key, coordref in f.refs().iteritems():
                    for term in set(coordref).difference(coordref.coord_terms):
                        if isinstance(coordref[term], dict):
                            f.remove_item(key)

                fields_in_file.pop(i)
                # Map the pointer to the field so that we'll later be
                # able to replace the pointer with the field
                ncvar_to_field[ncvar] = f
            else:
                i += 1
    #--- End: if

    # ----------------------------------------------------------------
    # Inside coordinate references, replace pointers to fields with
    # the actual fields themselves.
    # ----------------------------------------------------------------
    if ncvar_to_field:
        for f in fields_in_file:
            for coordref in f.refs().values():
                for term, value in coordref.iteritems():
                    if isinstance(value, dict):
                        coordref[term] = ncvar_to_field[value['ncvar']].copy()
    #--- End: if
        
    # ----------------------------------------------------------------
    # For each field that has ancillary variables, replace its
    # built-in list of netCDF variable names with an
    # AncillaryVariables object.
    # ----------------------------------------------------------------
    if ancillary_variables:
        ncvar_to_field = {}
        index = 0
        while ancillary_variables:
            try:
                f = fields_in_file[index]
            except IndexError:
                # No more fields
                break
            
            # Still here?
            ncvar = f.ncvar            
            if ncvar in ancillary_variables:
                # ----------------------------------------------------
                # This field is being used as an ancillary variable in
                # another field
                # ----------------------------------------------------
                ancillary_variables.discard(ncvar)
                ncvar_to_field[ncvar] = f
                fields_in_file.pop(index)
            else:
                index += 1
        #--- End: while
        
        for f in fields_in_file:
            if not hasattr(f, 'ancillary_variables'):
                continue

            av = AncillaryVariables()
            for ncvar in f.ancillary_variables:
                av.append(ncvar_to_field[ncvar].copy())

            f.ancillary_variables = av
        #--- End: for
    #--- End: if

    return fields_in_file
#--- End: def

def _create_Field(filename,
                  nc,
                  data_var,
                  attributes,
                  seen_in_file,
                  ancillary_variables, 
                  coordref_field_pointers,
                  global_attributes,
                  cfa=False,
                  verbose=False):
    '''

Create a field for a given netCDF variable.

:Parameters:

    filename : str
        The name of the netCDF file.

    nc : netCDF4.Dataset
        The entire netCDF file in a `netCDF4.Dataset` instance.

    data_var : str
        The netCDF name of the variable to be turned into a field.

    attributes : dict
        Dictionary of the data variable's netCDF attributes.

    seen_in_file : dict

#    formula_terms : dict

    ancillary_variables : set

    global_attributes : dict

    cfa : bool
        If True then netCDF file is a CFA file. By default it is
        assumed that the file is not a CFA file.

:Returns:

    out : Field
        The new field.

'''
    properties = attributes[data_var]

    # Add global attributes to the data variable's properties, unless
    # the data variables already has a property with the same name.
    for attr, value in global_attributes.iteritems():
#        if attr not in attributes[data_var]:
        if attr not in properties:
#            attributes[data_var][attr] = value
            properties[attr] = value

    # Take cell_methods out of the data variable's properties since it
    # will need special processing once the domain has been defined
    if 'cell_methods' in properties:
        cell_methods = properties.pop('cell_methods')
        try:
            cell_methods = CellMethods(cell_methods)
        except:
            # Something went wrong whilst trying to parse the cell
            # methods string
            properties['nonCF_cell_methods'] = cell_methods
            if verbose:
                print(
"WARNING: Moving unsupported cell methods to 'nonCF_cell_methods': %r" %
cell_methods)
            cell_methods = None
    else:
        cell_methods = None

    # Take add_offset and scale_factor out of the data variable's
    # properties since they will be dealt with by the variable's Data
    # object. Makes sure we note that they were there so we can adjust
    # the field's dtype accordingly
    values = [properties.pop(k, None) for k in ('add_offset', 'scale_factor')]
    unpacked_dtype = values != [None, None]
    if unpacked_dtype:
        try:
            values.remove(None)
        except ValueError:
            pass

        unpacked_dtype = numpy_result_type(*values)
    #--- End: if    

    # Change numpy arrays to tuples for selected attributes
    for attr in ('valid_range',):
#        if attr in attributes[data_var]:
#            attributes[data_var][attr] = tuple(attributes[data_var][attr])
        if attr in properties:
            properties[attr] = tuple(properties[attr])

    # ----------------------------------------------------------------
    # Initialize the field with the data variable and its attributes
    # ----------------------------------------------------------------
    f_Units = Units(properties.pop('units', None),
                    properties.pop('calendar', None))

    f = Field(properties=properties, copy=False)

    f.ncvar = data_var
    f.file  = filename
    f.Units = f_Units

    # Map netCDF dimension dimension names to domain dimension names.
    # 
    # For example:
    # >>> ncdim_to_dim
    # {'lat': 'dim0', 'time': 'dim1'}
    ncdim_to_dim = {}

    ncvar_to_key = {}
        
    f.domain._axes['data'] = []
    f.domain.nc_dimensions = {}

    # ----------------------------------------------------------------
    # Add axes and non-scalar dimension coordinates to the field
    # ----------------------------------------------------------------
    field_ncdimensions = _ncdimensions(nc.variables[data_var], cfa)

    for ncdim in field_ncdimensions:
        if ncdim in nc.variables:
            # There is a dimension coordinate for this dimension, so
            # create the coordinate and the dimension.
            if ncdim in seen_in_file:
                coord = seen_in_file[ncdim].copy()
            else:
                coord = _create_Coordinate(nc, ncdim, attributes, f, cfa=cfa,
                                           dimension=True)
                seen_in_file[ncdim] = coord                
            #--- End: if

            dim = f.domain.insert_dim(coord, copy=False)

            ncvar_to_key[ncdim] = dim
        else:
            # There is no dimension coordinate for this dimension, so
            # just create a dimension with the correct size.
            dim = f.domain.insert_axis(size=len(nc.dimensions[ncdim]))
        #--- End: if

        # Update data dimension name and set dimension size
        f.domain.nc_dimensions[dim] = ncdim
        f.domain._axes['data'].append(dim)
        
        ncdim_to_dim[ncdim] = dim
    #--- End: for
    
    f.Data = _set_Data(nc, nc.variables[data_var], f, f,
                       unpacked_dtype=unpacked_dtype, cfa=cfa)

    # ----------------------------------------------------------------
    # Add scalar dimension coordinates and auxiliary coordinates to
    # the field
    # ----------------------------------------------------------------
    coordinates = f.getprop('coordinates', None)
    if coordinates is not None:
        
        # Split the list (allowing for incorrect comma separated
        # lists).
        for ncvar in re.split('\s+|\s*,\s*', coordinates):
            # Skip dimension coordinates which are in the list
            if ncvar in field_ncdimensions:
                continue

            # Skip auxiliary coordinates which are in the list but not
            # in the file
            if ncvar not in nc.variables:
                continue

            # Set dimensions 
            aux_ncdimensions = _ncdimensions(nc.variables[ncvar], cfa)
            dimensions = [ncdim_to_dim[ncdim] for ncdim in aux_ncdimensions
                          if ncdim in ncdim_to_dim]    

            if ncvar in seen_in_file:
                coord = seen_in_file[ncvar].copy()
            else:
                coord = _create_Coordinate(nc, ncvar, attributes, f, cfa=cfa,
                                           dimension=False)
                seen_in_file[ncvar] = coord
            #--- End: if

            # --------------------------------------------------------
            # Turn a ..
            # --------------------------------------------------------
            is_dimension_coordinate = False
            if not dimensions:
                if nc.variables[ncvar].dtype.kind is 'S':
                    # String valued scalar coordinate. Is this CF
                    # complaint? Don't worry about it - it'll get
                    # turned into a 1-d, size 1 auxiliary coordinate
                    # construct, anyway
                    dim = f.domain.new_axis_identifier()
                    dimensions = [dim]
                else:  
                    # Numeric valued scalar coordinate
                    is_dimension_coordinate = True
            #--- End: if

            if is_dimension_coordinate:
                # Insert dimension coordinate
                coord = coord.asdimension(copy=False)
                dim = f.domain.insert_dim(coord, copy=False)
                f.domain.nc_dimensions[dim]= ncvar
                ncvar_to_key[ncvar] = dim
                seen_in_file[ncvar] = coord
            else:
                # Insert auxiliary coordinate
                aux = f.domain.insert_aux(coord, axes=dimensions,
                                          copy=False)
                ncvar_to_key[ncvar] = aux
        #--- End: for

        f.delprop('coordinates')
    #--- End: if

    # ----------------------------------------------------------------
    # Add formula_terms coordinate references
    # ----------------------------------------------------------------
    for key, coord in f.coords().iteritems():
        formula_terms = attributes[coord.ncvar].get('formula_terms', None)
        if formula_terms is None:
            # This coordinate doesn't have a formula_terms attribute
            continue

        _create_formula_terms_ref(f, key, coord, formula_terms,
                                  attributes, ncvar_to_key,
                                  coordref_field_pointers)
    #--- End: for

#        # Add the equation terms and references to their values to to
#        # new auxiliary coordinate's coordinate reference.
#        kwargs = {}
#        ft = re.split('\s+|\s*:\s+', form_terms)
#        for term, ncvar in zip(ft[0::2], ft[1::2]):
#            if ncvar in ncvar_to_key:
#                # CASE 1: This variable is a coordinate of the field,
#                #         so we point to it from the coordinate reference.
#                value = ncvar_to_key[ncvar]
#
#            elif ncvar not in attributes:
#                # CASE 2: The value does not exist as a netCDF
#                #         variable in this file
#                value = None
#
#            else:
#                # CASE 3: This variable is not a coordinate of the
#                #         field so it goes in to the coordinate reference as an
#                #         independent field
#
##            elif 'bounds' not in attributes[ncvar]:
##                # CASE 3: This variable is not a coordinate of the
##                #         field and it has no bounds, so it goes in to
##                #         the coordinate reference as an independent field.
#                value = {'ncvar': ncvar}
#                coordref_field_pointers.add(ncvar)
#                
##            else:
##                # CASE 4: This variable is not a coordinate of the
##                #         field and yet it has bounds
##                aux_dims = []
##                var_ncdimensions = _ncdimensions(nc.variables[ncvar], cfa)
##                for ncdim in var_ncdimensions:
##                    if ncdim not in ncdim_to_dim:
##                        aux_dims = None
##                        break
##
##                    aux_dims.append(ncdim_to_dim[ncdim])
##                #--- End: for
##
##                if aux_dims is None:
##                    # CASE 4a: This variable's dimensions are not a
##                    #          subset of the field's dimensions, so it
##                    #          can't be a coordinate. Therefore it
##                    #          goes into the coordinate reference as an
##                    #          independent field with the bounds
##                    #          deleted.
##                    value = {'ncvar': ncvar}
##
##                else:
##                    # CASE 4b: This variable's dimensions are a subset
##                    #          of the field's dimensions, so we may
##                    #          allow it to be a coordinate. Therefore
##                    #          add it to the field as an auxiliary
##                    #          coordinate and point to it from the
##                    #          coordinate reference.
##                    coord = _create_Coordinate(nc, ncvar, attributes, f, cfa=cfa,
##                                               dimension=False)
##                    if coord.hasprop('formula_terms'):
##                        coord.delprop('formula_terms')
##
##                    aux = f.domain.insert_aux(coord, axes=aux_dims, key=aux, 
##                                              copy=False)
##
##                    ncvar_to_key[ncvar] = aux
##
##                    # Add this variable name and its bounds name to
##                    # the set of variables which are not fields. Note
##                    # that if it turns out that this variable is also
##                    # being used as a field in another coordinate reference then
##                    # its name will be removed from this set.
##                    not_fields.update((ncvar, attributes[ncvar]['bounds']))
##                    
##                    value = aux
#            #--- End: if
#                    
#            kwargs[term] = value
#        #--- End: for 
#
#        name = coord.getprop('standard_name', None)
#        coordref = CoordinateReference(name=name, coords=(key,), crtype='formula_terms',
#                                        **kwargs)
#
#        f.domain.insert_coordref(coordref, copy=False)
#
#        formula_terms[coord_ncvar] = coordref
#
##        coord.delprop('formula_terms')
#    #--- End: for

    # ----------------------------------------------------------------
    # Add grid mapping coordinate references
    # ----------------------------------------------------------------
    grid_mapping = f.getprop('grid_mapping', None)
    if grid_mapping is not None:
        _create_grid_mapping_ref(f, grid_mapping, attributes, ncvar_to_key)

#        for ncvar in grid_mapping.split():
#            if ncvar not in attributes:
#                continue

#            name = attributes[ncvar].pop('grid_mapping_name', None)
#
#            coordref = CoordinateReference(name, crtype='grid_mapping',
#                                            **attributes[ncvar])
#            coordref.ncvar = ncvar
#
#            coordref_id = f.domain.insert_coordref(coordref, copy=False)
#        #--- End: for
#
#        f.delprop('grid_mapping')

    # ----------------------------------------------------------------
    # Add cell measures to the field
    # ----------------------------------------------------------------
    cell_measures = f.getprop('cell_measures', None)

    if cell_measures is not None:

        # Parse the cell measures attribute
        cell_measures = re.split('\s*(\w+):\s*', cell_measures)
        
        for measure, ncvar in zip(cell_measures[1::2], 
                                  cell_measures[2::2]):

            if ncvar not in attributes:
                continue

            # Set cell measures' dimensions 
            cm_ncdimensions = _ncdimensions(nc.variables[ncvar], cfa)
            dimensions = [ncdim_to_dim[ncdim] for ncdim in cm_ncdimensions]

            if ncvar in seen_in_file:
                # Copy the cell measure as it already exists
                cell = seen_in_file[ncvar].copy()
            else:
                cell = _create_CellMeasure(nc, ncvar, attributes, f, cfa=cfa)
                cell.measure = measure
                seen_in_file[ncvar] = cell
            #--- End: if

            clm = f.domain.insert_measure(cell, axes=dimensions, copy=False)

            ncvar_to_key[ncvar] = clm
        #--- End: for

        f.delprop('cell_measures')
    #--- End: if

    # -----------------------------
    # Add cell methods to the field
    # -----------------------------
    if cell_methods is not None:
        f.cell_methods = cell_methods.netcdf_translation(f)
 
    # ----------------------------------------------------------------
    # Parse an ancillary_variables string to a list of netCDF variable
    # names, which will get converted to an AncillaryVariables object
    # later. Add these netCDF variable names to the set of all
    # ancillary data variables in the file.
    # ----------------------------------------------------------------
    if hasattr(f, 'ancillary_variables'):  ##dch hasprop?
        f.ancillary_variables = f.ancillary_variables.split()
        ancillary_variables.update(f.ancillary_variables)
    #--- End: if
    
    f.setcyclic()

    # Return the finished field
    return f
#--- End: def

def _create_Coordinate(nc, ncvar, attributes, f, cfa=False,
                       dimension=True):
    '''

Create a coordinate variable, including any bounds.

:Parameters:

    nc : netCDF4.Dataset
        The entire netCDF file in a `netCDF4.Dataset` object.

    ncvar : str
        The netCDF name of the coordinate variable.

    attributes : dict
        Dictionary of the coordinate variable's netCDF attributes.

    f : cf.Field

    cfa : bool, optional
        If True then netCDF file is a CFA file. By default it is
        assumed that the file is not a CFA file.

    dimension : bool, optional
        If True then the a dimension coordinate is created, otherwise
        an auxiliary coordinate is created.

:Returns:

    out : cf.DimensionCoordinate or cf.AuxiliaryCoordinate
        The new coordinate.

'''
    properties = attributes[ncvar].copy()

    c_Units = Units(properties.pop('units', None),
                    properties.pop('calendar', None))

    properties.pop('formula_terms', None)

    ncbounds = properties.pop('bounds', None)
    if ncbounds is None:
        ncbounds = properties.pop('climatology', None)
        climatology = True
    else:
        climatology = False

    if dimension:
        c = DimensionCoordinate(properties=properties, copy=False)
    else:
        c = AuxiliaryCoordinate(properties=properties, copy=False)

    c.ncvar = ncvar
    c.Units = c_Units
    if climatology:
        c.climatology = climatology

    data = _set_Data(nc, nc.variables[ncvar], f, c, cfa=cfa)

    # ------------------------------------------------------------
    # Add any bounds
    # ------------------------------------------------------------
    if ncbounds is None:
        bounds = None
    else:
        properties = attributes[ncbounds].copy()
        properties.pop('formula_terms', None)

        b_Units = Units(properties.pop('units', None),
                        properties.pop('calendar', None))

        bounds = CoordinateBounds(properties=properties, copy=False)

        bounds.ncvar = ncbounds
        bounds.Units = b_Units
    
        bounds.insert_data(
            _set_Data(nc, nc.variables[ncbounds], f, bounds, cfa=cfa),
            copy=False)

        if not b_Units:
            bounds.override_units(c_Units, i=True)
           
        if b_Units and not b_Units.equivalent(c_Units):
            bounds.override_units(c_Units, i=True)
            if verbose:
                print(
"WARNING: Overriding %r of '%s' bounds ('%s') with %r" %
(b_Units, ncvar, ncbounds, c_Units))
 
        # Make sure that the bounds dimensions are in the same order
        # as its parent's dimensions
        c_ncdims = nc.variables[ncvar].dimensions
        b_ncdims = nc.variables[ncbounds].dimensions
        if c_ncdims != b_ncdims[:-1]:
            iaxes = [c_ncdims.index(ncdim) for ncdim in b_ncdims[:-1]]
            iaxes.append(-1)
            bounds.transpose(iaxes, i=True)
        #--- End: if

    #--- End: if

    c.insert_data(data, bounds=bounds, copy=False)

    # ---------------------------------------------------------
    # Return the coordinate
    # ---------------------------------------------------------
    return c
#--- End: def

def _create_CellMeasure(nc, ncvar, attributes, f, cfa=False): #, key=None):
    '''

Create a cell measure variable.

:Parameters:

    nc : netCDF4.Dataset
        The entire netCDF file in a `netCDF4.Dataset` instance.

    ncvar : str
        The netCDF name of the cell measure variable.

    attributes : dict
        Dictionary of the cell measure variable's netCDF attributes.

    f : Field

    cfa : bool, optional
        If True then netCDF file is a CFA file. By default it is
        assumed that the file is not a CFA file.

:Returns:

    out : CellMeasure
        The new cell measure.

'''
    clm       = CellMeasure(properties=attributes[ncvar])
    clm.ncvar = ncvar

    data = _set_Data(nc, nc.variables[ncvar], f, clm, cfa=cfa)

    clm.insert_data(data, copy=False)

    return clm
#--- End: def

def _ncdimensions(ncvariable, cfa=False):
    '''

Return a list of the netCDF dimension names for a netCDF variable.

:Parameters:

    ncvariable : netCDF4.Variable
    
    cfa : bool, optional
        If True then netCDF file is a CFA file. By default it is
        assumed that the file is not a CFA file.

:Returns:

    out : list
        The list of netCDF dimension names.

:Examples: 

>>> ncdims = _ncdimensions(ncvariable)
>>> ncdims = _ncdimensions(ncvariable, cfa=True)

'''
    ncattrs = ncvariable.ncattrs()
    if (cfa and 
        'cf_role' in ncattrs and 
        ncvariable.getncattr('cf_role') == 'cfa_variable'):
        # NetCDF variable is a CFA variable
        if 'cfa_dimensions' in ncattrs:
            ncdimensions = ncvariable.getncattr('cfa_dimensions').split()
        else:
            ncdimensions = []
    else:
        # NetCDF variable is not a CFA variable
        ncdimensions = list(ncvariable.dimensions)
        cfa = False
      
    # Remove a string-length dimension, if there is one. dch alert
    if (not cfa and 
        ncvariable.dtype.kind == 'S' and
        ncvariable.ndim >= 2 and ncvariable.shape[-1] > 1):
        ncdimensions.pop()
     
    return map(str, ncdimensions)
#--- End: def

def _create_grid_mapping_ref(f, grid_mapping, attributes, ncvar_to_key):
    '''

:Parameters:

    f : cf.Field

    grid_mapping : str

    attributes : dict

    ncvar_to_key : dict

:Returns:

    None

'''
    if ':' not in grid_mapping:
        grid_mapping = '%s:' % grid_mapping

    coords = []
    for x in re.sub('\s*:\s*', ': ', grid_mapping).split()[::-1]:
        if not x.endswith(':'):
            try:
                coords.append(ncvar_to_key[x])
            except KeyError:
                continue
        else:
            if not coords:
                coords = None

            grid_mapping = x[:-1]

            if grid_mapping not in attributes:
                coords = []      
                continue
                
            kwargs = attributes[grid_mapping].copy()
            
            name = kwargs.pop('grid_mapping_name', None)                 
  
            coordref = CoordinateReference(name, crtype='grid_mapping',
                                           coords=coords, **kwargs)
            coordref.ncvar = grid_mapping

            f.domain.insert_ref(coordref, copy=False)

            coords = []      
    #--- End: for

    f.delprop('grid_mapping')
#--- End: def

def _create_formula_terms_ref(f, key, coord, formula_terms,
                              attributes, ncvar_to_key,
                              coordref_field_pointers):
    '''

:Parameters:

    f : cf.Field

    key : str

    coord : cf.Coordinate

    formula_terms : str

    attributes : dict

    ncvar_to_key : dict

    coordref_field_pointers : set

:Returns:

    out : cf.CoordinateReference

'''        
    # Add the equation terms and references to their values to to
    # new auxiliary coordinate's coordinate reference.
    kwargs      = {}
    coord_terms = []

    ft = re.split('\s+|\s*:\s+', formula_terms)

    for term, ncvar in zip(ft[0::2], ft[1::2]):
        if ncvar in ncvar_to_key:
            # CASE 1: This variable is a coordinate of the field, so
            #         we point to it from the coordinate reference.
            value = ncvar_to_key[ncvar]
            coord_terms.append(term)

        elif ncvar not in attributes:
            # CASE 2: The value does not exist as a netCDF variable in
            #         this file
            value = None
            
        else:
            # CASE 3: This variable is not a coordinate of the field
            #         so it goes in to the coordinate reference as an
            #         independent field
            value = {'ncvar': ncvar}
            coordref_field_pointers.add(ncvar)
        #--- End: if
            
        kwargs[term] = value
    #--- End: for 

    coordref = CoordinateReference(coord.getprop('standard_name', None),
                                   crtype='formula_terms',
                                   coords=(key,),
                                   coord_terms=coord_terms,
                                   **kwargs)
    
    f.domain.insert_ref(coordref, copy=False)

    return coordref
#--- End: def

def _set_Data(nc, ncvar, f, variable, unpacked_dtype=False, cfa=False):
    '''

Set the Data attribute of a variable.

:Parameters:

    nc : netCDf4.Dataset

    ncvar : netCDF4.Variable

    f : Field

    variable : cf.Variable

    unpacked_dtype : False or numpy.dtype, optional

    cfa : bool, optional
        If True then netCDF file is a CFA file. By default it is
        assumed that the file is not a CFA file.

:Returns:

    None

:Examples: 

'''    
    iscfa_variable = variable.getprop('cf_role', None) == 'cfa_variable'

    if cfa and iscfa_variable:

        try:
            cfa_data = json_loads(variable.getprop('cfa_array'))
        except ValueError as error:
            raise ValueError(
                "Error during JSON-decoding of 'cfa_array' property: %s" %
                error)

        cfa_data['file']       = f.file
        cfa_data['Units']      = variable.Units      
        cfa_data['fill_value'] = variable.fill_value()
        cfa_data['_pmshape']   = cfa_data.pop('pmshape', ())
        cfa_data['_pmaxes']    = cfa_data.pop('pmdimensions', ())
        
        base = cfa_data.get('base', None)
        if base is not None:
            cfa_data['base'] = abspath(pathjoin(dirname(f.file), base))

        ncdimensions = variable.getprop('cfa_dimensions', '').split()
        dtype = ncvar.dtype
        if dtype.kind == 'S' and ncdimensions:
            strlen = len(nc.dimensions[ncdimensions[-1]])
            if strlen > 1:
                ncdimensions.pop()
                dtype = numpy_dtype('S%d' % strlen)
        #--- End: if
        cfa_data['dtype'] = dtype
        cfa_data['_axes'] = ncdimensions
        cfa_data['shape'] = [len(nc.dimensions[ncdim])
                             for ncdim in ncdimensions]

        for attrs in cfa_data['Partitions']:

            # FORMAT
            sformat = attrs.get('subarray', {}).pop('format', 'netCDF')
            if sformat is not None:
                attrs['format'] = sformat

            # DTYPE
            dtype = attrs.get('subarray', {}).pop('dtype', None)
            if dtype not in (None, 'char'):
                attrs['subarray']['dtype'] = numpy_dtype(dtype)

            # UNITS and CALENDAR
            units    = attrs.pop('punits', None)
            calendar = attrs.pop('pcalendar', None)
            if units is not None or calendar is not None:
                attrs['Units'] = Units(units, calendar)

            # AXES
            pdimensions = attrs.pop('pdimensions', None)
            if pdimensions is not None:
                attrs['axes'] = pdimensions

            # REVERSE
            reverse = attrs.pop('reverse', None)
            if reverse is not None:
                attrs['reverse'] = reverse

            # LOCATION: Change to python indexing (i.e. range does not
            #           include the final index)
            for r in attrs['location']:
                r[1] += 1

            # PART: Change to python indexing (i.e. slice range does
            #       not include the final index)
            part = attrs.get('part', None)
            if part:
                p = []
                for x in ast_literal_eval(part):
                    if isinstance(x, list):
                        if x[2] > 0:
                            p.append(slice(x[0], x[1]+1, x[2]))
                        elif x[1] == 0:
                            p.append(slice(x[0], None, x[2]))
                        else:
                            p.append(slice(x[0], x[1]-1, x[2]))
                    else:
                        p.append(list(x))
                #--- End: for
                attrs['part'] = p
        #--- End: for

        variable.delprop('cf_role')
        variable.delprop('cfa_array')
        if variable.hasprop('cfa_dimensions'):
            variable.delprop('cfa_dimensions')

        data = Data(loadd=cfa_data)

    else:        
        dtype = ncvar.dtype
        if unpacked_dtype is not False:
            dtype = numpy_result_type(dtype, unpacked_dtype)

        ndim  = ncvar.ndim
        shape = ncvar.shape
        size  = ncvar.size
        if size < 2:
            size = int(size)

        if dtype.kind == 'S' and ndim >= 1: #shape[-1] > 1:
            # Has a trailing string-length dimension
            strlen = shape[-1]
            shape = shape[:-1]
            size /= strlen
            ndim -= 1
            dtype = numpy_dtype('S%d' % strlen)
        #--- End: if

        filearray = NetCDFFileArray(file=f.file,
                                    ncvar=ncvar._name,
                                    dtype=dtype,
                                    ndim=ndim,
                                    shape=shape,
                                    size=size)
        
        data = Data(filearray,
                    units=variable.Units,
                    fill_value=variable.fill_value())
    #--- End: if

    return data
#--- End: def

def _is_cfa_private_variable(ncvar, cfa):
    '''

Return True if a netCDF variable is a CFA private variable.

:Parameters:

    ncvar : netCDF4.Variable

    cfa : bool
        If True then netCDF file is a CFA file. By default it is
        assumed that the file is not a CFA file.

:Returns:

    out : bool
        True if *cfa* is True and *ncvar* is a CFA private
        variable. Otherwise False.

:Examples: 

>>> if _is_cfa_private_variable(x, True):
...     print 'This is private CFA'

>>> False == _is_cfa_private_variable(x, False)
True

'''  
    return (cfa and 
            'cf_role' in ncvar.ncattrs() and 
            ncvar.getncattr('cf_role') == 'cfa_private')
#--- End: def

def is_netcdf_file(filename):
    '''Return True if the file is a netCDF file.

Note that the file type is determined by inspecting the file's
contents and any file suffix is not not considered.

:Parameters:

    filename : str

:Returns:

    out : bool

:Examples:

>>> is_netcdf_file('myfile.nc')
True
>>> is_netcdf_file('myfile.pp')
False
>>> is_netcdf_file('myfile.pdf')
False
>>> is_netcdf_file('myfile.txt')
False

    '''
    # Read the magic number 
    try:
        fh = open(filename, 'rb')
        magic_number = struct_unpack('=L', fh.read(4))[0]
    except struct_error:
        fh.close()
        return False
    else:
        fh.close()        
        if magic_number in (21382211, 1128547841, 1178880137, 38159427):
            return True
        else:
            return False
#--- End: def
