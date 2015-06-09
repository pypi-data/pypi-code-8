
from butterknife.subvol import Subvol
from butterknife.pool import LocalPool

class WebPool(LocalPool):

    def __init__(self, hostname, port=None, path=None, user=None, secure=False):
        self.secure = secure
        self.hostname = hostname
        self.port = port
        self.user = user
        self.path = path or "/api"
        
    def template_list(self, f=None):
        fh = urllib.request.urlopen("%s/template/" % self)
        for entry in json.loads(fh.read().decode("ascii"))["templates"]:
            yield entry["namespace"], entry["identifier"], entry["architectures"]

    def subvol_list(self):
        fh = urllib.request.urlopen("%s/subvol/" % self)
        for entry in json.loads(fh.read().decode("ascii"))["subvolumes"]:
            yield Subvol(entry["path"])

    def __str__(self):
        url = "https" if self.secure else "http"
        url += "://"
        if self.user:
            url += "%s@" % self.user
        url += self.hostname
        if self.port:
            url += ":%d" % self.port
        url += self.path
        return url

    def receive(self, fh, subvol, parent_subvol=None):
        raise NotImplementedError("Unable to push via HTTP/HTTPS")

    def send(self, subvol, parent_subvol=None):
        cmd = "curl",
        cmd += "-A", "Butterknife-Util/0.1"
        if self.secure:
            cmd += "--compressed",
        url = "%s%s" % (self, subvol)
        if parent_subvol:
            url += "?parent=%s" % parent_subvol
        cmd += url,
            
        click.echo("Executing: %s" % " ".join(cmd))
        return subprocess.Popen(cmd, stdout=subprocess.PIPE, close_fds=True)
