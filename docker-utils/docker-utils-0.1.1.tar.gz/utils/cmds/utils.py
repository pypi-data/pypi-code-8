import os


def get_service(project):
    cur = os.getcwd()

    def walk(directory):
        if 'Dockerfile' in os.listdir(directory):
            return os.path.basename(directory)

        new = os.path.dirname(directory)
        if new == directory:
            raise ValueError('No project found.')
        return walk(new)

    service = walk(cur)
    if service not in [s.name for s in project.services]:
        raise ValueError('Not a valid project: {0}'.format(service))

    return service


def get_container(project, service):
    containers = project.containers(service_names=[service])
    if not containers:
        raise ValueError('No containers found for: {0}. '.format(service))
    return containers[0]
