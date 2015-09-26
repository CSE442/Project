#!/usr/bin/env python2
# encoding: utf-8

import bluetooth

nearby_device = bluetooth.discover_devices(lookup_names=True)

print('found %d devices' %len(nearby_device))
