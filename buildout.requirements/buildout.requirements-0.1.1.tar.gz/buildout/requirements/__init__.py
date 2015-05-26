""" Implement requirements dumping for as buildout plugin. """

import os
import logging
import zc.buildout.easy_install
import pkg_resources

logger = zc.buildout.easy_install.logger

required_by = {}


def _log_requirement(ws, req):
    ws = list(ws)
    ws.sort()
    for dist in ws:
        if req in dist.requires():
            req_ = str(req)
            dist_ = str(dist)
            if req_ in required_by and dist_ not in required_by[req_]:
                required_by[req_].append(dist_)
            else:
                required_by[req_] = [dist_]
            logger.debug('  required by %s.' % dist)


def enable_dumping_picked_versions(old_get_dist):
    """ Monkey path __get_dist to store requirements. """
    def get_dist(self, requirement, ws, **kwargs):
        dists = old_get_dist(self, requirement, ws, **kwargs)

        for dist in dists:
            if not (dist.precedence == pkg_resources.DEVELOP_DIST) and \
               not kwargs.get('for_buildout_run', False):
                    self.__all_picked_versions[dist.project_name] \
                        = dist.version
        return dists
    return get_dist


def dump_picked_versions(old_logging_shutdown, file_name, overwrite):
    """ Monkey patch logging_shutdown to write requirements file. """
    def logging_shutdown():

        picked_versions_top = ''
        picked_versions_bottom = ''
        picked = zc.buildout.easy_install.Installer \
                                         .__all_picked_versions.items()
        for d, v in sorted(picked):
            if d in required_by:
                req_ = '\n#Required by:\n#' + '\n#'.join(required_by[d]) + '\n'
                picked_versions_bottom += '%s%s==%s\n' % (req_, d, v)
            else:
                picked_versions_top += '%s==%s\n' % (d, v)

        picked_versions = picked_versions_top + picked_versions_bottom

        if file_name is not None:
            if not os.path.exists(file_name):
                print('*********************************************')
                print('Writing picked versions to %s' % file_name)
                print('*********************************************')
                open(file_name, 'w').write(picked_versions)
            elif overwrite:
                print('*********************************************')
                print('Overwriting %s' % file_name)
                print('*********************************************')
                open(file_name, 'w').write(picked_versions)
            else:
                print('*********************************************')
                print('Skipped: File %s already exists.' % file_name)
                print('*********************************************')
        else:
            print('*************** PICKED VERSIONS ****************')
            print(picked_versions)
            print('*************** /PICKED VERSIONS ***************')

        old_logging_shutdown()
    return logging_shutdown


def install(buildout):
    """ Install the requirements buildout extension. """
    file_name = 'dump-requirements-file' in buildout['buildout'] and \
                buildout['buildout']['dump-requirements-file'].strip() or \
                None

    overwrite = 'overwrite-requirements-file' not in buildout['buildout'] or \
                buildout['buildout']['overwrite-requirements-file'].lower() \
                in ['yes', 'true', 'on']

    zc.buildout.easy_install.Installer.__all_picked_versions = {}
    zc.buildout.easy_install._log_requirement = _log_requirement
    zc.buildout.easy_install.Installer._get_dist = \
        enable_dumping_picked_versions(
            zc.buildout.easy_install.Installer._get_dist)

    logging.shutdown = dump_picked_versions(logging.shutdown,
                                            file_name,
                                            overwrite)
