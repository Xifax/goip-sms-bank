# encoding: utf-8
from django.core.management.base import BaseCommand
from twisted.internet import reactor

from smsbank.apps.hive.utils import (
    HandleUdp,
    ThreadedHandleUdp,
    MultiServer,
    Echo
)

from optparse import make_option
import threading
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
        make_option(
            '--multithread',
            action='store_true',
            dest='multithread',
            default=False,
            help='Use multithreading'),
        make_option(
            '--twisted',
            action='store_true',
            dest='twisted',
            default=False,
            help='Use twisted server'),
    )

    help = """
    UDP server for testing purposes. You may test it using:
        nc -u <hostname> <port> << <data>
    """

    def handle(self, *args, **options):
        """
        Launch UDP server
        """
        if options['twisted']:
            reactor.listenUDP(options['port'], Echo())
            reactor.run()

        elif options['multithread']:
            server = MultiServer(
                (options['host'], options['port']),
                ThreadedHandleUdp
            )

            server_thread = threading.Thread(target=server.serve_forever)
            server_thread.start()

        else:
            SocketServer.UDPServer(
                (options['host'], options['port']),
                HandleUdp
            ).serve_forever()
