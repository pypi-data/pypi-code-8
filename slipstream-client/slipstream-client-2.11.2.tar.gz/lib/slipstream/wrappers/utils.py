from slipstream.exceptions.Exceptions import ExecutionException


def get_allowed_provisioning_failures_per_node(node_instances):
    """Return number of tolerable failures per node in the deployment.
    :param node_instances: list of all node instances of the deployment
    :type node_instances: list of <NodeInstance> objects
    :return: number of tolerable failures per node
    :rtype: dict {'<node_name>': int, }
    """
    max_failures_per_node = {}
    for ni in node_instances:
        if ni.get_node_name() not in max_failures_per_node:
            try:
                max_failures = int(ni.get_max_provisioning_failures())
            except ValueError:
                raise ExecutionException("Failed to convert 'max provisioning "
                                         "failures' to int for node %s." % ni.get_node_name())
            max_failures_per_node[ni.get_node_name()] = max_failures
    return max_failures_per_node

