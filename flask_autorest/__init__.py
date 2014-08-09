# -*- coding: utf-8 -*-
"""
AUTOREST_SOURCES:
    {
        'test': {
            'uri': 'mysql://root:@localhost/test_stat',
            'auth': ('dantezhu', 'dantezhu'),
            'tables': ['user'],
            }
        }
    }
AUTOREST_BLUEPRINT_NAME
AUTOREST_URL_PREFIX
"""

__version__ = '0.1.1'

from flask.views import MethodView
from flask import Blueprint, jsonify, abort, request, Response
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
            bp.add_url_rule('/%s/<tb_name>/<pk>' % db_name,
                            view_func=ResourceView.as_view(
                                '%s' % db_name,
                                db_conf=db_conf,
                            )
            )

            bp.add_url_rule('/%s/<tb_name>' % db_name,
                            view_func=ResourceListView.as_view(
                                '%s_list' % db_name,
                                db_conf=db_conf,
                            )
            )

        return bp


class ResourceView(MethodView):
    """
    /resource/<id>
    """
    def __init__(self, db_conf):
        super(ResourceView, self).__init__()
        self.db_conf = db_conf

    def get_tb(self, tb_name):
        if tb_name not in self.db_conf['tables']:
            # 说明不存在
            return None, None

        tb = dataset.connect(self.db_conf['uri'])[tb_name]
        pk_name = tb.table.primary_key.columns.values()[0].name
        return tb, pk_name

    def get(self, tb_name, pk):
        tb, pk_name = self.get_tb(tb_name)
        if tb is None or pk_name is None:
            abort(403)
            return

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

    def patch(self, tb_name, pk):
        json_data = request.get_json(force=True)

        tb, pk_name = self.get_tb(tb_name)
        if tb is None or pk_name is None:
            abort(403)
            return

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

    def delete(self, tb_name, pk):
        tb, pk_name = self.get_tb(tb_name)
        if tb is None or pk_name is None:
            abort(403)
            return

        kwargs = {
            pk_name: pk
        }

        tb.delete(**kwargs)

        return Response(status=204)


class ResourceListView(MethodView):
    """
    /resource/
    """

    def __init__(self, db_conf):
        super(ResourceListView, self).__init__()
        self.db_conf = db_conf

    def get_tb(self, tb_name):
        if tb_name not in self.db_conf['tables']:
            # 说明不存在
            return None, None

        tb = dataset.connect(self.db_conf['uri'])[tb_name]
        pk_name = tb.table.primary_key.columns.values()[0].name
        return tb, pk_name

    def options(self, tb_name):
        tb, pk_name = self.get_tb(tb_name)
        if tb is None or pk_name is None:
            abort(403)
            return

        return jsonify(
            columns=tb.columns
        )

    def get(self, tb_name):
        tb, pk_name = self.get_tb(tb_name)
        if tb is None or pk_name is None:
            abort(403)
            return

        obj_list = tb.find()
        json_obj_list = [obj for obj in obj_list]

        return jsonify(
            objects=json_obj_list
        )

    def post(self, tb_name):
        json_data = request.get_json(force=True)

        tb, pk_name = self.get_tb(tb_name)
        if tb is None or pk_name is None:
            abort(403)
            return

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
