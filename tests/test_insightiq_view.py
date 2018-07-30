# -*- coding: UTF-8 -*-
"""
A suite of tests for the insightiqView object
"""
import unittest
from unittest.mock import patch, MagicMock

import ujson
from flask import Flask
from vlab_api_common import flask_common
from vlab_api_common.http_auth import generate_test_token


from vlab_insightiq_api.lib.views import insightiq


class TestInsightIQView(unittest.TestCase):
    """A set of test cases for the InsightIQView object"""
    @classmethod
    def setUpClass(cls):
        """Runs once for the whole test suite"""
        cls.token = generate_test_token(username='bob')

    @classmethod
    def setUp(cls):
        """Runs before every test case"""
        app = Flask(__name__)
        insightiq.InsightIQView.register(app)
        app.config['TESTING'] = True
        cls.app = app.test_client()
        # Mock Celery
        app.celery_app = MagicMock()
        cls.fake_task = MagicMock()
        cls.fake_task.id = 'asdf-asdf-asdf'
        app.celery_app.send_task.return_value = cls.fake_task

    def test_get_task(self):
        """InsightIQView - GET on /api/1/inf/insightiq returns a task-id"""
        resp = self.app.get('/api/1/inf/insightiq',
                            headers={'X-Auth': self.token})

        task_id = resp.json['content']['task-id']
        expected = 'asdf-asdf-asdf'

        self.assertEqual(task_id, expected)

    def test_post_task(self):
        """InsightIQView - POST on /api/1/inf/insightiq returns a task-id"""
        resp = self.app.post('/api/1/inf/insightiq',
                             headers={'X-Auth': self.token},
                             json={'name': "myIIQ", 'image': "4.1.2", 'network': "someNetwork"})

        task_id = resp.json['content']['task-id']
        expected = 'asdf-asdf-asdf'

        self.assertEqual(task_id, expected)

    def test_delete_task(self):
        """InsightIQView - DELETE on /api/1/inf/insightiq returns a task-id"""
        resp = self.app.delete('/api/1/inf/insightiq',
                               headers={'X-Auth': self.token},
                               json={'name': "myIIQ"})

        task_id = resp.json['content']['task-id']
        expected = 'asdf-asdf-asdf'

        self.assertEqual(task_id, expected)

    def test_get_image_task(self):
        """InsightIQView - GET on /api/1/inf/insightiq/image returns a task-id"""
        resp = self.app.get('/api/1/inf/insightiq/image',
                            headers={'X-Auth': self.token})

        task_id = resp.json['content']['task-id']
        expected = 'asdf-asdf-asdf'

        self.assertEqual(task_id, expected)


if __name__ == '__main__':
    unittest.main()
