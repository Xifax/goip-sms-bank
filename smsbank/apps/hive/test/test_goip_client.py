from django.test import TestCase

from smsbank.apps.hive.client import GOIPClient

import threading
import SocketServer
import json


class GOIPHandler(SocketServer.BaseRequestHandler):
    """Server handle stub"""

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        socket.sendto(data, self.client_address)


class GOIPStub(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
    """Server stub"""
    allow_reuse_address = True


class ClientTestCase(TestCase):
    def setUp(self):
        self.ip = 'localhost'
        self.port = 9999
        self.device_id = 1

        # Launch test server
        self.server = GOIPStub((self.ip, self.port), GOIPHandler)
        server_thread = threading.Thread(target=self.server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.start()

    def test_can_query_server(self):
        """Check if can perform simple query command"""
        client = GOIPClient(self.device_id, self.ip, self.port)
        response = client.send_sms('recipient', 'test')
        self.assertIn('data', json.loads(response))

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
