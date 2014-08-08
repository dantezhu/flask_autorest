# -*- coding: utf-8 -*-

__version__ = '0.1.1'

from flask.views import MethodView
from flask import Blueprint

AUTOREST_BLUEPRINT_NAME = 'autorest'
AUTOREST_URL_PREFIX = '/autorest'


class AutoRest(object):

    def __init__(self, app=None):
        """init with app

        :app: Flask instance

        """
        if app:
            self.init_app(app)

    def init_app(self, app):
        """
        安装到app上
        """

    def create_blueprint(self, app, sources):
        """
        生成一个blueprint
        """
        blueprint_name = app.config.get('AUTOREST_BLUEPRINT_NAME') or AUTOREST_BLUEPRINT_NAME
        url_prefix = app.config.get('AUTOREST_URL_PREFIX') or AUTOREST_URL_PREFIX
        sources = app.config.get('AUTOREST_SOURCES')

        bp = Blueprint(blueprint_name, __name__, url_prefix=url_prefix)


class ResourceView(MethodView):
    """
    /resource/<id>
    """
    pass


class ResourceListView(MethodView):
    """
    /resource/
    """