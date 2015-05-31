__author__ = 'Stephan Conrad <stephan@conrad.pics>'

from exon.utils.command.execute import exec as run
import os

def runLdapQuery(file, query, fields = []):
    """
    Runs a SAMBA LDAP query
    :param file: ldb file
    :param query: ldap query string
    :param fields: array or tupel of fields to get
    :return: output from ldap query or error msg
    """
    if not os.path.exists(file):
        raise Exception("file %s not found" % file)
    cmd = "ldbsearch -H %s '%s' %s" % (
        file,
        query,
        " ".join(fields)
    )
    out = run(cmd)
    if out.rc == 0:
        return out.stdout
    else:
        return {
            "rc": out.rc,
            "stdout": out.stdout,
            "stderr": out.stderr,
        }