from __future__ import print_function
import os, subprocess

from webassets.filter import Filter
from webassets.exceptions import FilterError

__all__ = ('LiveScript')


class LiveScript(Filter):
  name = 'livescript'

  options = {
    'coffee_deprecated': (False, 'COFFEE_PATH'),
    'coffee_bin': ('binary', 'COFFEE_BIN'),
    'no_bare': 'COFFEE_NO_BARE',
    }

  def output(self, _in, out, **kwargs):
    bin = "lsc"
    args = "-csp" + ("" if self.no_bare else 'b')
    try:
      proc = subprocess.Popen([bin, args],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=(os.name == 'nt'))
    except OSError as e:
      if e.errno == 2:
        raise Exception("livescript not installed or in system path for webassets")
      raise
    stdout, stderr = proc.communicate(_in.read().encode('utf-8'))

    if proc.returncode != 0:
      raise FilterError(('livescript: subprocess had error: stderr=%s, '+
        'stdout=%s, returncode=%s') % (stderr, stdout, proc.returncode))
    elif stderr:
      print("livescript filter has warnings:", stderr)

    out.write(stdout.decode('utf-8'))
