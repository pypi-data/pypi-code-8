import BaseHTTPServer
import json
import logging
import requests


from utils import get_images
log = logging.getLogger(__name__)


class handler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_POST(self):
        content_len = int(self.headers.getheader('content-length', 0))
        data = json.loads(self.rfile.read(content_len))

        name = data['repository']['repo_name']
        log.info('Image updated on docker hub: {name}'
                 .format(name=name))

        response = {'state': 'success'}
        if 'callback_url' in data:
            requests.post(data['callback_url'],
                          data=json.dumps(response),
                          headers={'Content-Type': 'application/json'})
            log.debug('Sent reply to callback_url.')

        for image in get_images(self.compose_project):
            if image.options['image'] == name:
                image.pull()
                log.info('...image updated locally.')
                break

        else:
            log.info('No such image: {name}'.format(name=name))
            self.send_response(422)
            self.end_headers()
            return


def listen(project, options):
    address = (options['HOST'] or 'localhost', options['PORT'] or 8000)
    httpd = BaseHTTPServer.HTTPServer(address, handler)
    handler.compose_project = project
    log.info('Server listening at: {0}:{1}. CTRL-C to exit.'.format(*address))
    httpd.serve_forever()
