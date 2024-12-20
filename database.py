import sqlite3

# Initialize database
def init_db():
    conn = sqlite3.connect("roulette.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            balance INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Add a new player
def add_player(name, balance):
    conn = sqlite3.connect("roulette.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO players (name, balance) VALUES (?, ?)", (name, balance))
    conn.commit()
    conn.close()

# Get player balance
def get_balance(name):
    conn = sqlite3.connect("roulette.db")
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM players WHERE name=?", (name,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

# Update player balance
def update_balance(name, balance):
    conn = sqlite3.connect("roulette.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE players SET balance=? WHERE name=?", (balance, name))
    conn.commit()
    conn.close()

init_db()
