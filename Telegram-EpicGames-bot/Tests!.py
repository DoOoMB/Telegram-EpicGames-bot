import sqlite3

con = sqlite3.connect(":memory:")
cur = con.cursor()

cur.execute("create table tab(one integer, two integer)")
cur.execute("""insert into tab(one, two) values(?, ?)""", [1, 2])
a = cur.execute("""select * from tab""")
print(a.fetchall())

one = 'one'
num = 4
two = 2
a = cur.execute("update tab set (%s) = ? where two = ?" % one, [num, two])
print(a.fetchall())
a = cur.execute("""Select * from tab""")
print(a.fetchall())

con.commit()