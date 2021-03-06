# -*- coding: UTF-8 -*-
"""
Defines the RESTful API for the InsightIQ deployment service
"""
import ujson
from flask import current_app
from flask_classy import request, route, Response
from vlab_inf_common.views import MachineView
from vlab_inf_common.vmware import vCenter, vim
from vlab_api_common import describe, get_logger, requires, validate_input


from vlab_insightiq_api.lib import const


logger = get_logger(__name__, loglevel=const.VLAB_INSIGHTIQ_LOG_LEVEL)


class InsightIQView(MachineView):
    """API end point for InsightIQ instances"""
    route_base = '/api/2/inf/insightiq'
    RESOURCE = 'insightiq'
    POST_SCHEMA = { "$schema": "http://json-schema.org/draft-04/schema#",
                    "type": "object",
                    "description": "Create an InsightIQ instance",
                    "properties": {
                        "network": {
                            "description": "The public network to connect InsightIQ to",
                            "type": "string"
                        },
                        "name": {
                            "description": "The name to give the new InsightIQ instance",
                            "type": "string"
                        },
                        "image": {
                            "description": "The image/version of InsightIQ to create",
                            "type": "string"
                        }
                    },
                    "required": ["network", "name", "image"]
                  }
    DELETE_SCHEMA = {"$schema": "http://json-schema.org/draft-04/schema#",
                     "description": "Destroy an InsightIQ instance",
                     "properties": {
                        "name": {
                            "description": "The name of the InsightIQ instance to destroy",
                            "type": "string"
                        },
                     },
                     "required": ["name"]
                    }
    GET_SCHEMA = {"$schema": "http://json-schema.org/draft-04/schema#",
                  "description": "Display the InsightIQ instances you own"
                 }
    IMAGES_SCHEMA = {"$schema": "http://json-schema.org/draft-04/schema#",
                     "description": "View available versions ofinsightiq that can be created"
                    }


    @requires(verify=const.VLAB_VERIFY_TOKEN, version=2)
    @describe(post=POST_SCHEMA, delete=DELETE_SCHEMA, get=GET_SCHEMA)
    def get(self, *args, **kwargs):
        """Display the insightiq instances you own"""
        username = kwargs['token']['username']
        txn_id = request.headers.get('X-REQUEST-ID', 'noId')
        resp_data = {'user' : username}
        task = current_app.celery_app.send_task('insightiq.show', [username, txn_id])
        resp_data['content'] = {'task-id': task.id}
        resp = Response(ujson.dumps(resp_data))
        resp.status_code = 202
        resp.headers.add('Link', '<{0}{1}/task/{2}>; rel=status'.format(const.VLAB_URL, self.route_base, task.id))
        return resp

    @requires(verify=const.VLAB_VERIFY_TOKEN, version=2)
    @validate_input(schema=POST_SCHEMA)
    def post(self, *args, **kwargs):
        """Create a insightiq"""
        username = kwargs['token']['username']
        txn_id = request.headers.get('X-REQUEST-ID', 'noId')
        resp_data = {'user' : username}
        body = kwargs['body']
        network = '{}_{}'.format(username, kwargs['body']['network'])
        machine_name = kwargs['body']['name']
        image = kwargs['body']['image']
        task = current_app.celery_app.send_task('insightiq.create', [username, machine_name, image, network, txn_id])
        resp_data['content'] = {'task-id': task.id}
        resp = Response(ujson.dumps(resp_data))
        resp.status_code = 202
        resp.headers.add('Link', '<{0}{1}/task/{2}>; rel=status'.format(const.VLAB_URL, self.route_base, task.id))
        return resp

    @requires(verify=const.VLAB_VERIFY_TOKEN, version=2)
    @validate_input(schema=DELETE_SCHEMA)
    def delete(self, *args, **kwargs):
        """Destroy a insightiq"""
        username = kwargs['token']['username']
        txn_id = request.headers.get('X-REQUEST-ID', 'noId')
        resp_data = {'user' : username}
        machine_name = kwargs['body']['name']
        task = current_app.celery_app.send_task('insightiq.delete', [username, machine_name, txn_id])
        resp_data['content'] = {'task-id': task.id}
        resp = Response(ujson.dumps(resp_data))
        resp.status_code = 202
        resp.headers.add('Link', '<{0}{1}/task/{2}>; rel=status'.format(const.VLAB_URL, self.route_base, task.id))
        return resp

    @route('/image', methods=["GET"])
    @requires(verify=const.VLAB_VERIFY_TOKEN, version=2)
    @describe(get=IMAGES_SCHEMA)
    def image(self, *args, **kwargs):
        """Show available versions of insightiq that can be deployed"""
        username = kwargs['token']['username']
        txn_id = request.headers.get('X-REQUEST-ID', 'noId')
        resp_data = {'user' : username}
        task = current_app.celery_app.send_task('insightiq.image', [txn_id])
        resp_data['content'] = {'task-id': task.id}
        resp = Response(ujson.dumps(resp_data))
        resp.status_code = 202
        resp.headers.add('Link', '<{0}{1}/task/{2}>; rel=status'.format(const.VLAB_URL, self.route_base, task.id))
        return resp
