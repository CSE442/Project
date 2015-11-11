#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from channel import InChannel

def keyboard_input(send_channel):
    assert type(send_channel) is InChannel
    while(True):
        try:
            send_channel.send({"0000" : raw_input("")})

        except KeyboardInterrupt:
            thread.exit()
