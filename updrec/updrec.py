from __future__ import print_function
__author__ = 'mpaly'


import SocketServer
import argparse

class UdpHandler(SocketServer.BaseRequestHandler):
    """
    upd request handler (instantiated once for each udp request)
   """
    def handle(self):
        self.data = self.request[0]
        self.socket = self.request[1]
        print("{client} : {hexdata}  ==> {rawdata}".format(
            client=self.client_address[0],
            hexdata= ':'.join(x.encode('hex') for x in self.data), #bitstring.BitArray(bytes=self.data)
            rawdata=self.data))



class UdpRec():
    """
    this class holds a simple udp receiver that print the received packets to the shell
    """

    def __init__(self, host, port):
        self.initialize(host, port)

    def initialize(self, host, port):
        self.host = host
        self.port = port
        self.handler = UdpHandler
        self.server = SocketServer.UDPServer((self.host,self.port), self.handler)

    def serve(self):
        print("""
UDP Receiver listening on :{port}
============================================""""".format(port=self.port))
        self.server.serve_forever()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="UDP listener on some port")
    parser.add_argument("--port",dest="port", default=1234, help="port to listen on", type=int)
    parser.add_argument("--host",dest="host", default="localhost", help="host name to listen on")
    args=parser.parse_args()
    myUdpRec = UdpRec(args.host, args.port)

    myUdpRec.serve()

