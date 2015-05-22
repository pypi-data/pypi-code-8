"""Automatic Mercurial hooks"""

import os.path

import mercurial.extensions
import mercurial.hook
import mercurial.match
from mercurial.i18n import _


testedwith = "3.1.2"
buglink = "https://github.com/jribbens/hg-autohooks/issues"


PREPOST_HOOKS = (
    "add", "addremove", "annotate", "archive", "backout", "bisext",
    "bookmarks", "branch", "branches", "bundle", "cat", "clone", "commit",
    "config", "copy", "diff", "export", "forget", "graft", "grep", "heads",
    "help", "identify", "import", "incoming", "init", "locate", "log",
    "manifest", "merge", "outgoing", "parents", "paths", "phase", "pull",
    "push", "recover", "remove", "rename", "resolve", "revert", "root",
    "serve", "status", "summary", "tag", "tags", "unbundle", "update",
    "verify", "version"
)

NORMAL_HOOKS = (
    "changegroup", "commit", "incoming", "outgoing", "prechangegroup",
    "precommit", "prelistkeys", "preoutgoing", "prepushkey", "pretag",
    "pretxnopen", "pretxnclose", "txnclose", "txnabort", "pretxnchangegroup",
    "pretxncommit", "preupdate", "listkeys", "pushkey", "tag", "update"
)


def uisetup(ui):
    """Setup pre-/post- hooks"""
    for hooktype in PREPOST_HOOKS:
        ui.setconfig("hooks", "pre-" + hooktype + ".autohooks", autohook)
        ui.setconfig("hooks", "post-" + hooktype + ".autohooks", autohook)


def reposetup(ui, repo):
    """Setup normal hooks"""
    # pylint: disable=unused-argument
    for hooktype in NORMAL_HOOKS:
        ui.setconfig("hooks", hooktype + ".autohooks", autohook)


def _runhook(ui, repo, hooktype, filename, kwargs):
    """Run the hook in `filename` and return its result."""
    hname = hooktype + ".autohooks." + os.path.basename(filename)
    if filename.lower().endswith(".py"):
        try:
            mod = mercurial.extensions.loadpath(filename,
                "hghook.%s" % hname)
        except Exception:
            ui.write(_("loading %s hook failed:\n") % hname)
            raise
        return mercurial.hook._pythonhook(ui, repo, hooktype, hname,
            getattr(mod, hooktype.replace("-", "_")), kwargs, True)
    elif filename.lower().endswith(".sh"):
        return mercurial.hook._exthook(ui, repo, hname, filename, kwargs, True)
    return False


def autohook(ui, repo, hooktype, **kwargs):
    """Look for hooks inside the repository to run."""
    cmd = hooktype.replace("-", "_")
    if not repo or not cmd.replace("_", "").isalpha():
        return False
    result = False
    trusted = ui.configlist("autohooks", "trusted")
    if "" not in trusted:
        default_path = ui.config("paths", "default")
        if not default_path:
            return False
        for match in trusted:
            if default_path.startswith(match):
                break
        else:
            return False
    for hookdir in ("hg-autohooks", ".hg-autohooks"):
        dirname = os.path.join(repo.root, hookdir)
        if not os.path.exists(dirname):
            continue
        for leafname in os.listdir(dirname):
            if not leafname.startswith(cmd + "."):
                continue
            filename = os.path.join(dirname, leafname)
            result = _runhook(ui, repo, hooktype, filename, kwargs) or result
    return result
