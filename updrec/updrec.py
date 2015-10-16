from __future__ import print_function
__author__ = 'mpaly'


import SocketServer
import argparse
import string

class UdpHandler(SocketServer.BaseRequestHandler):
    """
    upd request handler (instantiated once for each udp request)
   """
    def handle(self):
        self.data = self.request[0]
        self.socket = self.request[1]
        print("{client_ip}:{client_port} : {hexdata}  ==> {rawdata}".format(
            client_ip=self.client_address[0],
            client_port=self.client_address[1],
            hexdata= ':'.join(x.encode('hex') for x in self.data), #bitstring.BitArray(bytes=self.data)
            rawdata=  filter(lambda x: x in string.printable, self.data)))
        if self.server.bounce_back:
            self.socket.sendto(self.request[0], self.client_address)


class SimpleUdpServer(SocketServer.UDPServer):
    def __init__(self, server_address, RequestHandlerClass, bounce_back):
        SocketServer.UDPServer.__init__(self, server_address, RequestHandlerClass)
        self.bounce_back = bounce_back



class UdpRec():
    """
    this class holds a simple udp receiver that print the received packets to the shell
    """

    def __init__(self, host, port, bounce_back=False):
        self.host = None
        self.port = None
        self.handler = None
        self.server = None
        self.bounce_back = None
        self.initialize(host, port, bounce_back)

    def initialize(self, host, port, bounce_back):
        self.host = host
        self.port = port
        self.bounce_back = bounce_back
        self.handler = UdpHandler
        self.server = SimpleUdpServer((self.host, self.port), self.handler, bounce_back)

    def serve(self):
        print("""
UDP Receiver listening on :{port}
============================================""".format(port=self.port))
        self.server.serve_forever()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="UDP listener on some port")
    parser.add_argument("--port", dest="port", default=2000, help="port to listen on", type=int)
    parser.add_argument("--host", dest="host", default="localhost", help="host name to listen on")
    parser.add_argument("--bounceback", dest="bounce_back", help="packets a bounced back to source", action='store_true')
    args=parser.parse_args()
    myUdpRec = UdpRec(args.host, args.port, args.bounce_back)

    myUdpRec.serve()

