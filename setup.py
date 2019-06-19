#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
RESTful endpoint for creating/deleting/showing InsightIQ appliances
"""
from setuptools import setup, find_packages


setup(name="vlab-insightiq-api",
      author="Nicholas Willhite,",
      author_email='willnx84@gmail.com',
      version='2019.6.19',
      packages=find_packages(),
      include_package_data=True,
      package_files={'vlab_insightiq_api' : ['app.ini']},
      description="Create, delete, and show InsightIQ appliances in vLab",
      install_requires=['flask', 'ldap3', 'pyjwt', 'uwsgi', 'vlab-api-common',
                        'ujson', 'cryptography', 'vlab-inf-common', 'celery']
      )
