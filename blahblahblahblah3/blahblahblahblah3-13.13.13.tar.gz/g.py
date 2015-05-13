import zipimport

try:
    if isinstance(__loader__, zipimport.zipimporter):
        raise RuntimeError("Zipped imports are not supported, use something less terrible.")
except NameError:
    pass
