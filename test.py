import duckdb

db = duckdb.connect(database=':memory:')
db.execute("CREATE TABLE people (id INTEGER, name TEXT, age INTEGER)")
db.execute("INSERT INTO people VALUES (1, 'Alice', 25), (2, 'Bob', 30), (3, 'Charlie', 35)")
result = db.execute("SELECT * FROM people").fetchall()
print(result)