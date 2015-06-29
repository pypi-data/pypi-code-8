
project_name = 'Yayi'

__doc__ = "Image processing and mathematical morphology library in C++ and Python"""
__author__ = "Raffi Enficiaud"
__all__ = []

_loaded = False

def _load_yayi_shared_libraries():
    import os, sys, imp, types, datetime
    pjoin = os.path.join

    yayi_libraries = [('Common', 'COM'), ('ImageCore', 'CORE'), ('IO', 'IO'),
                      ('StructuringElement', 'SE'), ('LowLevelMorphology', 'LMM'),
                      ('PixelProcessing', 'PIX'), ('Label', 'LAB'),
                      ('Segmentation', 'SEG'), ('Distances', 'DIST'),
                      ('Measurements', 'MEAS'), ('Reconstruction', 'REC'),
                      ('NeighborhoodProcessing', 'NP')]


    yayi_python_binary_name  = "YAYI"
    if not os.environ.has_key("YAYIPATH"):
      yayi_bin_dir = pjoin(os.path.dirname(__file__), "bin")
    else:
      yayi_bin_dir = os.environ["YAYIPATH"]

    suffixes = [i[0] for i in imp.get_suffixes()]

    for current in yayi_libraries:
        module_name = 'Yayi' + current[0] + 'Python'
        print '\tLoading', module_name
        if(not sys.modules.has_key(module_name)):
            mod = None
            for suf in suffixes:
                binary_name = module_name + suf
                try:
                    #filename = resource_filename(Requirement.parse(project_name), binary_name)
                    filename = os.path.join(os.path.dirname(__file__), 'bin', binary_name)
                    print '\t\tattempt ', os.path.abspath(filename)
                    mod = imp.load_dynamic(module_name, filename)#pjoin(yayi_bin_dir, binary_name))
                except Exception, e:
                    continue

                if(mod):
                    break

            if(mod is None):
                raise Exception('Cannot load ' + module_name)
        else:
            mod = sys.modules[module_name]

        globals()[current[1]] = mod
        __all__.append(current[1])


    print __name__, ' IS MY NAME'
    d = COM.current_build_date()
    print
    print '#' * 15
    print
    print '\tYAYI library version %s (compiled %s) loaded' % (COM.current_build_version(), d)
    for i in globals().items():
        if(i[0] in __all__ and type(i[1]) is types.ModuleType):
            print '\t\t%7s ->\'%s\'<-' % (i[0], os.path.abspath(i[1].__file__))
    print
    print '#' * 30
    print

if not _loaded:
  _load_yayi_shared_libraries()
  _loaded = True
