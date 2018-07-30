# -*- coding: UTF-8 -*-
"""
A suite of tests for the HTTP API schemas
"""
import unittest

from jsonschema import Draft4Validator, validate, ValidationError
from vlab_insightiq_api.lib.views import insightiq


class TestInsightIQViewSchema(unittest.TestCase):
    """A set of test cases for the schemas of /api/1/inf/insightiq"""

    def test_post_schema(self):
        """The schema defined for POST is valid"""
        try:
            Draft4Validator.check_schema(insightiq.InsightIQView.POST_SCHEMA)
            schema_valid = True
        except RuntimeError:
            schema_valid = False

        self.assertTrue(schema_valid)

    def test_delete_schema(self):
        """The schema defined for DELETE is valid"""
        try:
            Draft4Validator.check_schema(insightiq.InsightIQView.DELETE_SCHEMA)
            schema_valid = True
        except RuntimeError:
            schema_valid = False

        self.assertTrue(schema_valid)

    def test_get_schema(self):
        """The schema defined for GET is valid"""
        try:
            Draft4Validator.check_schema(insightiq.InsightIQView.GET_SCHEMA)
            schema_valid = True
        except RuntimeError:
            schema_valid = False

        self.assertTrue(schema_valid)

    def test_images_schema(self):
        """The schema defined for GET on /images is valid"""
        try:
            Draft4Validator.check_schema(insightiq.InsightIQView.IMAGES_SCHEMA)
            schema_valid = True
        except RuntimeError:
            schema_valid = False

        self.assertTrue(schema_valid)

    def test_delete(self):
        """The DELETE schema happy path test"""
        body = {'name': "myIIQ"}
        try:
            validate(body, insightiq.InsightIQView.DELETE_SCHEMA)
            ok = True
        except ValidationError:
            ok = False

        self.assertTrue(ok)

    def test_delete_required(self):
        """The DELETE schema requires the parameter 'name'"""
        body = {}
        try:
            validate(body, insightiq.InsightIQView.DELETE_SCHEMA)
            ok = False
        except ValidationError:
            ok = True

        self.assertTrue(ok)

    def test_post(self):
        """The POST schema happy path test"""
        body = {'name': "myIIQ", 'network': "someNetwork", 'image': "4.1.2"}
        try:
            validate(body, insightiq.InsightIQView.POST_SCHEMA)
            ok = True
        except ValidationError:
            ok = False

        self.assertTrue(ok)

    def test_post_name_required(self):
        """The POST schema requires the 'name' parameter"""
        body = { 'network': "someNetwork", 'image': "4.1.2"}
        try:
            validate(body, insightiq.InsightIQView.POST_SCHEMA)
            ok = False
        except ValidationError:
            ok = True

        self.assertTrue(ok)

    def test_post_network_required(self):
        """The POST schema requires the 'network' parameter"""
        body = { 'name': "myIIQ", 'image': "4.1.2"}
        try:
            validate(body, insightiq.InsightIQView.POST_SCHEMA)
            ok = False
        except ValidationError:
            ok = True

        self.assertTrue(ok)

    def test_post_image_required(self):
        """The POST schema requires the 'image' parameter"""
        body = { 'name': "myIIQ", 'network': "someNetwork"}
        try:
            validate(body, insightiq.InsightIQView.POST_SCHEMA)
            ok = False
        except ValidationError:
            ok = True

        self.assertTrue(ok)


if __name__ == '__main__':
    unittest.main()
