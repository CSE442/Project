#!/usr/bin/env python2
# encoding: utf-8

# Requirements:
# sudo aptitude install python-bluetooth

# Information Sources:
# http://code.google.com/p/pybluez/source/browse/trunk/examples/simple/rfc...
# http://people.csail.mit.edu/albert/bluez-intro/x290.html#py-rfcomm-serve...

import bluetooth
import threading
import subprocess                                                        # to turn on wifi on linux system
import os

if os.name == 'posix':
    subprocess.call(['hciconfig', 'hci0', 'up'])
    subprocess.call(['hciconfig', 'hci0', 'piscan'])

print("performing inquiry...")

nearby_devices = bluetooth.discover_devices(\
        duration=2, lookup_names=True, flush_cache=True, lookup_class=False)

print("found %d devices" % len(nearby_devices))

for addr, name in nearby_devices:
    try:
        print("  %s - %s" % (addr, name))
    except UnicodeEncodeError:
        print("  %s - %s" % (addr, name.encode('utf-8', 'replace')))

name = "BluetoothChat"
uuid = "fa87c0d0-afac-11de-6b39-0800200c9a66"

server_sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)
port = server_sock.getsockname()[1]

bluetooth.advertise_service( server_sock, name, uuid )

print("Waiting for connection on RFCOMM channel %d" % port)

class echoThread(threading.Thread):
    def __init__ (self,sock,client_info, data_to_send = 0):
        threading.Thread.__init__(self)
        self.sock = sock
        self.client_info = client_info
    def run(self):                                                       # runs upon connection opening.
        print 'testing'
        try:
            while True:                                                  # will continue to retrieve data until the device is not sending anymore
                print 'testing'
                data = self.sock.recv(1024)                              # buffer size to be found with testing, in bytes (I think)
                if len(data) == 0:                                       # breaks out of loop if data recieved is nothing
                    break
                print self.client_info, ": received [%s]" % data
                self.sock.send(data)
                print self.client_info, ": sent [%s]" % data
        except IOError:
            pass
        self.sock.close()
        print self.client_info, ": disconnected"

while True:
    client_sock, client_info = server_sock.accept()
    print client_info, ": connection accepted"
    echo = echoThread(client_sock, client_info)
    echo.setDaemon(True)
    echo.start()

server_sock.close()
print "all done"
