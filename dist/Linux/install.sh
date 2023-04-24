#bin/bash

apt-get install python3
apt-get install python3-pip --upgrade
apt-get install unzip --upgrade

curl --output /tmp/SCPRelay.zip -s -L https://github.com/Snow4k/Relay-Script/archive/refs/tags/1.0.zip

unzip /tmp/SCPRelay.zip -d /usr/local/scprelay

touch /etc/systemd/system/scprelay.service;
echo $'[Unit]\nDescription=SCP Relay Server for Immix Intergration\nAfter=network.target\nStartLimitIntervalSec=0\n[Service]\nType=simple\nRestart=always\nRestartSec=1\nUser=bridgeadmin\nExecStart=/usr/bin/python3 /usr/local/scprelay/Relay-Script-1.0/src/relay.py \n[Install]\nWantedBy=multi-user.target' >> /etc/systemd/system/scprelay.service;

pip3 install -r /usr/local/scprelay/Relay-Script-1.0/requirements.txt

systemctl start scprelay;
systemctl enable scprelay;