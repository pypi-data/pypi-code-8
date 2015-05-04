#!/usr/bin/env python

# example to create http server so cluster can be monitored / managed
# with a web browser

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
    http_server = dispy.httpd.DispyHTTPServer()

    # create cluster
    cluster = dispy.JobCluster(compute)

    # pass cluster to HTTP server so the cluster can be managed with web browser
    http_server.cluster(cluster)

    # cluster can now be monitored / managed in web browser at
    # http://<host>:8181 where <host> is name or IP address of
    # computer running this program

    for i in range(8):
        cluster.submit(random.randint(15, 20))
    
    cluster.wait() # wait for all jobs to finish
    http_server.shutdown() # this waits until browser gets all updates
    cluster.close()
