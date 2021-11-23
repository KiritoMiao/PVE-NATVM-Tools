import sqlite3
from prettytable import PrettyTable
if __name__ == '__main__':
    con = sqlite3.connect('nat.db')
    cur = con.cursor()
    cur.execute('SELECT * from rule')
    rows = cur.fetchall()
    cur.close()
    con.close()
    output = PrettyTable([
        'ID',
        'IP Address',
        'External Port',
        'Internal Port',
        'protocol'], border=False, align="l")
    for row in rows:
        output.add_row([
            row[0],row[1],row[2],row[3],row[4]])
    print(output)