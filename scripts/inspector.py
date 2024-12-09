import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), '../rma.db')
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute('SELECT * FROM employees')
print(c.fetchall())
conn.close()
