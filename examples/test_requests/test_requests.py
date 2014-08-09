# -*- coding: utf-8 -*-

import json
import requests
from urlparse import urljoin

BASE_URL = 'http://127.0.0.1:5000/'
AUTH = ('admin', 'admin')

URL_PREFIX = '/autorest/test/ds'


def test_options_user_list():
    rsp = requests.options(urljoin(BASE_URL, URL_PREFIX), auth=AUTH)
    assert rsp.ok, rsp.status_code
    print rsp.json()


def test_get_user_list():
    rsp = requests.get(urljoin(BASE_URL, URL_PREFIX), params=dict(page=1, per_page=10), auth=AUTH)
    assert rsp.ok, rsp.status_code
    print rsp.json()


def test_post_user_list():
    json_data = dict(
        password='ppp',
        name='init',
        create_time='2014-03-3T03:3:3'
    )
    rsp = requests.post(urljoin(BASE_URL, URL_PREFIX), auth=AUTH, data=json.dumps(json_data))
    assert rsp.ok, rsp.status_code
    print rsp.json()


def test_get_user():
    rsp = requests.get(urljoin(BASE_URL, '%s/27' % URL_PREFIX), auth=AUTH)
    assert rsp.ok, rsp.status_code
    print rsp.json()


def test_put_user():
    json_data = dict(
        password='put',
        nick='xx',
        create_time='2014-03-3T03:3:3'
    )
    # 注意最后的 /
    rsp = requests.put(urljoin(BASE_URL, '%s/27' % URL_PREFIX), auth=AUTH, data=json.dumps(json_data))
    assert rsp.ok, rsp.status_code
    print rsp.json()


def test_patch_user():
    json_data = dict(
        password=300,
        )
    rsp = requests.patch(urljoin(BASE_URL, '%s/27' % URL_PREFIX), auth=AUTH, data=json.dumps(json_data))
    assert rsp.ok, rsp.status_code
    print rsp.json()
