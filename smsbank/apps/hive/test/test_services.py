from django.test import TestCase

from smsbank.apps.hive.models import (
    Device,
    Sms
)
from smsbank.apps.hive.services import (
    device_exists,
    get_or_create_device,
    get_device_by_id,
    new_sms,
    sms_list
)


class DeviceTestCase(TestCase):
    def setUp(self):
        self.device = Device.objects.create(ip='127.0.0.1', port=1234)

    def test_can_check_if_device_exists(self):
        """Check if can check device status"""
        self.assertTrue(device_exists('127.0.0.1', 1234))
        self.assertEqual(device_exists('127.0.0.1', 1234), self.device)
        self.assertFalse(device_exists('0.0.0.0', 4321))
        self.assertNotEqual(device_exists('0.0.0.0', 4321), self.device)

    def test_can_get_or_create_device(self):
        """Check if can get existing or create new device"""
        self.assertTrue(get_or_create_device('127.0.0.1', 1234))
        device = get_or_create_device('0.0.0.0', 4321)
        self.assertIsInstance(device, Device)
        self.assertEqual(device, Device.objects.get(ip='0.0.0.0', port=4321))

    def test_can_get_device_by_id(self):
        """Check if can get previously saved device by its id"""
        self.assertEqual(self.device, get_device_by_id(self.device.id))


class SmsTestCase(TestCase):
    def setUp(self):
        self.device = Device.objects.create(ip='127.0.0.1', port=1234)
        self.anotherDevice = Device.objects.create(ip='0.0.0.1', port=1111)
        self.sms = Sms.objects.create(
            recipient='test',
            message='hello',
            device=self.device
        )

    def test_can_create_new_sms(self):
        """Check if can create new SMS and associate it with device"""
        sms = new_sms('who goes here?', 'hi there!', self.device)
        self.assertEqual(sms.device, self.device)

    def test_can_list_sms_for_device(self):
        """Check if can get SMS list associated with device"""
        self.assertIn(self.sms, sms_list(self.device))
        self.assertNotIn(self.sms, sms_list(self.anotherDevice))
