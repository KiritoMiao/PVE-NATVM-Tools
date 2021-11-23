#!/bin/sh
mkdir /opt/proxmox-ve-nat-tools
cd /opt/proxmox-ve-nat-tools

echo "Proxmox VE Nat Tools Installer"
echo ""
echo "This installer will install the following: "
echo " - Proxmox VE Nat Tools"
echo " - Proxmox VE Nat Tools Web Interface"
echo " - Proxmox VE Nat Tools API Server"
echo ""
read -p 'Input Private network bridge name: ' VMBRNM
read -p 'Input Private network host IP: ' ADDRESS
read -p 'Input Private network netmask: ' NETMASK
read -p 'Input Private network CIDR: ' CIDR

echo ""
echo "Initial System..."
echo ""
echo 'net.ipv4.ip_forward = 1' >> /etc/sysctl.conf
sysctl -p
iptables -t nat -A POSTROUTING -s $ADDRESS/$CIDR  -j MASQUERADE
apt install iptables-persistent -y
iptables-save > /etc/iptables/rules.v4

echo ""
echo "Install Proxmox VE Nat Tools and all it dependents..."
echo ""

git clone https://github.com/KiritoMiao/PVE-NATVM-Tools ./
apt install python3 python3-pip python3-venv -y
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 setup.py
