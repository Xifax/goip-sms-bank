# encoding: utf-8
from django.core.management.base import BaseCommand

from optparse import make_option
import SocketServer as ss
import multiprocessing as mp

from smsbank.apps.hive.utils import (
    LocalAPIServer,
    GoipUDPListener
)


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option(
            '--host',
            dest='host',
            default='0.0.0.0',
            help='Host to use'),
        make_option(
            '--port',
            dest='port',
            default=44444,
            type=int,
            help='Port to serve on')
    )

    help = """
    Launch GOIP daemon for interacting with GOIP devices and performing
    SMS/USSD operations.
    """

    def handle(self, *args, **options):
        """
        Launch GOIP daemon.
        """
        # Launch local API handler
        apiQueue = mp.Queue()
        apiHandle = LocalAPIServer(apiQueue,)
        apiHandle.start()

        # Initialize shared dictionary
        manager = mp.Manager()
        seedDic = manager.dict()

        # Launch GOIP server
        server = ss.UDPServer(
            (options['host'], options['port']),
            GoipUDPListener
        )
        server.serve_forever()