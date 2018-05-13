#!/bin/bash
# Turn ethernet cable into DHCP device
set -xeuo pipefail

DEVICE='ens9'
INTERNET='wlp3s0'
ROUTERIP='192.168.123.1'

echo 'Restarting Device'
ip link set "$DEVICE" down
ip link set "$DEVICE" up
# Check if ip already assigned
if [ -z "$(ip a | grep -A 5 ens9 | grep 192.168.123.1)" ]; then
    ip addr add "$ROUTERIP"/24 dev "$DEVICE"  # arbitrary address
fi

echo 'Allowing ip forwarding/enabling Nat'
sysctl net.ipv4.ip_forward=1
iptables -t nat -A POSTROUTING -o "$INTERNET" -j MASQUERADE
iptables -A FORWARD -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
iptables -A FORWARD -i "$DEVICE" -o "$INTERNET" -j ACCEPT

echo 'Creating /etc/dhcpd.conf file'
#Config file: /etc/dhcpd.conf
cat > /etc/dhcpd.conf <<- EOM
option domain-name-servers 8.8.8.8, 8.8.4.4;
option subnet-mask 255.255.255.0;
option routers $ROUTERIP;
subnet 192.168.123.0 netmask 255.255.255.0 {
    range 192.168.123.150 192.168.123.250;
}
EOM
#Database file: /var/lib/dhcp/dhcpd.leases
# cat this to see if a device has been assigned a lease
#PID file: /var/run/dhcpd.pid
pkill dhcpd || true
dhcpd $DEVICE 
