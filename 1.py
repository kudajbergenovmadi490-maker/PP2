import psycopg2

conn = psycopg2.connect(host='localhost', database='postgres', user='postgres', password='Madi2007@#', port=5432) 

cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name VARCHAR(255), email VARCHAR(255))")

cursor.execute("INSERT INTO users (name, email) VALUES ('John Doe', 'john.doe@example.com')")
conn.commit()
cursor.close()
conn.close()

print("Table created successfully")
print("Data inserted successfully")
print("Connection closed successfully")
print("Table created successfully")
print("Data inserted successfully")
print("Connection closed successfully")
print("Table created successfully")
print("Data inserted successfully")
print("Connection closed successfully")