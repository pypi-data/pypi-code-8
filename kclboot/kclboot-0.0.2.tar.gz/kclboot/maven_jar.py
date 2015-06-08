import os

try:
    # Python 3
    from urllib.request import urlretrieve
except ImportError:
    # Python 2
    from urllib import urlretrieve

MAVEN_PREFIX = 'http://search.maven.org/remotecontent?filepath='

class MavenJar:
    def __init__(self, group, artifact, version):
        self.group    = group
        self.artifact = artifact
        self.version  = version

    @property
    def filename(self):
        '''
        Filename in the format of {artifact}-{version}.jar
        '''
        return '{artifact}-{version}.jar'.format(
            artifact = self.artifact, 
            version  = self.version)

    @property
    def maven_url(self):
        '''
        Download-URL from Maven
        '''
        return '{prefix}/{path}/{artifact}/{version}/{filename}'.format(
            prefix   = MAVEN_PREFIX,
            path     = '/'.join(self.group.split('.')),
            artifact = self.artifact,
            version  = self.version,
            filename = self.filename)

    def download_to(self, folder):
        '''
        Download into a folder
        '''
        urlretrieve(self.maven_url, os.path.join(folder, self.filename))
