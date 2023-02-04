#!/sbin/openrc-run

supervisor=supervise-daemon
command=/usr/bin/mm-sms-frowarder.py

description="sms forwarder Daemon"

depend() {
   need dbus
}
