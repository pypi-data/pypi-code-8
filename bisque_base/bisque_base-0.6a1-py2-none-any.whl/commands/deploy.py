import os
import optparse
import shutil


JSBASE = "bisque_web/bq/web/public/"

class deploy(object):
    desc = 'Advanced deployment options: public'
    def __init__(self, version):
        parser = optparse.OptionParser(
                    usage="%prog deploy [public]",
                    version="%prog " + version)
        options, args = parser.parse_args()
        self.args = args
        self.options = options

    def run(self):
        #if 'public' in self.args:
        self.public_dir = self.args.pop(0) if len(self.args)>0 else 'public'
        self.deploy_public()



    def deploy_public(self):
        ''
        from bq.util.copylink import copy_symlink
        import pkg_resources
        import shutil

        # dima: deploy fails under windows with access denied, need to clean dir first
        if os.name == 'nt':
            try:
                print "Cleaning up %s" % self.public_dir
                shutil.rmtree(self.public_dir, ignore_errors=True)
            except OSError, e:
                pass

        try:
            print "Creating %s" % self.public_dir
            os.makedirs (self.public_dir)
        except OSError, e:
            pass

        rootdir = os.getcwd()
        coredir = os.path.join(rootdir, JSBASE).replace('/', os.sep)

        #os.chdir(self.public_dir)
        #currdir = os.getcwd()

        for x in pkg_resources.iter_entry_points ("bisque.services"):
            try:
                #print ('found static service: ' + str(x))
                try:
                    service = x.load()
                except Exception, e:
                    print "Problem loading %s: %s" % (x, e)
                    continue
                if not hasattr(service, 'get_static_dirs'):
                    print "service %s has no statics" % service
                    continue
                staticdirs  = service.get_static_dirs()

                for d,r in staticdirs:
                    dest = os.path.join(self.public_dir, x.name)
                    if os.path.exists (dest):
                        shutil.rmtree (dest)
                    shutil.copytree (r, dest)
            except Exception,e :
                print "Exception: ", e


    def deploy_old(self):

        for x in pkg_resources.iter_entry_points ("bisque.services"):
            try:
                #print ('found static service: ' + str(x))
                try:
                    service = x.load()
                except Exception, e:
                    print "Problem loading %s: %s" % (x, e)
                    continue
                if not hasattr(service, 'get_static_dirs'):
                    print "service %s has no statics" % service
                    continue
                staticdirs  = service.get_static_dirs()
                for d,r in staticdirs:
                    print ( "adding static: %s %s" % ( d,r ))
                    static_path =  r[len(d)+1:]
                    print "basepath =", os.path.dirname(static_path)
                    basedir = os.path.dirname(static_path)
                    try:
                        #os.makedirs (os.path.join(self.dir, os.path.dirname(static_path)))
                        print "static path=", static_path
                        os.makedirs (os.path.dirname(static_path))

                    except OSError,e:
                        pass
                    #print "link ", (r, os.path.join('public', static_path))
                    dest = os.path.join(currdir, static_path)
                    if os.path.exists (dest):
                        os.unlink (dest)
                    relpath = os.path.relpath(r, os.path.dirname(dest))
                    print "%s -> %s" % (relpath, dest)

                    copydir = os.getcwd()
                    os.chdir(basedir)
                    copy_symlink (relpath, dest)
                    os.chdir(copydir)
                    print "Deployed ", r
            except Exception, e:
                print "Exception: ", e
                pass
        # Link all core dirs
        import glob
        for l in glob.glob(os.path.join(coredir, '*')):
            dest = os.path.join(currdir, os.path.basename(l))
            if os.path.exists (dest):
                os.unlink (dest)

            relpath = os.path.relpath(l, currdir)
            #print "%s -> %s " % (relpath, dest)
            copy_symlink (relpath, dest)

        # ensure b.js exists and will be picked up by the paster static file server
        #src = os.path.join(rootdir, 'bqcore/bq/core/public/js/bq_api.js')
        dst = os.path.join(rootdir, JSBASE, 'b.js')
        with open(dst, 'a'):
            pass

        # finish
        os.chdir (rootdir)

