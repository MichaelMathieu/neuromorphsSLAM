#  Copyright (C) 2009 Michael Mathieu <mathieu.mic@free.fr>
#
#   This file is part of BattleShipy.
#
#   BattleShipy is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   BattleShipy is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with BattleShippy.  If not, see <http://www.gnu.org/licenses/>.
#
#   Authors:
#      Michael Mathieu <mathieu.mic@free.fr>

import socket
import threading
import Queue

debug = False
timeout = 0.1
max_size = 1024

class ClientTCPSender(threading.Thread):
    def __init__(self, connection):
        super(ClientTCPSender, self).__init__()
        self.connection = connection
        self.send_queue = Queue.Queue()
    
    def run(self):
        while True:
            to_send = self.send_queue.get(True)
            if to_send:
                self.connection.send(to_send)
            else:
                break

    def send(self, data):
        self.send_queue.put(data)
    
    def stop(self):
        self.send_queue.put(None)

class ClientTCPConnection(threading.Thread):
    def __init__(self, address, port, recv_fun, lost_fun):
        super(ClientTCPConnection, self).__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((address, port))
        self.socket.settimeout(timeout)
        self.active = True
        #self.socket.settimeout(timeout)
        self.recv_fun = recv_fun
        self.lost_fun = lost_fun
        self.address = (address, port)
        self.send_thread = ClientTCPSender(self.socket)
        self.send_thread.start()

    def run(self):
        if debug:
            print "A TCP client connection thread has started, address", \
                self.address
        while self.active:
            try:
                data = self.socket.recv(max_size)
            except socket.error, msg:
                if msg.message == "timed out":
                    continue
                else:
                    print "ERROR", msg
                    break
            if not data:
                break
            self.recv_fun(data, self.address)
        if debug:
            print "A TCP client connection thread has stopped, address", \
                self.address
        self.lost_fun(self.address)
        self.socket.close()

    def send(self, data):
        if debug:
            print "Client sends data to", self.address
        self.send_thread.send(data)

    def stop(self):
        self.send_thread.stop()
        self.active = False

class ClientTCP(object):
    def __init__(self):
        self.socket = None
        self.connections = {}

    def connect(self, address, port):
        try:
            self.connections[(address, port)] = \
                ClientTCPConnection(address, port, self.data_received,
                                    self.connection_lost)
            self.connections[(address, port)].start()
        except Exception, e:
            print "Connection failed", e
            return None
#        self.connection_made((address, port))
        if debug:
            print "Connected to", (address, port)
        return (address, port)

#    def connection_made(self, address):
#        if debug:
#            print "Client has made connection to", address

    def connection_lost(self, address):
        if debug:
            print "Client has lost connection to", address
        if address in self.connections:
            del self.connections[address]

    def data_received(self, data, address):
        if debug:
            print "Client has received data from", address

    def send(self, data, address):
#        if debug:
#            print "Client has sent data to", address
        if address in self.connections:
            self.connections[address].send(data)

    def close_connection(self, address):
        if address in self.connections:
            self.connections[address].stop()

    def close(self):
        for co in self.connections.values():
            co.stop()

if __name__ == "__main__":
    c = ClientTCP()
    c.connect("localhost", 4242)
    c.send("prout", ("localhost", 4242))
