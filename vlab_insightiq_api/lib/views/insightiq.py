# -*- coding: UTF-8 -*-
"""
TODO
"""
import ujson
from flask import current_app
from flask_classy import request, route
from vlab_inf_common.views import TaskView
from vlab_inf_common.vmware import vCenter, vim
from vlab_api_common import describe, get_logger, requires, validate_input


from vlab_insightiq_api.lib import const


logger = get_logger(__name__, loglevel=const.VLAB_INSIGHTIQ_LOG_LEVEL)


class InsightIQView(TaskView):
    """API end point for InsightIQ instances"""
    route_base = '/api/1/inf/insightiq'
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


    @requires(verify=False)
    @describe(post=POST_SCHEMA, delete=DELETE_SCHEMA, get=GET_SCHEMA)
    def get(self, *args, **kwargs):
        """Display the insightiq instances you own"""
        username = kwargs['token']['username']
        resp = {'user' : username}
        task = current_app.celery_app.send_task('insightiq.show', [username])
        resp['content'] = {'task-id': task.id}
        return ujson.dumps(resp), 200

    @requires(verify=False) # XXX remove verify=False before commit
    @validate_input(schema=POST_SCHEMA)
    def post(self, *args, **kwargs):
        """Create a insightiq"""
        username = kwargs['token']['username']
        resp = {'user' : username}
        body = kwargs['body']
        network = kwargs['body']['network']
        machine_name = kwargs['body']['name']
        image = kwargs['body']['image']
        task = current_app.celery_app.send_task('insightiq.create', [username, machine_name, image, network])
        resp['content'] = {'task-id': task.id}
        return ujson.dumps(resp), 200

    @requires(verify=False) # XXX remove verify=False before commit
    @validate_input(schema=DELETE_SCHEMA)
    def delete(self, *args, **kwargs):
        """Destroy a insightiq"""
        username = kwargs['token']['username']
        resp = {'user' : username}
        machine_name = kwargs['body']['name']
        task = current_app.celery_app.send_task('insightiq.delete', [username, machine_name])
        resp['content'] = {'task-id': task.id}
        return ujson.dumps(resp), 200

    @route('/image', methods=["GET"])
    @requires(verify=False)
    @describe(get=IMAGES_SCHEMA)
    def image(self, *args, **kwargs):
        """Show available versions of insightiq that can be deployed"""
        username = kwargs['token']['username']
        resp = {'user' : username}
        task = current_app.celery_app.send_task('insightiq.image')
        resp['content'] = {'task-id': task.id}
        return ujson.dumps(resp), 200
