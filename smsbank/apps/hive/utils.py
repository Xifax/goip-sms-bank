# encoding: utf-8
import SocketServer


class HandleUdp(SocketServer.BaseRequestHandler):
    """
    Process basic UDP requests.
    """

    def handle(self):
        # Get data and socket
        data, socket = self.request[0].strip(), self.request[1]
        # Display received data
        print "%s send us: %s" % (self.client_address[0], data)
        # Reply with uppercased data
        socket.sendto(data.upper(), self.client_address)
