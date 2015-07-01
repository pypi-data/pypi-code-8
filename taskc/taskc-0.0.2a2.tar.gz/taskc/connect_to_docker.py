from simple import TaskdConnection
import logging
def manual():
    # Task 2.3.0 doesn't let you have a cacert if you enable trust
    tc = TaskdConnection()
    tc.client_cert = "/home/jack/.task/docker/client.cert.pem"
    tc.client_key = "/home/jack/.task/docker/client.key.pem"
    tc.cacert_file = "/home/jack/.task/docker/ca.cert.pem"
    tc.server = "172.17.0.51"
    tc.group = "Public"
    tc.username = "jack"
    tc.uuid = "07751281-b3d4-4d59-9f4d-ffdeb92b7135"
    return tc


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    taskd = manual()
    taskd.connect()
    resp =  taskd.pull()
    print resp.as_string()
    from IPython import embed
    embed()