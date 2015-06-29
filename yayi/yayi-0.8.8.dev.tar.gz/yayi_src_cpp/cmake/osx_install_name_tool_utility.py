# simple script to handle the @rpath change of the boost, in order 
# to be able to create "bootle" like package

import sys
import os
import subprocess
import re
import shutil

def get_list_reference(path_dylib, pattern = None):
  """Returns the list of shared libraries referenced by the one given as argument"""
  p = subprocess.Popen(['otool', '-L', path_dylib], stdout=subprocess.PIPE)
  p.wait()
  
  if p.returncode != 0:
    return None
  
  relevant_part = re.compile('\s*(.*%s.+).dylib' % (pattern if pattern is not None else ''))
  
  # discard the first line
  list_dependencies = []
  for l in p.stdout.readlines()[1:]:
    t = re.search(relevant_part, l)
    if t is not None:
      list_dependencies.append(t.group(0).strip())
  
  return list_dependencies

def get_list_rpath(path_dylib):
  """Returns the list of rpath commands already in the shared library"""
  p = subprocess.Popen(['otool', '-l', path_dylib], stdout=subprocess.PIPE)
  p.wait()
  
  if p.returncode != 0:
    return None
    
  l_output = ''.join(p.stdout.readlines())
  relevant_part = re.compile('LC_RPATH.*path\s+(\S+)', re.MULTILINE | re.DOTALL)
  
  return relevant_part.findall(l_output)

def get_shared_library_id(path_dylib):
  """Returns the id of this shared library"""
  p = subprocess.Popen(['otool', '-D', path_dylib], stdout=subprocess.PIPE)
  p.wait()
  
  if p.returncode != 0:
    return None
    
  l_output = ''.join(p.stdout.readlines()[1:]).strip()
  return l_output



def relocate_dependencies(path_dylib, list_dependencies):
  # invoke the tool for all dependant libraries
  # we suppose they lie in the same path
  # we discard ourselves, we suppose there is no cycle
  # todo: remove the add_rpath is this one is already correct
  # todo: remove the id is this one is already correct
    
  already_copied = False
  for l in list_dependencies:
    bname = os.path.basename(l)
    
    if bname == os.path.basename(path_dylib):
      # the id is changed always at the end
      continue

    if not l.startswith('@rpath'):
        
      return_code = subprocess.call(['install_name_tool', '-change', l, '@rpath/' + bname, path_dylib])
      
    
  # change id
  new_shared_library_id = '@rpath/' + os.path.basename(path_dylib)
  if(get_shared_library_id(path_dylib) != new_shared_library_id):
    subprocess.call(['install_name_tool', '-id', new_shared_library_id, path_dylib])
  
  # add rpath to @loader_path
  list_rpath = get_list_rpath(path_dylib)
  if('@loader_path/.' not in list_rpath):
    subprocess.call(['install_name_tool', '-add_rpath', '@loader_path/.', path_dylib])
  
  return

def main(filename, output_path, pattern = None):
  
  output_path = os.path.abspath(output_path)
  
  if not os.path.exists(output_path):
    os.makedirs(output_path)
  if(os.path.abspath(os.path.dirname(filename)) != output_path):
    shutil.copy(filename, output_path)
  copied_dylib = os.path.join(output_path, os.path.basename(filename))  
  
  references = get_list_reference(filename, pattern = pattern)
  relocate_dependencies(copied_dylib, references)
  #relocated_references = get_list_reference(copied_dylib, pattern = pattern)
  return copied_dylib

def test():
  #filename = r'/Users/raffi/Code/SoftwareWorkshop/sw_thirdparties/osx/boost_1_55_0/stage/lib/libboost_graph-xgcc42-mt-1_55.dylib'
  filename = r'/Users/raffi/Personnel/YayiBitbucket/plugins/PythonPackage/build/lib.macosx-10.10-intel-2.7/yayi/bin/libboost_graph-clang-darwin42-mt-1_55.dylib'
  tmp_path = '/Users/raffi/tmp/boost_reloc_exp'
  
  print get_list_rpath(filename)
  print get_shared_library_id(filename)
  return 
  
  copied_dylib = main(filename, tmp_path, 'boost')
  
  l = get_list_reference(filename, pattern = 'boost')
  print '\t' + '\n\t'.join(l)
  
  ll = get_list_reference(copied_dylib, pattern = 'boost')
  print '\t' + '\n\t'.join(ll)
  
  
if __name__ == '__main__':
  
  #print sys.argv
  if(len(sys.argv) > 2):
    main(sys.argv[1],sys.argv[2], sys.argv[3] if len(sys.argv) >= 4 else None)
  else:
    test()
