#!/usr/bin/env python2
# encoding: utf-8

import bluetooth
import threading
import os
import subprocess
import Queue
import channel
import thread
from message_generator import MessageGenerator



class BluetoothManager(object):

    """
    Will allow working on bluetooth objects, all contained in
    this class
    """

    manager_in_channel, manager_out_channel = channel.Channel()

    def __init__(self, name = "Default_Name",
            uuid = "fa87c0d0-afac-11de-6b39-0800200c9a66"):

        self.name = name
        self.uuid = uuid

#       devices = {
#           btmac : {
#               "client_sock" : client_sock,
#               "device_in_channel" : device_in_channel,
#               "device_out_channel" : device_out_channel,
#               "listener_thread_id" : listener_thread_id,
#               "commander_thread_id" : commander_thread_id
#               }
#
        self.devices = {}

    def bluetooth_start(self):
        """
        Inititiates the bluetooth device. Starts the server socket using
        RFCOMM, bind's it to a port, and begins listening. If using linux,
        will turn the device on.
        """
        if os.name == "posix":
            subprocess.call(['hciconfig', 'hci0', 'up', 'piscan'])

        self.server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.server_sock.bind(("", bluetooth.PORT_ANY))
        self.server_sock.listen(1)
        port = self.server_sock.getsockname()[1]

        bluetooth.advertise_service(self.server_sock,
                                    self.name,
                                    service_id = self.uuid,
                                    service_classes = [self.uuid, bluetooth.SERIAL_PORT_CLASS],
                                    profiles = [bluetooth.SERIAL_PORT_PROFILE]
                                    )

    def bluetooth_stop(self):
        """
        Stops the bluetooth device and closes all connections.
        Will turn it off if linux.
        """
        self.connection_close()
        bluetooth.stop_advertising(self.server_sock)
        self.server_sock.close()
        if os.name == "posix":
            subprocess.call(['hciconfig', 'hci0', 'noscan', 'down'])

    def add_device(self):
        """
        Will accept a connection from a device, and return
        the device's bluetooth uuid. The device can be any device that
        is currently trying to connect. To connect tanks, use discover_devices
        with connect_device.
        """

        client_sock, client_info = self.server_sock.accept()
        btmac = str(client_info[0])

        # All new devices will be given manager_in_channel and
        # and given device_out_channel
        device_in_channel, device_out_channel = channel.Channel()

#       Spawns listener thread for given btmac, used for
#       retrieving data from the device
        listener_thread_id = thread.start_new_thread(listener,\
                (client_sock, btmac, self.manager_in_channel,))

#       Spawns commander thread for given btmac, used for
#       sending data to the device
        commander_thread_id = thread.start_new_thread(commander,\
                (client_sock, device_out_channel,))

        self.devices[btmac] = {
                "client_sock" : client_sock,
                "device_in_channel" : device_in_channel,
                "device_out_channel" : device_out_channel,
                "listener_thread_id" : listener_thread_id,
                "commander_thread_id" : commander_thread_id
                }
        return btmac

    def discover_devices(self):
        """discover_devices will take 5 seconds and return a list of all devices
        in the area that are discoverable. Used for connecting tanks.
        :returns: dictionary list of btmac : common_name

        """
#       Search for nearby devices in timelimit of 5
        devices = bluetooth.discover_devices(duration=5,\
                                             lookup_names=True,\
                                             flush_cache=True,\
                                             lookup_class=False)
        nearby_devices = {}

        for i,j in devices:
            nearby_devices[i] = j

#       output a dictionary list in format:
#       nearby_devices = {
#                          btmac : device_name
#                      }
        return nearby_devices

    def connect_device(self, btmac,
                       uuid = "00001101-0000-1000-8000-00805F9B34FB"):

        """connect_device will attempt a connection to
        the given btmac. Returns boolean of whether connection
        was successful. Used to connect the tanks

        :btmac: bluetooth mac address of device to connect to
        :uuid: uuid the device is looking for, by default set for HC-06
        :returns: whether connection was successful or not

        """

        device = bluetooth.find_service(address = btmac, uuid = uuid)

        if len(device) == 0:
            return False

        client_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        client_sock.connect((device[0]["host"], device[0]["port"]))
        device_in_channel, device_out_channel = channel.Channel()

        listener_thread_id = thread.start_new_thread(listener,\
                            (client_sock, btmac, self.manager_in_channel,))

        commander_thread_id = thread.start_new_thread(commander,\
                            (client_sock, device_out_channel,))

        self.devices[btmac] = {
                "client_sock" : client_sock,
                "device_in_channel" : device_in_channel,
                "device_out_channel" : device_out_channel,
                "listener_thread_id" : listener_thread_id,
                "commander_thread_id" : commander_thread_id
                }
        return True

    def send_data(self, btmac, data):
        """send_data adds the data to the queue of btmac to read

        :btmac: bluetooth mac address of device to send data to
        :data: the actual data (any form) to be sent to the device
        :returns: none

        """
        self.devices[btmac]["device_in_channel"].send(data)

    def receive_data(self):
        """receive_data will return the oldest data in the bluetooth
        devices receive queue. Returns in a dictionary with the key as
        the btmac and value as the data it sent.

        :returns: dictionary of btmac : data

        """
        return self.manager_out_channel.receive()

    def receive_data_channel(self):
        """receive_data_channel will return the channel that external
        bluetooth devices are writing to. This can be used if the desired
        output is meant to be continuous
        :returns: BluetoothManager channel for bluetooth device threads

        """
        return self.manager_out_channel

    def connection_close(self):
        """
        Commands the bluetooth device to close all connections
        with it's devices.

        :returns: None
        """
        for btmac in self.devices.iterkeys():
            self.devices[btmac]["client_sock"].close()


def listener(sock, client_info, send_channel):
    """
    The thread entry point for a bluetooth device to send data.
    The behavior is undefined unless this function controls a thread.

    listener continuously receives data from the bluetooth device it was
    spawned for. Returns the data into send_channel.

    :sock: Socket specific to the client, generated during handshaking
    :client_info: The Bluetooth Mac Address (BTMAC) of the device
    :send_channel: Channel to send data received to
    :returns: none

    """

    assert type(send_channel) is channel.InChannel
    while True:
#       shows software errors without try, except block
        try:
            received_data = sock.recv(1024)
#           data_sent = {
#                         client_info : received_data
#                     }
            send_channel.send({client_info : received_data})
        except IOError:
            sock.close()
    thread.exit()

def commander(sock, receive_channel):
    """
    The thread entry point for a bluetooth device to send data.
    The behavior is undefined unless this function controls a thread.

    commander is used to send data to the bluetooth device. Constantly
    reads from receive_channel and will try to send data to the device

    :sock: socket to communicate with the client
    :receive_channel: channel to receive commands from
    :returns: none

    """
    assert type(receive_channel) is channel.OutChannel
    for message in MessageGenerator(receive_channel):
#       shows software errors without try, except block
        try:
            sock.send(message)
        except IOError:
            sock.close()
            break
    thread.exit()
