import sqlite3

conn = sqlite3.connect('Vocab.db')

c = conn.cursor()

c.execute('''CREATE TABLE Vocab(ID, Vocab_German, Vocab_Englisch)''')

conn.commit()

conn.close()