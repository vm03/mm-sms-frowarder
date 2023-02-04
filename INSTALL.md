# Alpine OpenRC

```
sudo cp mm-sms-frowarder-conf.d /etc/conf.d/mm-sms-frowarder
```
Add `" --martix_server <server FQDN> --martix_room '<room id>' --martix_token <auth token>"` to command_args in /etc/conf.d/mm-sms-frowarder
```
sudo cp mm-sms-frowarder-init.d /etc/init.d/mm-sms-frowarder
sudo cp mm-sms-frowarder.py /usr/bin
sudo rc-service mm-sms-frowarder start
sudo rc-update add mm-sms-frowarder default
```
