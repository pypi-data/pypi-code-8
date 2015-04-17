import getpass
import json
import requests

import util
import auth


def login(username, password, cloud, endpoint):
    if not username:
        username = raw_input('Username: ')
    if not password:
        password = getpass.getpass()

    api_endpoint = endpoint
    if api_endpoint is None:
        api_endpoint = auth.get_api_endpoint(cloud)
    url = api_endpoint + 'generate-api-token/'
    payload = {'username': username, 'password': password}
    r = requests.post(url, payload)
    d = json.loads(r.text)
    token = d['token']
    auth.save_token(api_endpoint, token)
    print 'Successfully logged in as {}.'.format(username)


def logout():
    auth.delete_token()
    print 'Bye'


def service_create(image, name, do_not_start, target_num_instances, instance_size, run_command, env, ports):
    image_name, image_tag = util.parse_image_name_tag(image)
    target_state = util.parse_target_state(do_not_start)
    instance_ports = util.parse_instance_ports(ports)
    envvars = util.parse_envvars(env)
    api_endpoint, token = auth.load_token()
    url = api_endpoint + 'apps/'
    headers = auth.build_headers(token)
    payload = {
        "app_name": name,
        "target_num_instances": target_num_instances,
        "image_name": image_name,
        "image_tag": image_tag,
        "instance_size": instance_size,
        "scaling_mode": "MANUAL",
        "target_state": target_state,
        "run_command": run_command,
        "instance_envvars": envvars,
        "instance_ports": instance_ports,
    }
    r = requests.post(url, headers=headers, data=json.dumps(payload))
    print '[service_create]: ' + r.text


def service_update(name, target_num_instances):
    api_endpoint, token = auth.load_token()
    url = api_endpoint + 'apps/' + name
    headers = auth.build_headers(token)
    payload = {
        "app_name": name,
        "target_num_instances": target_num_instances
    }
    r = requests.put(url, headers=headers, data=json.dumps(payload))
    print '[service_update]: ' + r.text


def service_get(name):
    api_endpoint, token = auth.load_token()
    url = api_endpoint + 'apps/' + name
    headers = auth.build_headers(token)
    r = requests.get(url, headers=headers)
    print '[service_get]: ' + json.dumps(json.loads(r.text), indent=2)


def service_start(name):
    api_endpoint, token = auth.load_token()
    url = api_endpoint + 'apps/' + name + '/start/'
    headers = auth.build_headers(token)
    r = requests.put(url, headers=headers)
    print '[service_start]: ' + r.text


def service_stop(name):
    api_endpoint, token = auth.load_token()
    url = api_endpoint + 'apps/' + name + '/stop/'
    headers = auth.build_headers(token)
    r = requests.put(url, headers=headers)
    print '[service_stop]: ' + r.text


def service_delete(name):
    api_endpoint, token = auth.load_token()
    url = api_endpoint + 'apps/' + name
    headers = auth.build_headers(token)
    r = requests.delete(url, headers=headers)
    print '[service_delete]: ' + r.text


def service_list():
    api_endpoint, token = auth.load_token()
    url = api_endpoint + 'apps/'
    headers = auth.build_headers(token)
    r = requests.get(url, headers=headers)
    print '[service_list]: ' + json.dumps(json.loads(r.text), indent=2)
