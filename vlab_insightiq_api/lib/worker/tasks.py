# -*- coding: UTF-8 -*-
"""
Entry point logic for available backend worker tasks
"""
from celery import Celery
from celery.utils.log import get_task_logger

from vlab_insightiq_api.lib import const
from vlab_insightiq_api.lib.worker import vmware

app = Celery('insightiq', backend='rpc://', broker=const.VLAB_MESSAGE_BROKER)
logger = get_task_logger(__name__)
logger.setLevel(const.VLAB_INSIGHTIQ_LOG_LEVEL.upper())


@app.task(name='insightiq.show')
def show(username):
    """Obtain basic information about the InsightIQ instances a user owns.

    :Returns: Dictionary

    :param username: The name of the user who wants info about their default gateway
    :type username: String
    """
    resp = {'content' : {}, 'error': None, 'params': {}}
    logger.info('Task starting')
    try:
        info = vmware.show_insightiq(username)
    except ValueError as doh:
        logger.error('Task failed: {}'.format(doh))
        resp['error'] = '{}'.format(doh)
    else:
        logger.info('Task complete')
        resp['content'] = info
    return resp


@app.task(name='insightiq.create')
def create(username, machine_name, image, network):
    """Deploy a new shinny instance of InsightIQ

    :Returns: Dictionary

    :param username: The name of the user who wants to create a new default gateway
    :type username: String
    """
    resp = {'content' : {}, 'error': None, 'params': {}}
    logger.info('Task starting')
    try:
        resp['content'] = vmware.create_insightiq(username, machine_name, image, network)
    except ValueError as doh:
        logger.error('Task failed: {}'.format(doh))
        resp['error'] = '{}'.format(doh)
    logger.info('Task complete')
    return resp


@app.task(name='insightiq.delete')
def delete(username, machine_name):
    """Destroy an instance of InsightIQ

    :Returns: Dictionary

    :param username: The name of the user who wants to create a new default gateway
    :type username: String

    :param machine_name: The name of the instance of insightiq
    :type machine_name: String
    """
    resp = {'content' : {}, 'error': None, 'params': {}}
    logger.info('Task starting')
    try:
        vmware.delete_insightiq(username, machine_name)
    except ValueError as doh:
        logger.error('Task failed: {}'.format(doh))
        resp['error'] = '{}'.format(doh)
    else:
        logger.info('Task complete')
    return resp


@app.task(name='insightiq.image')
def image():
    """Deplay the available versions/images of InsightIQ that a user can deploy/create.

    :Returns: Dictionary

    :param username: The name of the user who wants to create a new default gateway
    :type username: String
    """
    resp = {'content' : {}, 'error': None, 'params': {}}
    logger.info('Task starting')
    resp['content'] = {'image': vmware.list_images()}
    logger.info('Task complete')
    return resp
