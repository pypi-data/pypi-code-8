__author__ = 'Stephan Conrad <stephan@conrad.pics>'

from exon.utils.command.execute import exec as run
import os
import tempfile

def getLdifByDn(file, dn):
    """
    Returns a LDIF File by a DN
    :param file: ldb file
    :param dn: dn for the object
    :return: output from ldap query or error msg
    """
    cmd = "ldbsearch -H %s -s base -b '%s'" % (
        file,
        dn
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

def modifyLdap(file, ldifLines = []):
    if type(ldifLines) != list:
        raise Exception('ldifLines must be a list')
    with tempfile.NamedTemporaryFile() as f:
        for line in ldifLines:
            s = '{}{}'.format(line, os.linesep)
            f.write(s.encode('UTF-8'))
        f.flush()
        cmd = 'ldbmodify -H %s %s' % (file, f.name)
        out = run(cmd)
        if out.rc == 0:
            return out.stdout
        else:
            return {
                "rc": out.rc,
                "stdout": out.stdout,
                "stderr": out.stderr,
                'ldif': ldifLines
            }
