import core
import sqlite3
from prettytable import PrettyTable
if __name__ == '__main__':
    rule_id = input("Enter Rule ID:")
    con = sqlite3.connect('nat.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM rule WHERE id=?", (rule_id,))
    rows = cur.fetchall()
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
    if input("Are you sure you want to delete this rule? (y/n)") == 'y':
        cur.execute("DELETE FROM rule WHERE id=?", (rule_id,))
        core.del_nat_rule(str(row[4]), str(row[2]), str(row[1]), str(row[3]))
        con.commit()
        print("Rule deleted.")
    con.close()
