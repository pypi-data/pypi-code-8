# -*- coding: utf-8 -*-
from numpy import array as numpy_array
from numpy import append as numpy_append
from .data.data import Data
from .functions import REGRID_LOGGING
from . import _found_ESMF
if _found_ESMF:
    import ESMF

class Regrid:
    """

Class containing all the methods required for accessing ESMF regridding through
ESMPY and the associated utility methods.

    """
    
    def __init__(self, srcfield, dstfield, srcfracfield, dstfracfield,
                 conservative=True):
        """

Creates a handle for regridding fields from a source grid to a destination grid
that can then be used by the run_regridding method.

:Parameters:

    srcfield: ESMF.Field
        The source field with an associated grid to be used for regridding.

    dstfield: ESMF.Field
        The destination field with an associated grid to be used for
        regridding.

    srcfracfield: ESMF.Field
        A field to hold the fraction of the source field that contributes to 
        conservative regridding.

    dstfracfield: ESMF.Field
        A field to hold the fraction of the source field that contributes to 
        conservative regridding.

    conservative: bool, optional
        By default the regridding method is conservative. If this parameter is
        set to False then multilinear interpolation is used.
    
        """
        # create a handle to the regridding method
        method = ESMF.RegridMethod.CONSERVE if conservative \
                 else ESMF.RegridMethod.BILINEAR
        self.regridSrc2Dst = ESMF.Regrid(srcfield, dstfield, regrid_method=method,
                                         src_mask_values=numpy_array([0], dtype='int32'),
                                         dst_mask_values=numpy_array([0], dtype='int32'),
                                         src_frac_field=srcfracfield,
                                         dst_frac_field=dstfracfield,
                                         unmapped_action=ESMF.UnmappedAction.IGNORE)
    #--- End: def
    
    def release(self):
        """

Free the memory associated with the ESMF.Regrid instance.

        """
        self.regridSrc2Dst.release()
    #--- End: def
    
    @staticmethod
    def initialize():
        """

Check whether ESMF has been found. If not raise an import error. Initialise the
ESMPy manager. Whether logging is enabled or not is determined by
cf.REGRID_LOGGING. If it is then logging takes place after every call to ESMPy.

:Returns:

    manager: ESMF.Manager
        A singleton instance of the ESMPy manager.

        """
        if not _found_ESMF:
            raise ImportError('ESMPy is needed to support regridding.')
        
        if REGRID_LOGGING():
            manager = ESMF.Manager(logkind=ESMF.LogKind.MULTI, debug=True)
        else:
            manager = ESMF.Manager(logkind=ESMF.LogKind.NONE)
        return manager
    
    @staticmethod
    def create_grid(lon, lat, cyclic, mask=None):
        """

Create an ESMPy grid given 1D latitude and 1D longitude coordinates for use as
a source or destination grid in regridding. Optionally the grid may have an
associated mask.

:Parameters:

    lon : DimensionCoordinate
        The DimensionCoordinate containing the 1D longitude coordinates.

    lat : DimensionCoordinate
        The DimensionCoordinate containing the 1D latitude coordinates.

    cyclic : bool
        Whether or not the longitude is cyclic.

    mask : numpy.ndarray, optional
        An optional numpy array of booleans containing the grid points to mask.
        Where the elements of mask are True the output grid is masked.

:Returns:

    out: ESMF.Grid
        The resulting ESMPy grid for use as a source or destination grid in
        regridding.

        """
        # Check the bounds for contiguity if they exist
        if lon.hasbounds and not lon.contiguous(overlap=False):
            raise ValueError('The longitude bounds must be contiguous.')
        #--- End: if
        if lat.hasbounds and not lon.contiguous(overlap=False):
            raise ValueError('The latitude bounds must be contiguous.')
        #--- End: if
        
        # Get the bounds, creating them if they do not exist
        x_bounds = lon.get_bounds(create=True).array
        y_bounds = lat.get_bounds(create=True).clip(-90, 90, 'degrees').array
        
        # Create empty grid
        max_index = numpy_array([lon.size, lat.size], dtype='int32')
        staggerLocs = [ESMF.StaggerLoc.CORNER, ESMF.StaggerLoc.CENTER]
        if cyclic:
            grid = ESMF.Grid(max_index, num_peri_dims=1, staggerloc=staggerLocs)
        else:
            grid = ESMF.Grid(max_index, staggerloc=staggerLocs)
        #--- End: if
        
        # Populate grid centres
        x, y = 0, 1
        gridXCentre = grid.get_coords(x, staggerloc=ESMF.StaggerLoc.CENTER)
        gridXCentre[...] = lon.array.reshape((lon.size, 1))
        gridYCentre = grid.get_coords(y, staggerloc=ESMF.StaggerLoc.CENTER)
        gridYCentre[...] = lat.array.reshape((1, lat.size))
        
        # Populate grid corners
        gridCorner = grid.coords[ESMF.StaggerLoc.CORNER]
        if cyclic:
            gridCorner[x][...] = x_bounds[:, 0].reshape(lon.size, 1)
        else:
            gridCorner[x][...] = numpy_append(x_bounds[:, 0],
                                     x_bounds[-1, 1]).reshape(lon.size + 1, 1)
        #--- End: if
        y_bounds = numpy_append(y_bounds[:, 0], y_bounds[-1, 1])
        gridCorner[y][...] = y_bounds.reshape(1, lat.size + 1)
        
        # Add the mask if appropriate
        if not mask is None:
            gmask = grid.add_item(ESMF.GridItem.MASK)
            gmask[...] = 1
            gmask[mask] = 0
        #--- End: if
        
        return grid
    #--- End: def
    
    @staticmethod
    def create_2Dgrid(lon, lat, order, mask=None):
        """

Create an ESMPy grid given 2D latitude and 2D longitude coordinates for use as
a source or destination grid in regridding. Optionally the grid may have an
associated mask.

:Parameters:

    lon: AuxiliaryCoordinate
        The AuxiliaryCoordinate containing the 2D longitude coordinates.

    lat : AuxiliaryCoordinate
        The AuxiliaryCoordinate containing the 2D latitude coordinates.

    order : tuple
        A tuple indicating the order of the x and y axes.

    mask : numpy.ndarray, optional
        An optional numpy array of booleans containing the grid points to mask.
        Where the elements of mask are True the output grid is masked.

:Returns:

    out: ESMF.Grid
        The resulting ESMPy grid for use as a source or destination grid in
        regridding.

    out: bool
        A boolean indicating whether or not the grid has bounds.

        """
        # Get the shape of the grid
        shape = lon.transpose(order).shape
        if lat.shape != lon.shape:
            raise ValueError('The longitude and latitude coordinates must' +
                             ' have the same shape.')
        
        # Check whether bounds exist or not, and get them if they do
        hasbounds = lon.hasbounds and lat.hasbounds
        if hasbounds:
            x_bounds = lon.get_bounds().array
            y_bounds = lat.get_bounds().clip(-90, 90, 'degrees').array
        
        # Create empty grid
        max_index = numpy_array(shape, dtype='int32')
        if hasbounds:
            staggerLocs = [ESMF.StaggerLoc.CORNER, ESMF.StaggerLoc.CENTRE]
        else:
            staggerLocs = ESMF.StaggerLoc.CENTER
        grid = ESMF.Grid(max_index, staggerloc=staggerLocs)
        
        # Populate grid centres
        x, y = 0, 1
        gridXCentre = grid.get_coords(x, staggerloc=ESMF.StaggerLoc.CENTER)
        gridXCentre[...] = lon.transpose(order).array
        gridYCentre = grid.get_coords(y, staggerloc=ESMF.StaggerLoc.CENTER)
        gridYCentre[...] = lat.transpose(order).array
        
        # Populate grid corners if there are bounds
        if hasbounds:
            gridCorner = grid.coords[ESMF.StaggerLoc.CORNER]
            x_bounds = numpy_append(x_bounds[:, 0], x_bounds[-1, 1])
            gridCorner[x][...] = x_bounds.transpose(order).array
            y_bounds = numpy_append(y_bounds[:, 0], y_bounds[-1, 1])
            gridCorner[y][...] = y_bounds.transpose(order).array
        
        
        # Add the mask if appropriate
        if not mask is None:
            gmask = grid.add_item(ESMF.GridItem.MASK)
            gmask[...] = 1
            gmask[mask] = 0
        #--- End: if
        
        return grid, hasbounds
    #--- End: def

    @staticmethod
    def create_cartesian_grid(coords, mask=None):
        """

Create a cartesian grid with between 1 and 3 dimensions given a tuple or list
of dimension coordinates and optionally a mask. The number of coordinates
passed will determine the dimensionality of the grid.

:Parameters:

    coords : tuple or list of cf.DimensionCoordinate objects
        The coordinates specifying the grid. There must be between 1 and 3
        elements.

    mask : numpy.ndarray, optional
        An optional numpy array of booleans containing the grid points to mask.
        Where the elements of mask are True the output grid is masked.

        """
        
        # Test the dimensionality of the list of coordinates
        ndim = len(coords)
        if ndim < 2 or ndim > 3:
            raise ValueError('Cartesian grid must have 2 or 3 dimensions.')
        #--- End: if
        
        shape = list()
        for coord in coords:
            shape.append(coord.size)
        
        # Initialize the grid
        max_index = numpy_array(shape, dtype='int32')
        staggerLocs = [ESMF.StaggerLoc.CORNER, ESMF.StaggerLoc.CENTER]
        grid = ESMF.Grid(max_index, coord_sys=ESMF.CoordSys.CART,
                         staggerloc=staggerLocs)
        
        # Populate the grid centres
        for d in xrange(0, ndim):
            gridDCentre = grid.get_coords(d, staggerloc=ESMF.StaggerLoc.CENTER)
            gridDCentre[...] = coords[d].array.reshape([shape[d] if x == d else 1
                                                       for x in xrange(0, ndim)])
        #--- End: for
        
        # Populate grid corners
        gridCorner = grid.coords[ESMF.StaggerLoc.CORNER]
        for d in xrange(0, ndim):
            if coords[d].hasbounds and not coords[d].contiguous(overlap=False):
                raise ValueError('Coordinate ' + d + ' does not have contiguous bounds.')
            #--- End: if
            boundsD = coords[d].get_bounds(create=True).array
            boundsD = numpy_append(boundsD[:, 0], boundsD[-1, 1])
            gridCorner[d][...] = boundsD.reshape([shape[d] + 1 if x == d else 1
                                                  for x in xrange(0, ndim)])
        
        # Add the mask if appropriate
        if not mask is None:
            gmask = grid.add_item(ESMF.GridItem.MASK)
            gmask[...] = 1
            gmask[mask] = 0
        #--- End: if
        
        return grid
    #--- End: def

    @staticmethod
    def create_field(grid, name):
        """

Create an ESMPy field for use as a source or destination field in regridding
given an ESMPy grid and a name.

:Parameters:

    grid : ESMF.Grid
        The ESMPy grid to use in creating the field.

    name : str
        The name to give the field.

:Returns:

    out : ESMF.Field
        The resulting ESMPy field for use as a source or destination field in
        regridding.

        """
        field = ESMF.Field(grid, name)
        return field
    #--- End: def
    
    def run_regridding(self, srcfield, dstfield):
        dstfield = self.regridSrc2Dst(srcfield, dstfield,
                                      zero_region=ESMF.Region.SELECT)
        return dstfield
    #--- End: def
    
    @staticmethod
    def concatenate_data(data_list, axis):
        """

Concatenates a list of Data objects into a single Data object along the
specified access (see cf.Data.concatenate for details). In the case that
the list contains only one element, that element is simply returned.

:Parameters:

    data_list : list
        The list of data objects to concatenate.

    axis : int
        The axis along which to perform the concatenation.

:Returns:

    out : Data
        The resulting single Data object.

        """
        if len(data_list) > 1:
            return Data.concatenate(data_list, axis=axis)
        else:
            assert len(data_list) == 1
            return data_list[0]
        #--- End: if
    #--- End: def
    
    @staticmethod
    def reconstruct_sectioned_data(sections):
        """

Expects a dictionary of Data objects with ordering information as keys, as
output by the section method when called with a Data object. Returns a
reconstructed cf.Data object with the sections in the original order.

:Parameters:

    sections : dict
        The dictionary or Data objects with ordering informationa as keys.

:Returns:

    out : Data
        The resulting reconstructed Data object.

        """
        ndims = len(sections.keys()[0])
        for i in range(ndims - 1, -1, -1):
            keys = sorted(sections.keys())
            if i==0:
                if keys[0][i] is None:
                    assert len(keys) == 1
                    return sections.values()[0]
                else:
                    data_list = []
                    for k in keys:
                        data_list.append(sections[k])
                    return Regrid.concatenate_data(data_list, i)
                #--- End: if
            else:
                if keys[0][i] is None:
                    pass
                else:
                    new_sections = {}
                    new_key = keys[0][:i]
                    data_list = []
                    for k in keys:
                        if k[:i] == new_key:
                            data_list.append(sections[k])
                        else:
                            new_sections[new_key] = Regrid.concatenate_data(data_list, i)
                            new_key = k[:i]
                            data_list = [sections[k]]
                        #--- End: if
                    new_sections[new_key] = Regrid.concatenate_data(data_list, i)
                    sections = new_sections
                #--- End: if
            #--- End: if
    #--- End: def
    
    @staticmethod
    def get_latlong(f, f_2D_latlong, name):
        """
Retrieve the latitude and longitude coordinates of a field for regridding and
the associated informarion required. If f_2D_latlong is specified to be true it
is expected that the auxiliary coordinates returned by f.aux('X') and
f.aux('Y') will be 2D longitude and latitude coordinates.

:Parameters:

    f : Field
        The field to retrieve coordinates from.

    f_2D_latlong : bool
        Whether to retrieve 2D auxilliary coordinates or if not 1D dimension
        coordinates.

    name : string
        A name to identify the field in error messages.

:Returns:

    x : Coordinate
        The x coordinate (1D dimension coordinate or 2D auxilliary coordinate).

    y : Coordinate
        The y coordinate (1D dimension coordinate or 2D auxilliary coordinate).

    x_key : string
        The key of the x dimension coordinate.

    y_key : string
        The key of the y dimension coordinate.

    x_index : int
        The index of the x axis.

    y_index : int
        The index of the y axis.

    x_size : int
        The size of the x dimension coordinate.

    y_size : int
        The size of the y dimension coordinate.

        """
        # Retrieve the field's X and Y dimension coordinates
        x = f.dims('X')
        y = f.dims('Y')
        if len(x) != 1 or len(y) != 1:
            raise ValueError('Unique dimension coordinates specifying the X' +
                             ' and Y axes of the ' + name + ' field not found.')
        #--- End: if
        x_key, x = x.popitem()
        y_key, y = y.popitem()
        if not f_2D_latlong:
            if not x.Units.islongitude:
                raise ValueError('X dimension coordinate of the ' + name +
                                 ' field does not have CF-compliant units' +
                                 ' of longitude.')
            #--- End: if
            if not y.Units.islatitude:
                raise ValueError('Y dimension coordinate of the ' + name +
                                 ' field does not have CF-compliant units' +
                                 ' of latitude.')
            #--- End: if
        #--- End: if
        x_index = f.data_axes().index(x_key)
        y_index = f.data_axes().index(y_key)
        x_size = x.size
        y_size = y.size

        # If 2D latitude and longitude coordinates for the field are expected
        # retrieve them from the auxiliary coordinates.
        if f_2D_latlong:
            lon_found = False
            lat_found = False
            for aux in f.auxs(ndim=2).values():
                if aux.Units.islongitude:
                    if lon_found:
                        raise ValueError('The 2D auxiliary longitude coordinate' +
                                         ' of the ' + name + ' field is not unique.')
                    else:
                        lon_found = True
                        x = aux
                    #--- End: if
                #--- End: if
                if aux.Units.islatitude:
                    if lat_found:
                        raise ValueError('The 2D auxiliary latitude coordinate' +
                                         ' of the ' + name + ' field is not unique.')
                    else:
                        lat_found = True
                        y = aux
                    #--- End: if
                #--- End: if
            if not lon_found or not lat_found:
                raise ValueError('Both 2D longitude and 2D latitude auxiliary' +
                                 ' coordinates were not found for the ' + name +
                                 ' field.')
        #--- End: if
        
        return x, y, x_key, y_key, x_index, y_index, x_size, y_size
    #--- End: def
    
#--- End: class
