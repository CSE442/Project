#!/usr/bin/env python2
# encoding: utf-8

import bluetooth
import threading
import os
import subprocess
import Queue



class BluetoothManager(object):

    """
    Will allow working on bluetooth objects, all contained in
    this class
    """

    is_connected = False

    def __init__(self, name = "Default_Name",
            uuid = "fa87c0d0-afac-11de-6b39-0800200c9a66"):

        self.name = name
        self.uuid = uuid
        self.devices = {}

    def bluetooth_start(self):
        '''
        Inititiates the bluetooth device. If using linux,
        will turn the device on.
        '''
        subprocess.call(['hciconfig', 'hci0', 'up', 'piscan'])

        self.server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.server_sock.bind(("", bluetooth.PORT_ANY))
        self.server_sock.listen(1)
        port = self.server_sock.getsockname()[1]

        bluetooth.advertise_service(self.server_sock, self.name, self.uuid)


    def bluetooth_stop(self):
        '''
        Stops the bluetooth device. Will throw an exception
        if connections are still open. Will turn it
        off if linux.
        '''
        if self.is_connected:
            raise ValueError('Attempted to stop bluetooth, but connections exist')
        self.server_sock.close()
        subprocess.call(['hciconfig', 'hci0', 'noscan', 'down'])

    def add_device(self):
        '''
        Will accept a connection from a device, and return
        the device's bluetooth uuid
        '''
        client_sock, client_info = self.server_sock.accept()
        buid = str(client_info[0])
        self.devices[buid] = BluetoothComThread(client_sock, buid)
        self.devices[buid].setDaemon(True)
        self.devices[buid].start()
        self.is_connected = True
        return buid

    def send_data(self, buid, data):
        '''
        sends data to the device specified by buid, throws an exception if device is no longer connected.
        '''
        try:
            self.devices[buid].send_data(data)
        except bluetooth.btcommon.BluetoothError:
            self.connection_close()
            raise ValueError("Tried to send data to: %s and is disconnected" % buid)

    def receive_data(self):
        pass


    def connection_close(self):
        '''
        Commands the bluetooth device to close all connections
        with it's devices.
        '''
        for buid,device in self.devices.iteritems():
            device.close()


        self.is_connected = False

class BluetoothComThread(threading.Thread):
    '''
    Thread to be used in order to communicate with a
    bluetooth device. Should not be used outside
    of this
    '''
    send_queue = Queue.Queue()
    receive_queue = Queue.Queue()

    def __init__ (self, sock, client_info):
        threading.Thread.__init__(self)
        self.sock = sock
        self.client_info = client_info

    def run(self):
        try:
            while(True):
                recieved_data = self.sock.recv(1024)
                print self.client_info, ' ', recieved_data
        except IOError:
            self.close()

    def send_data(self, data):
        self.sock.send(data)

    def close(self):
        self.sock.close()
