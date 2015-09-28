#!/usr/bin/env python2
# encoding: utf-8

import bluetooth
'''
nearby_devices = bluetooth.discover_devices(duration = 1, lookup_names = True)
for device in nearby_devices:
    print(device)
'''

port = bluetooth.PORT_ANY 

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", port))
server_sock.listen(1)

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"       # Most likely change in the future

bluetooth.advertise_service(server_sock, "ShawnMilligan", service_id = uuid, service_classes = [uuid, bluetooth.SERIAL_PORT_CLASS], profiles = [bluetooth.SERIAL_PORT_PROFILE])

print("Waiting for connection on RFCOMM channel %d" %port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from ", client_info)


try:
    while true:
        data = client_sock.recv(1024)
        if len(data) == 0: break
        print("received [%s]" %data)
except IOError:
    pass

print("Disconnected...")

client_sock.close()
server_sock.close()
print("All done")
