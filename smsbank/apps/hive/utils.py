# encoding: utf-8
import SocketServer
import threading

from twisted.internet import protocol

################
# SocketServer #
################


class HandleUdp(SocketServer.BaseRequestHandler):
    """
    Process basic UDP requests using single handle.
    """

    def handle(self):
        # Get data and socket
        data, socket = self.request[0].strip(), self.request[1]

        # Display received data
        print "%s send us: %s" % (self.client_address[0], data)
        # Reply with uppercased data
        socket.sendto(data.upper(), self.client_address)


class ThreadedHandleUdp(SocketServer.BaseRequestHandler):
    """
    Process UDP requests using multiple instances of this handle.
    """

    def handle(self):
        # Save current thread
        thread = threading.current_thread()
        # Get data and socket
        data, socket = self.request[0].strip(), self.request[1]

        # Display received data
        print "[%s]%s send us: %s" % (
            thread.name,
            self.client_address[0],
            data
        )
        # Reply with uppercased data
        socket.sendto(data.upper(), self.client_address)

    def finish(self):
        pass


class MultiServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
    daemon_threads = True


###########
# Twisted #
###########

class Echo(protocol.DatagramProtocol):

    def datagramReceived(self, data, (host, port)):
        print "received %r from %s:%d" % (data, host, port)
        self.transport.write(data, (host, port))
