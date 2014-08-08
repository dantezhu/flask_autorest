# -*- coding: utf-8 -*-
"""
AUTOREST_SOURCES:
    {
        'test': {
            'uri': 'mysql://root:@localhost/test_stat',
            'tables': ['user'],
            }
        }
    }
AUTOREST_BLUEPRINT_NAME
AUTOREST_URL_PREFIX
"""

__version__ = '0.1.1'

from flask.views import MethodView
from flask import Blueprint, jsonify, abort, request
import dataset

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
            for tb_name in db_conf['tables']:
                bp.add_url_rule('/%s/%s/<pk>' % (db_name, tb_name),
                                view_func=ResourceView.as_view(
                                    '%s_%s' % (db_name, tb_name),
                                    db_uri=db_uri,
                                    tb_name=tb_name,
                                )
                )

                bp.add_url_rule('/%s/%s' % (db_name, tb_name),
                                view_func=ResourceListView.as_view(
                                    '%s_%s_list' % (db_name, tb_name),
                                    db_uri=db_uri,
                                    tb_name=tb_name,
                                )
                )

        return bp


class ResourceView(MethodView):
    """
    /resource/<id>
    """
    def __init__(self, db_uri, tb_name):
        super(ResourceView, self).__init__()
        self.db_uri = db_uri
        self.tb_name = tb_name

    def get_tb(self):
        tb = dataset.connect(self.db_uri)[self.tb_name]
        pk_name = tb.table.primary_key.columns.values()[0].name
        return tb, pk_name

    def get(self, pk):
        tb, pk_name = self.get_tb()

        kwargs = {
            pk_name: pk
        }

        obj = tb.find_one(**kwargs)
        if not obj:
            abort(404)
            return
        return jsonify(
            **obj
        )

    def patch(self, pk):
        json_data = request.get_json(force=True)
        tb, pk_name = self.get_tb()

        json_data.update({
            pk_name: pk
        })

        tb.update(json_data, [pk_name])

        kwargs = {
            pk_name: pk
        }

        obj = tb.find_one(**kwargs)
        if not obj:
            abort(404)
            return
        return jsonify(
            **obj
        )

    put = patch

    def delete(self, pk):
        tb, pk_name = self.get_tb()
        kwargs = {
            pk_name: pk
        }

        tb.delete(**kwargs)


class ResourceListView(MethodView):
    """
    /resource/
    """

    def __init__(self, db_uri, tb_name):
        super(ResourceListView, self).__init__()
        self.db_uri = db_uri
        self.tb_name = tb_name

    def get_tb(self):
        tb = dataset.connect(self.db_uri)[self.tb_name]
        pk_name = tb.table.primary_key.columns.values()[0].name
        return tb, pk_name

    def options(self):
        tb, pk_name = self.get_tb()

        return jsonify(
            columns=tb.columns
        )

    def get(self):
        tb, pk_name = self.get_tb()

        obj_list = tb.find()
        json_obj_list = [obj for obj in obj_list]
        return jsonify(
            obj_list=json_obj_list
        )

    def post(self):
        json_data = request.get_json(force=True)

        tb, pk_name = self.get_tb()
        pk = tb.insert(json_data)

        kwargs = {
            pk_name: pk
        }

        obj = tb.find_one(**kwargs)
        if not obj:
            abort(404)
            return
        return jsonify(
            **obj
        )
