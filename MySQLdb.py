import MySQLdb


db = MySQLdb.connect("localhost","username", "password","table_name")

cursor = db.cursor()

x='a'
query = "INSERT INTO table_name (column_name) VALUES (%s)"
cursor.execute(query, (x,))

db.commit()
db.close()