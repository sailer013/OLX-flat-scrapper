import sqlite3

con = sqlite3.connect('flats.db')
cur = con.cursor()
cur.execute('''CREATE TABLE flats (
Link TEXT,
Text TEXT,
Price REAL,
Other prices TEXT
)''')
con.commit()
con.close()
