"""Set of for utilizing Przelewy24 API."""

import collections
import hashlib

import requests


BASE_URL = 'https://secure.przelewy24.pl/'
BASE_SANDBOX_URL = 'https://sandbox.przelewy24.pl/'


Config = collections.namedtuple(
    'Config',
    ['merchant_id', 'pos_id', 'crc', 'sandbox'])


def get_sign(*args):
    return hashlib.md5(('|'.join(str(arg) for arg in args)).encode()).hexdigest()


def get_url(config, path):
    if config.sandbox:
        return BASE_SANDBOX_URL + path
    else:
        return BASE_URL + path


class P24Response:
    def __init__(self, http_response):
        self._http_response = http_response

        content = http_response.content.decode()
        data = {}
        for kv in content.split('&'):
            key, value = kv.split('=')
            data[key] = value

        self.error = data.get('error', None)
        self.error_message = data.get('errorMessage', None)


def test_connection(config):
    url = get_url(config, 'testConnection')
    data = {
        'p24_merchant_id': config.merchant_id,
        'p24_pos_id': config.pos_id,
        'p24_sign': get_sign(config.pos_id, config.crc)
    }
    http_response = requests.post(url, data)
    p24_response = P24Response(http_response)
    return p24_response

