import gdal
import osr

uris = [
    r"C:/Users/rich/Downloads/delete_ibe_InVEST_debug/InVEST_debug/dem",
    r"C:/Users/rich/Downloads/delete_ibe_InVEST_debug/InVEST_debug/erosivity",
    r"C:\Users\rich\Downloads\delete_ibe_InVEST_debug\InVEST_debug\erodibility",
    r"C:\Users\rich\Downloads\delete_ibe_InVEST_debug\InVEST_debug\nlcd2011_dc",
    r"C:\Users\rich\Documents\delete_ibe_sdr_debug\prepared_data\tiled_dem.tif"]

for uri in uris:
    dataset = gdal.Open(uri)
    projection_as_str = dataset.GetProjection()
    dataset_sr = osr.SpatialReference()
    dataset_sr.ImportFromWkt(projection_as_str)
    print uri
    print projection_as_str
    print dataset_sr.IsProjected()
    print ''
