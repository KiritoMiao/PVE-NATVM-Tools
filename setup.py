import core
import sqlite3
if __name__ == '__main__':
    print("Create NAT-Tool Database")
    con = sqlite3.connect("nat.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS rule (id INTEGER PRIMARY KEY NOT NULL, internalIp TEXT NOT NULL, externalPort INTEGER NOT NULL, internalPort INTEGER NOT NULL, protocol TEXT NOT NULL)")
    con.commit()
    con.close()