import sqlite3
con = sqlite3.connect("pokehand.db")

cursor = con.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS SETS (id TEXT PRIMARY KEY, code TEXT, name TEXT)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS CARDS (id TEXT PRIMARY KEY, name TEXT, types TEXT, supertype TEXT, subtypes TEXT, set_id TEXT, number INTEGER)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS DECKS (id INTEGER PRIMARY KEY, name TEXT)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS CARD_DECKS (deck_id INTEGER, card_id TEXT, quantity INTEGER, UNIQUE(deck_id, card_id)) """)