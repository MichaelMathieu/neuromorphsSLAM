#!/usr/bin/python

from socket import *
import sys
import time

class MalformedCommandError(Exception):
    pass

class DispatchError(Exception):
    pass

class StreamServer:
    def __init__(self, host, port):
        self.sock = socket(AF_INET,SOCK_DGRAM)
        self.sock.bind((host, port))
        self.keymap = {}

    def listen(self):
        while True:
            try:
                data,addr = self.sock.recvfrom(65536)
            except timeout:
                continue

            if not data:
                print 'warning: failed recvfrom()'
                continue

            try:
                command,key,seq,value = self.parseCommand(data)
                self.dispatchCommand(command, key, seq, value, addr)
            except MalformedCommandError:
                print 'warning: bad response datagram on listen()'
                continue
            except DispatchError:
                print 'warning: cannot execute command'
                continue

    def parseCommand(self, data):
        command = None
        key = None
        seq = None
        value = None
        try:
            s = data.split('\r\n',1)
            commandLine = s[0].split()
            command = commandLine[0]
            key = commandLine[1]

            if command == 'SET':
                seq = int(commandLine[2])
                vallen = int(commandLine[3])

                if len(s[1]) != vallen+2:
                    raise MalformedCommandError

                value = s[1][0:vallen]
        except:
            raise MalformedCommandError
        return (command, key, seq, value)

    def dispatchCommand(self, command, key, seq, value, addr):
        if command == 'GET':
            try:
                rval = self.keymap[key][0]
            except KeyError:
                rval = ''

            resp = key + ' 1 ' + str(len(rval)) + '\r\n' + str(rval) + '\r\n'
            self.sock.sendto(resp, addr)

        if command == 'SET':
            now = time.time()
            if not self.keymap.has_key(key):
                self.keymap[key] = (value, {}, {addr: (now, seq)})
            else:
                cel = self.keymap[key]

                # purge sequence counters for senders that have been silent for > 5 seconds
                for a in cel[2].keys():
                    if now - cel[2][a][0] > 5.0:
                        del cel[2][a]

                # if we still have a seq counter, make sure this datagram is newer
                #   than the last datagram to arrive from the current sender for this key
                if cel[2].has_key(addr):
                    lastseq = cel[2][addr][1]

                    if lastseq >= seq:
                        return

                    cel[2][addr] = (now, seq)


                # contents are new, proceed with assignment
                self.keymap[key] = (value, cel[1], cel[2])

                # filter out listeners inactive for > 10 seconds, then transmit
                #   new data to all remaining listening addresses
                for a in cel[1].keys():
                    then = cel[1][a][0]
                    tseq = cel[1][a][1]

                    if now - then > 10.0:
                        del cel[1][a]
                        continue

                    # increment the transmit seqence number
                    cel[1][a] = (then, tseq + 1)

                    msg = key + ' ' + str(tseq) + ' ' + str(len(value)) + '\r\n' + str(value) + '\r\n'
                    self.sock.sendto(msg, a)


        if command == 'STREAM':
            now = time.time()
            if not self.keymap.has_key(key):
                self.keymap[key] = ('', {addr: (now, 1)}, {})
            elif self.keymap[key][1].has_key(addr):
                seq = self.keymap[key][1][addr][1]
                self.keymap[key][1][addr] = (now, seq)
            else:
                self.keymap[key][1][addr] = (now, 1)

if __name__ == '__main__':
    host = ''
    port = 21567

    if len(sys.argv) == 3:
        host = sys.argv[1]
        port = int(sys.argv[2])

    print 'Launching UDP streaming server on \'' + host + '\':' + str(port) + '...'
    s = StreamServer(host, port)
    s.listen()
  