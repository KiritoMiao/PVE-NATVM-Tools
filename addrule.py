import sys
import core
import sqlite3
import re


def is_valid_ip(ip):
    m = re.match(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", ip)
    return bool(m) and all(map(lambda n: 0 <= int(n) <= 255, m.groups()))


if __name__ == '__main__':
    internal_ip = input("Enter Internal Ip:")
    external_port = input("Enter External Port:")
    internal_port = input("Enter Internal Port:")
    protocol = input("Enter protocol(tcp/udp):")
    if protocol != "tcp" or protocol != "udp":
        sys.exit("Invalid protocol")
    if external_port < 0 or external_port > 65535:
        sys.exit("Invalid external port")
    if internal_port < 0 or internal_port > 65535:
        sys.exit("Invalid internal port")
    if is_valid_ip(internal_ip) == False:
        sys.exit("Invalid internal ip")
    con = sqlite3.connect('nat.db')
    cur = con.cursor()
    cur.execute("INSERT INTO rule(internalIp,externalPort,internalPort,protocol) VALUES(?,?,?,?)",
                (internal_ip, external_port, internal_port, protocol))
    core.set_nat_rule(protocol, external_port, internal_ip, internal_port)
    con.commit()
    con.close()
    print("Rule added successfully")
