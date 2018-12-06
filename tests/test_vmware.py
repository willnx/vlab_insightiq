# -*- coding: UTF-8 -*-
"""
A suite of tests for the functions in vmware.py
"""
import unittest
from unittest.mock import patch, MagicMock

from vlab_insightiq_api.lib.worker import vmware


class TestVMware(unittest.TestCase):
    """A set of test cases for the vmware.py module"""
    @classmethod
    def setUpClass(cls):
        vmware.logger = MagicMock()

    @patch.object(vmware.virtual_machine, 'get_info')
    @patch.object(vmware, 'vCenter')
    def test_show_insightiq(self, fake_vCenter, fake_get_info):
        """``show_insightiq`` returns a dictionary when everything works as expected"""
        fake_vm = MagicMock()
        fake_vm.name = 'myIIQ'
        fake_folder = MagicMock()
        fake_folder.childEntity = [fake_vm]
        fake_vCenter.return_value.__enter__.return_value.get_by_name.return_value = fake_folder
        fake_get_info.return_value = {'worked': True, 'note': "InsightIQ=4.1.2"}

        output = vmware.show_insightiq(username='alice')
        expected = {'myIIQ': {'worked': True, 'note': "InsightIQ=4.1.2"}}

        self.assertEqual(output, expected)

    @patch.object(vmware.virtual_machine, 'get_info')
    @patch.object(vmware, 'vCenter')
    def test_show_insightiq_nothing(self, fake_vCenter, fake_get_info):
        """``show_insightiq`` returns an empty dictionary no insightiq is found"""
        fake_vm = MagicMock()
        fake_vm.name = 'myIIQ'
        fake_folder = MagicMock()
        fake_folder.childEntity = [fake_vm]
        fake_vCenter.return_value.__enter__.return_value.get_by_name.return_value = fake_folder
        fake_get_info.return_value = {'worked': True, 'note': "noIIQ=4.1.2"}

        output = vmware.show_insightiq(username='alice')
        expected = {}

        self.assertEqual(output, expected)

    @patch.object(vmware, 'consume_task')
    @patch.object(vmware, 'Ova')
    @patch.object(vmware.virtual_machine, 'get_info')
    @patch.object(vmware.virtual_machine, 'deploy_from_ova')
    @patch.object(vmware, 'vCenter')
    def test_create_insightiq(self, fake_vCenter, fake_deploy_from_ova, fake_get_info, fake_Ova, fake_consume_task):
        """``create_insightiq`` returns the new insightiq's info when everything works"""
        fake_logger = MagicMock()
        fake_Ova.return_value.networks = ['vLabNetwork']
        fake_get_info.return_value = {'worked' : True}
        fake_vCenter.return_value.__enter__.return_value.networks = {'someNetwork': vmware.vim.Network(moId='asdf')}

        output = vmware.create_insightiq(username='alice',
                                         machine_name='myIIQ',
                                         image='4.1.2',
                                         network='someNetwork',
                                         logger=fake_logger)
        expected = {'worked': True}

        self.assertEqual(output, expected)

    @patch.object(vmware, 'consume_task')
    @patch.object(vmware, 'Ova')
    @patch.object(vmware.virtual_machine, 'get_info')
    @patch.object(vmware.virtual_machine, 'deploy_from_ova')
    @patch.object(vmware, 'vCenter')
    def test_create_insightiq_value_error(self, fake_vCenter, fake_deploy_from_ova, fake_get_info, fake_Ova, fake_consume_task):
        """``create_insightiq`` raises ValueError if supplied with a non-existing network"""
        fake_logger = MagicMock()
        fake_Ova.return_value.networks = ['vLabNetwork']
        fake_get_info.return_value = {'worked' : True}
        fake_vCenter.return_value.__enter__.return_value.networks = {'someNetwork': vmware.vim.Network(moId='asdf')}

        with self.assertRaises(ValueError):
            vmware.create_insightiq(username='alice',
                                    machine_name='myIIQ',
                                    image='4.1.2',
                                    network='not a thing',
                                    logger=fake_logger)

    @patch.object(vmware.virtual_machine, 'get_info')
    @patch.object(vmware, 'consume_task')
    @patch.object(vmware.virtual_machine, 'power')
    @patch.object(vmware, 'vCenter')
    def test_delete_insightiq(self, fake_vCenter, fake_power, fake_consume_task, fake_get_info):
        """``delete_insightiq`` powers off the VM then deletes it"""
        fake_logger = MagicMock()
        fake_vm = MagicMock()
        fake_vm.name = 'myIIQ'
        fake_folder = MagicMock()
        fake_folder.childEntity = [fake_vm]
        fake_vCenter.return_value.__enter__.return_value.get_by_name.return_value = fake_folder
        fake_get_info.return_value = {'worked': True, 'note': "InsightIQ=4.1.2"}
        vmware.delete_insightiq(username='alice', machine_name='myIIQ', logger=fake_logger)

        self.assertTrue(fake_power.called)
        self.assertTrue(fake_vm.Destroy_Task.called)

    @patch.object(vmware.virtual_machine, 'get_info')
    @patch.object(vmware, 'consume_task')
    @patch.object(vmware.virtual_machine, 'power')
    @patch.object(vmware, 'vCenter')
    def test_delete_insightiq_value_error(self, fake_vCenter, fake_power, fake_consume_task, fake_get_info):
        """``delete_insightiq`` raises ValueError if no InsightiQ machine has the supplied name"""
        fake_logger = MagicMock()
        fake_vm = MagicMock()
        fake_vm.name = 'myIIQ'
        fake_folder = MagicMock()
        fake_folder.childEntity = [fake_vm]
        fake_vCenter.return_value.__enter__.return_value.get_by_name.return_value = fake_folder
        fake_get_info.return_value = {'worked': True, 'note': "InsightIQ=4.1.2"}

        with self.assertRaises(ValueError):
            vmware.delete_insightiq(username='alice', machine_name='not a thing', logger=fake_logger)

    @patch.object(vmware.os, 'listdir')
    def test_list_images(self, fake_listdir):
        """``list_images`` returns a list of images when everything works as expected"""
        fake_listdir.return_value = ['InsightIQ_4.1.2.ova']

        output = vmware.list_images()
        expected = ['4.1.2']

        self.assertEqual(output, expected)

    def test_convert_name(self):
        """``convert_name`` defaults to converting versions to images"""
        output = vmware.convert_name('4.1.2')
        expected = 'InsightIQ_4.1.2.ova'

        self.assertEqual(output, expected)

    def test_convert_name_to_version(self):
        """``convert_name`` can convert from versions to image names"""
        output = vmware.convert_name('InsightIQ_4.1.2.ova', to_version=True)
        expected = '4.1.2'

        self.assertEqual(output, expected)


if __name__ == '__main__':
    unittest.main()
