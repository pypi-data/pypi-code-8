#!/usr/bin/env python

# example to create http server so cluster status can be monitored
# with browser client

# (sample) computation to execute on the nodes
def compute(n):
    import time, socket
    time.sleep(n)
    host = socket.gethostname()
    return (host, n)

if __name__ == '__main__':
    import dispy, random

    # import dispy's httpd module, create http server
    import dispy.httpd
    http_server = dispy.httpd.Server()

    # create cluster with 'cluster_status' parameter set to http server's function
    cluster = dispy.JobCluster(compute, cluster_status=http_server.cluster_status)

    # cluster status can now be viewed in web browser at
    # http://<host>:8181 where <host> is name or IP address of
    # computer running this program

    for i in range(8):
        cluster.submit(random.randint(15, 20))
    
    cluster.wait() # wait for all jobs to finish
    cluster.close()
    http_server.shutdown() # this waits until browser gets all updates
