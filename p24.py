"""
Set of tools for utilizing Przelewy24 API.

Version: 0.2
Author: Piotr Wasilewski <piotrek@piotrek.io>


The MIT License (MIT)

Copyright (c) 2016 Piotr Wasilewski

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import collections
import hashlib

import requests


VERSION = (0, 2)


API_VERSION = '3.2'

BASE_URL = 'https://secure.przelewy24.pl/'
BASE_SANDBOX_URL = 'https://sandbox.przelewy24.pl/'

CURRENCY_PLN = 'PLN'
CURRENCY_EUR = 'EUR'
CURRENCY_GBP = 'GBP'
CURRENCY_CZK = 'CZK'

COUNTRY_AD = 'AD'
COUNTRY_AT = 'AT'
COUNTRY_BE = 'BE'
COUNTRY_CY = 'CY'
COUNTRY_CZ = 'CZ'
COUNTRY_DK = 'DK'
COUNTRY_EE = 'EE'
COUNTRY_FI = 'FI'
COUNTRY_FR = 'FR'
COUNTRY_EL = 'EL'
COUNTRY_ES = 'ES'
COUNTRY_NL = 'NL'
COUNTRY_IE = 'IE'
COUNTRY_IS = 'IS'
COUNTRY_LT = 'LT'
COUNTRY_LV = 'LV'
COUNTRY_LU = 'LU'
COUNTRY_MT = 'MT'
COUNTRY_NO = 'NO'
COUNTRY_PL = 'PL'
COUNTRY_PT = 'PT'
COUNTRY_SM = 'SM'
COUNTRY_SK = 'SK'
COUNTRY_SI = 'SI'
COUNTRY_CH = 'CH'
COUNTRY_SE = 'SE'
COUNTRY_HU = 'HU'
COUNTRY_GB = 'GB'
COUNTRY_IT = 'IT'
COUNTRY_US = 'US'
COUNTRY_CA = 'CA'
COUNTRY_JP = 'JP'
COUNTRY_UA = 'UA'
COUNTRY_BY = 'BY'
COUNTRY_RU = 'RU'

LANGUAGE_PL = 'pl'
LANGUAGE_EN = 'en'
LANGUAGE_DE = 'de'
LANGUAGE_ES = 'es'
LANGUAGE_IT = 'it'

WAIT_FOR_RESULT_NO = 0
WAIT_FOR_RESULT_YES = 1

CHANNEL_CARD = 1
CHANNEL_TRANSFER = 2
CHANNEL_TRADITIONAL_TRANSFER = 4
CHANNEL_NA = 8
CHANNEL_ALL_247 = 16
CHANNEL_PREPAID = 32

ENCODING_ISO = 'ISO-8859-2'
ENCODING_UTF = 'UTF-8'
ENCODING_WIN = 'Windows-1250'


Config = collections.namedtuple(
    'Config',
    ['merchant_id', 'pos_id', 'crc', 'sandbox'])

Transaction = collections.namedtuple(
    'Transaction',
    ['session_id', 'amount', 'currency', 'description', 'email', 'client',
     'address', 'zip', 'city', 'country', 'phone', 'language', 'method',
     'url_return', 'url_status', 'time_limit', 'wait_for_result', 'channel',
     'shipping', 'transfer_label', 'encoding']
)


def get_sign(*args):
    return hashlib.md5(('|'.join(str(arg) for arg in args)).encode()).hexdigest()


def get_amount(amount):
    return int(amount * 100)


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
        self.token = data.get('token', None)


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


def transaction_register(config, transaction):
    url = get_url(config, 'trnRegister')
    data = {
        'p24_merchant_id': config.merchant_id,
        'p24_pos_id': config.pos_id,
        'p24_session_id': transaction.session_id,
        'p24_amount': get_amount(transaction.amount),
        'p24_currency': transaction.currency,
        'p24_description': transaction.description,
        'p24_email': transaction.email,
        'p24_country': transaction.country,
        'p24_url_return': transaction.url_return,
        'p24_api_version': API_VERSION,
        'p24_sign': get_sign(
            transaction.session_id,
            config.merchant_id,
            get_amount(transaction.amount),
            transaction.currency,
            config.crc),
        'p24_encoding': transaction.encoding,
    }
    if transaction.client is not None:
        data['p24_client'] = transaction.client
    if transaction.address is not None:
        data['p24_address'] = transaction.address
    if transaction.zip is not None:
        data['p24_zip'] = transaction.zip
    if transaction.city is not None:
        data['p24_city'] = transaction.city
    if transaction.phone is not None:
        data['p24_phone'] = transaction.phone
    if transaction.language is not None:
        data['p24_language'] = transaction.language
    if transaction.method is not None:
        data['p24_method'] = transaction.method
    if transaction.url_status is not None:
        data['p24_url_status'] = transaction.url_status
    if transaction.time_limit is not None:
        data['p24_time_limit'] = transaction.time_limit
    if transaction.wait_for_result is not None:
        data['p24_wait_for_result'] = transaction.wait_for_result
    if transaction.channel is not None:
        data['p24_channel'] = transaction.channel
    if transaction.shipping is not None:
        data['p24_shipping'] = transaction.shipping
    if transaction.transfer_label is not None:
        data['p24_transfer_label'] = transaction.transfer_label
    if transaction.encoding is not None:
        data['p24_encoding'] = transaction.encoding
    http_response = requests.post(url, data)
    p24_response = P24Response(http_response)
    return p24_response


def transaction_verify(config, transaction, order_id):
    url = get_url(config, 'trnVerify')
    data = {
        'p24_merchant_id': config.merchant_id,
        'p24_pos_id': config.pos_id,
        'p24_session_id': transaction.session_id,
        'p24_amount': transaction.amount,
        'p24_currency': transaction.currency,
        'p24_order_id': order_id,
        'p24_sign': get_sign(
            transaction.session_id,
            config.merchant_id,
            transaction.amount,
            transaction.currency,
            config.crc),
    }
    http_response = requests.post(url, data)
    p24_response = P24Response(http_response)
    return p24_response
