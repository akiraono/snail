DATABASE=snailwords.db

all:clean createdb schema load dump


clean:
	rm -f $(DATABASE)


createdb:
	touch $(DATABASE)
	sqlite3 $(DATABASE) <create_table.sql3

schema:
	sqlite3 -batch $(DATABASE) ".tables"
	sqlite3 -batch $(DATABASE) ".schema noun"
	sqlite3 -batch $(DATABASE) ".schema adjective"

load:
	sqlite3 -batch $(DATABASE) <load_words.sql3

dump:
	sqlite3 $(DATABASE) <select_words.sql3

