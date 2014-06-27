# coding: utf-8

import socket
import json


class GOIPClient:
    """
    Client for GOIP daemon
    """

    # Public API #

    def __init__(self, device_id, ip='localhost', port=13666):
        """Initialize GOIP client"""
        self.ip = ip
        self.port = port
        self.device_id = device_id

    def send_sms(self, recipient, message):
        """Send request for new SMS"""
        return self.query(
            self.prepare(
                'sms',
                {'recipient': recipient, 'message': message}
            )
        )

    def send_ussd(self, code):
        """Send request for new USSD"""
        return self.query(
            self.prepare(
                'ussd', {'code': code}
            )
        )

    def goip_restart(self):
        """Send request for GOIP reboot"""
        return self.query(
            self.prepare('reboot')
        )

    def debug(self, data):
        """Send RAW debug command"""
        return self.query(
            self.prepare('command', data)
        )

    # Internal methods #

    def query(self, json):
        """Query GOIP daemon"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock.sendto(json + "\n", (self.ip, self.port))
            response = sock.recv(1024)
            return response
        except socket.timeout:
            return None
        except socket.error:
            return None
        finally:
            sock.close()

    def prepare(self, request, data=None):
        return json.dumps({
            'id': self.device_id,
            'command': request.upper(),
            'data': data
        })
