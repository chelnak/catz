import os
import json

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

CONFIG = '{0}./config.json'.format(__location__)


def get_config():
    with open(CONFIG, 'r') as file:
        return json.loads(file.read())


def get_short_version():
    data = get_config()
    return data['version']


def get_full_version():
    data = get_config()
    return data['version_text'].format(data['version'])


def set_version(version):
    config = get_config()
    with open(CONFIG, 'w') as file:
        config['version'] = version
        file.write(json.dumps(config, indent=4))
