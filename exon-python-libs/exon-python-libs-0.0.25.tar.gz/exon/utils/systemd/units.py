__author__ = 'Stephan Conrad <stephan@conrad.pics>'

from exon.utils.command.execute import exec as run

class Units(object):

    @classmethod
    def restart(cls, unit):
        out = run('systemctl restart %s' % unit)
        if out.rc == 0:
            return True
        else:
            return False