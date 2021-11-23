#!/bin/sh
mkdir /opt/proxmox-ve-nat-tools
cd /opt/proxmox-ve-nat-tools

echo "Proxmox VE Nat Tools Installer"
echo ""
echo "This installer will install the following: "
echo " - Proxmox VE Nat Tools"
#echo " - Proxmox VE Nat Tools Web Interface"
#echo " - Proxmox VE Nat Tools API Server"
echo ""
read -p 'Input Private network bridge name: ' VMBRNM
read -p 'Input Private network host IP: ' ADDRESS
read -p 'Input Private network netmask: ' NETMASK
read -p 'Input Private network CIDR: ' CIDR
read -p 'Input Public network interface name: ' PUBLIC_IF
echo ""
echo "Initial System..."
echo ""
echo 'auto '$VMBRNM >> /etc/network/interfaces
echo 'iface '$VMBRNM' inet static' >> /etc/network/interfaces
echo '	address  '$ADDRESS >> /etc/network/interfaces
echo '	netmask  '$NETMASK >> /etc/network/interfaces
echo '	bridge_ports none' >> /etc/network/interfaces
echo '	bridge_stp off' >> /etc/network/interfaces
echo '	bridge_fd 0' >> /etc/network/interfaces
echo 'net.ipv4.ip_forward = 1' >> /etc/sysctl.conf
sysctl -p
iptables -t nat -A POSTROUTING -s $ADDRESS/$CIDR  -j MASQUERADE
apt install iptables-persistent -y
iptables-save > /etc/iptables/rules.v4

echo ""
echo "Install Proxmox VE Nat Tools and all it dependents..."
echo ""


apt install python3 python3-pip python3-venv git -y
git clone https://github.com/KiritoMiao/PVE-NATVM-Tools ./

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo 'VMBRNM = "'$VMBRNM'"' > core/config.py
echo 'ADDRESS = "'$ADDRESS'"' > core/config.py
echo 'NETMASK = "'$NETMASK'"' > core/config.py
echo 'CIDR = "'$CIDR'"' > core/config.py
echo 'PUBLIC_IF = "'$PUBLIC_IF'"' > core/config.py
python3 setup.py

echo ""
echo "Enable Internal Bridge, this might cause lost network..."
echo ""
service networking restart