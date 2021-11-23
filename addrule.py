import core
import sqlite3
if __name__ == '__main__':
    internal_ip = input("Enter Internal Ip:")
    external_port = input("Enter External Ip:")
    internal_port = input("Enter Internal Port:")
    protocol = input("Enter protocol(TCP/UDP):")
    con = sqlite3.connect('nat.db')
    cur = con.cursor()
    cur.execute("INSERT INTO rule(internalIp,externalPort,internalPort,protocol) VALUES(?,?,?,?)",(internal_ip,external_port,internal_port,protocol))
    core.set_nat_rule(protocol,external_port,internal_ip,internal_port)
    con.commit()
    con.close()
    print("Rule added successfully")
