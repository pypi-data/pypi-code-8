import requests
import sys

cred_template = """
{
  "domainCredentials": {
    "domain": {
      "name": "",
      "description": ""
    },
    "credentials": [
      {
        "scope": "GLOBAL",
        "id": "",
        "username": "{USERNAME}",
        "description": "{DESCRIPTION}",
        "privateKeySource": {
          "value": "1",
          "privateKeyFile": "{KEY_FILE}",
          "stapler-class": "com.cloudbees.jenkins.plugins\
.sshcredentials.impl.BasicSSHUserPrivateKey$FileOnMasterPrivateKeySource"
        },
        "passphrase": "",
        "stapler-class": "com.cloudbees.jenkins.plugins\
.sshcredentials.impl.BasicSSHUserPrivateKey",
        "kind": "com.cloudbees.jenkins.plugins\
.sshcredentials.impl.BasicSSHUserPrivateKey"
      }
    ]
  }
}
"""


def init(url):
    cred = (cred_template.
            replace('{KEY_FILE}', '/var/jenkins_home/.ssh/id_rsa').
            replace('{USERNAME}', 'ubuntu').
            replace('{DESCRIPTION}', 'for jenkins slaves'))
    r = requests.post(url + '/credentials/configSubmit',
                      data={'description': 'GLOBAL DESCRIPTION',
                            'name': 'GLOBAL NAME',
                            'json': cred})
    r.raise_for_status()

init(*sys.argv[1:])
