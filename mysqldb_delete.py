from mysqldb import connection

c, conn = connection()

c.execute('DELETE FROM hourly WHERE time > 0')

conn.commit()