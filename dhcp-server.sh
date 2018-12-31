#!/bin/bash
# Turn ethernet cable into DHCP device
set -xeuo pipefail

BRIDGE_INTERFACE='ens9'
INTERNET_INTERFACE='wlp3s0'
SUBNET='192.168.2'
ROUTERIP="$SUBNET.1"

echo 'Restarting Device'
ip link set "$BRIDGE_INTERFACE" down
ip link set "$BRIDGE_INTERFACE" up
# Check if ip already assigned
if [ -z "$(ip a | grep -A 5 ens9 | grep $ROUTERIP)" ]; then
    ip addr add "$ROUTERIP"/24 dev "$BRIDGE_INTERFACE"  # arbitrary address
fi

echo 'Allowing ip forwarding/enabling Nat'
sysctl net.ipv4.ip_forward=1
iptables -t nat -A POSTROUTING -o "$INTERNET_INTERFACE" -j MASQUERADE
iptables -A FORWARD -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
iptables -A FORWARD -i "$BRIDGE_INTERFACE" -o "$INTERNET_INTERFACE" -j ACCEPT

echo 'Creating /etc/dhcpd.conf file'
#Config file: /etc/dhcpd.conf
cat > /etc/dhcpd.conf <<- EOM
option domain-name-servers 8.8.8.8, 8.8.4.4;
option subnet-mask 255.255.255.0;
option routers $ROUTERIP;
subnet $SUBNET.0 netmask 255.255.255.0 {
    range $SUBNET.2 $SUBNET.250;
}
EOM
#Database file: /var/lib/dhcp/dhcpd.leases
# cat this to see if a device has been assigned a lease
#PID file: /var/run/dhcpd.pid
pkill dhcpd || true
dhcpd $BRIDGE_INTERFACE 
