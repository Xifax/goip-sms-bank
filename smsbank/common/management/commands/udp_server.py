# encoding: utf-8
from django.core.management.base import BaseCommand

from smsbank.apps.hive.utils import HandleUdp

from optparse import make_option
import SocketServer


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option(
            '--host',
            dest='host',
            default='localhost',
            help='Host to use'),
        make_option(
            '--port',
            dest='port',
            default=1234,
            type=int,
            help='Port to serve on'),
    )

    help = 'UDP server for testing purposes'

    def handle(self, *args, **options):
        """
        Launch UDP server
        """
        SocketServer.UDPServer(
            (options['host'], options['port']),
            HandleUdp
        ).serve_forever()
