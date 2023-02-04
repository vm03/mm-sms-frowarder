#!/usr/bin/env python3

import argparse
import json
import requests
import sys
import signal

import gi
gi.require_version('ModemManager', '1.0')
from gi.repository import Gio, GLib, GObject, ModemManager

class SmsWatcher():

    def __init__(self, martix_server, martix_room, martix_token):
        self.martix_server = martix_server
        self.martix_room = martix_room
        self.martix_token = martix_token
        self.connection = Gio.bus_get_sync(Gio.BusType.SYSTEM, None)
        self.manager = ModemManager.Manager.new_sync(
            self.connection,
            Gio.DBusObjectManagerClientFlags.DO_NOT_AUTO_START,
            None)
        for obj in self.manager.get_objects():
            messaging = obj.get_modem_messaging()
            messaging.connect('added',self.on_sms)

    def on_sms(self, messaging, path, prop):
        for sms in messaging.list_sync():
            if sms.get_path() == path:
                text = 'SMS From: '+sms.get_number()+'\n'+sms.get_text()
                print (text)
                self.send_to_matrix(text)

    def send_to_matrix(self, text):
         url = 'https://'+self.martix_server+'/_matrix/client/r0/rooms/'+self.martix_room+'/send/m.room.message?access_token='+self.martix_token
         payload = {'msgtype': 'm.text', 'body' : text}
         headers = {'Content-Type': 'application/json; charset=utf-8'}
         resp = requests.post(url, data = json.dumps(payload), headers = headers)
         print(resp.text)

def signal_handler(loop):
    """SIGHUP and SIGINT handler."""
    loop.quit()


def main():

    parser = argparse.ArgumentParser(description='mm-sms-frowarder')
    parser.add_argument('--martix_server', default='output', help='Matrix IM server FQDN')
    parser.add_argument('--martix_room', default='', help='Matrix room ID')
    parser.add_argument('--martix_token', default='', help='Matrix access_token')
    args = parser.parse_args()

    SmsWatcher(args.martix_server,args.martix_room,args.martix_token)

    main_loop = GLib.MainLoop()
    GLib.unix_signal_add(
        GLib.PRIORITY_HIGH, signal.SIGHUP, signal_handler, main_loop)
    GLib.unix_signal_add(
        GLib.PRIORITY_HIGH, signal.SIGTERM, signal_handler, main_loop)
    try:
        main_loop.run()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
