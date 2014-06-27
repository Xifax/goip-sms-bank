from django.test import TestCase

from smsbank.apps.hive.models import (
    Device,
    Sms
)
from smsbank.apps.hive.services import (
    device_exists,
    get_or_create_device,
    initialize_device,
    get_device_by_id,
    get_device,
    new_sms,
    list_sms
)


class DeviceTestCase(TestCase):
    def setUp(self):
        self.device = Device.objects.create(
            ip='127.0.0.1',
            port=1234,
            device_id='abc'
        )

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

    def test_can_get_device_by_devid(self):
        """Check if can get previously saved device by its devid"""
        self.assertEqual(self.device, get_device(self.device.device_id))

    def test_can_initialize_device_from_daemon(self):
        """Check if can initialize device from GOIP daemon"""
        self.assertIsInstance(
            initialize_device('test', '0.0.0.0', 44444),
            Device
        )


class SmsTestCase(TestCase):
    def setUp(self):
        self.device = Device.objects.create(
            ip='127.0.0.1',
            port=1234,
            device_id='abc'
        )
        self.anotherDevice = Device.objects.create(ip='0.0.0.1', port=1111)
        self.sms = Sms.objects.create(
            recipient='test',
            message='hello',
            device=self.device
        )

    def test_can_create_new_sms(self):
        """Check if can create new SMS and associate it with device"""
        sms = new_sms(
            'who goes here?',
            'hi there!',
            True,
            self.device.device_id
        )
        self.assertEqual(sms.device, self.device)
        self.assertEqual(sms.message, 'hi there!')

    def test_can_list_sms_for_device(self):
        """Check if can get SMS list associated with device"""
        self.assertIn(self.sms, list_sms(self.device))
        self.assertNotIn(self.sms, list_sms(self.anotherDevice))
