import os
from .config import CONFIG

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


def get_config():
    return CONFIG


def get_short_version():
    data = get_config()
    return data['version']


def get_full_version():
    data = get_config()
    return data['version_text'].format(data['version'])
