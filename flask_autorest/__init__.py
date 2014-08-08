# -*- coding: utf-8 -*-
"""
AUTOREST_SOURCES:
    {
        'test': {
            'uri': 'mysql://root:@localhost/flask_dpl',
            'tables': {
                'user': {
                    'pk': 'id',
                }
            }
        }
    }
AUTOREST_BLUEPRINT_NAME
AUTOREST_URL_PREFIX
"""

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
        bp = self.create_blueprint(app)

        app.register_blueprint(bp)

    def create_blueprint(self, app):
        """
        生成一个blueprint
        """
        blueprint_name = app.config.get('AUTOREST_BLUEPRINT_NAME') or AUTOREST_BLUEPRINT_NAME
        url_prefix = app.config.get('AUTOREST_URL_PREFIX') or AUTOREST_URL_PREFIX
        sources = app.config.get('AUTOREST_SOURCES')

        bp = Blueprint(blueprint_name, __name__, url_prefix=url_prefix)

        for db_name, db_conf in sources.items():
            db_uri = db_conf['uri']
            for tb_name, tb_conf in db_conf['tables'].items():
                pk_name = tb_conf.get('pk') or 'id'

                bp.add_url_rule('/%s/%s/<pk>' % (db_name, tb_name),
                                view_func=ResourceView.as_view(
                                    '%s_%s' % (db_name, tb_name),
                                    db_uri=db_uri,
                                    pk_name=pk_name
                                )
                )

                bp.add_url_rule('/%s/%s' % (db_name, tb_name),
                                view_func=ResourceListView.as_view('%s_%s_list' % (db_name, tb_name), db_uri=db_uri))

        return bp


class ResourceView(MethodView):
    """
    /resource/<id>
    """
    def __init__(self, db_uri, pk_name):
        self.db_uri = db_uri
        self.pk_name = pk_name

        super(ResourceView, self).__init__()

    def get(self, pk):
        return str(pk)


class ResourceListView(MethodView):
    """
    /resource/
    """

    def __init__(self, db_uri):
        self.db_uri = db_uri

    def get(self):
        return 'list'