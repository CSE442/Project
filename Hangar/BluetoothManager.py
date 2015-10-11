#!/usr/bin/env python2
# encoding: utf-8

import bluetooth
import threading
import os
import subprocess
import Queue
import channel
import thread



class BluetoothManager(object):

    """
    Will allow working on bluetooth objects, all contained in
    this class
    """

    is_connected = False
    manager_in_channel, manager_out_channel = channel.Channel()


    def __init__(self, name = "Default_Name",
            uuid = "fa87c0d0-afac-11de-6b39-0800200c9a66"):

        self.name = name
        self.uuid = uuid

#       devices contain buid key based dictionary with another
#       dictionary as it's value. The second dictionary contains
#       client_sock, device_in_channel as keys, and respective values
#       for values
        self.devices = {}

    def bluetooth_start(self):
        """
        Inititiates the bluetooth device. If using linux,
        will turn the device on.
        """
        subprocess.call(['hciconfig', 'hci0', 'up', 'piscan'])

        self.server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.server_sock.bind(("", bluetooth.PORT_ANY))
        self.server_sock.listen(1)
        port = self.server_sock.getsockname()[1]

        bluetooth.advertise_service(self.server_sock, self.name, self.uuid)


    def bluetooth_stop(self):
        """
        Stops the bluetooth device and closes all connections.
        Will turn it off if linux.
        """
        if self.is_connected:
            self.connection_close()
        self.server_sock.close()
        subprocess.call(['hciconfig', 'hci0', 'noscan', 'down'])

    def add_device(self):
        """
        Will accept a connection from a device, and return
        the device's bluetooth uuid
        """
        client_sock, client_info = self.server_sock.accept()
        buid = str(client_info[0])

        # All new devices will be given manager_in_channel and
        # and given device_out_channel
        device_in_channel, device_out_channel = channel.Channel()
        listener_thread_id = thread.start_new_thread(listener, (client_sock, buid, self.manager_in_channel,))
        commander_thread_id = thread.start_new_thread(commander,(client_sock, device_out_channel,))
        self.devices[buid] = {
                "client_sock" : client_sock,
                "device_in_channel" : device_in_channel,
                "device_out_channel" : device_out_channel,
                "listener_thread_id" : listener_thread_id,
                "commander_thread_id" : commander_thread_id
                }
        self.is_connected = True
        return buid

    def send_data(self, buid, data):
        """send_data adds the data to the queue of buid
        :buid: bluetooth mac address of device to send data to
        :data: the actual data (any form) to be sent to the device
        :returns: none

        """
        self.devices[buid]["device_in_channel"].send(data)

    def receive_data(self):
        """receive_data will return the oldest data in the bluetooth
        devices receive queue. Returns in a dictionary with the key as
        the buid and value as the data it sent.
        :returns: dictionary of buid : data

        """
        return self.manager_out_channel.receive()

    def connection_close(self):
        """
        Commands the bluetooth device to close all connections
        with it's devices.
        """
        for buid in self.devices.iterkeys():
            self.devices[buid]["client_sock"].close()


def listener(sock, client_info, send_channel):
    """
    The thread entry point for a bluetooth device to send data.
    The behavior is undefined unless this function controls a thread.

    :sock: TODO
    :client_info: TODO
    :send_channel: TODO
    :returns: TODO

    """
    assert type(send_channel) is channel.InChannel
    while True:
        received_data = sock.recv(1024)
        send_channel.send({client_info : received_data})
    thread.exit()

def commander(sock, receive_channel):
    """
    The thread entry point for a bluetooth device to send data.
    The behavior is undefined unless this function controls a thread.

    :sock: TODO
    :receive_channel: TODO
    :returns: TODO

    """
    assert type(receive_channel) is channel.OutChannel
    while True:
        command = receive_channel.receive()
        sock.send(command)
    thread.exit()











#class BluetoothComThread(threading.Thread):
#    """
#    Thread to be used in order to communicate with a
#    bluetooth device. Should not be used outside
#    of this
#    """
#
#    def __init__ (self, sock, client_info, send_channel, receive_channel):
#        threading.Thread.__init__(self)
#        self.sock = sock
#        self.client_info = client_info
#
#        # retrieve data from BluetoothManager with receive_channel
#        # send data to BluetoothManager with send_channel
#        self.send_channel = send_channel
#        self.receive_channel = receive_channel
#
#    def run(self):
#        try:
#            while(True):
#                received_data = self.sock.recv(1024)
#                self.send_channel.send({self.client_info : received_data})
#
#        except IOError:
#            self.close()
#
#    def send_data(self, data):
#        self.sock.send(data)
#
#    def close(self):
#        self.sock.close()

