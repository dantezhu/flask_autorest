# -*- coding: utf-8 -*-

from flask import Flask
from flask_autorest import AutoRest

DEBUG = True
AUTOREST_SOURCES = {
    'test': {
        'uri': 'mysql://root:@localhost/test_stat',
        'auth': ('admin', 'admin'),
        'tables': {
            'user': {
                'per_page': 10,
                'max_per_page': 15,
            },
            'ds': {
            },
        },
    }
}


app = Flask(__name__)
app.config.from_object(__name__)


autorest = AutoRest(app)


if __name__ == '__main__':
    app.run()