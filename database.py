import sqlite3

def create_db():
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS passwords
                 (id INTEGER PRIMARY KEY, 
                 website TEXT NOT NULL, 
                 username TEXT NOT NULL, 
                 password BLOB NOT NULL)''')
    conn.commit()
    conn.close()

def add_password(website, username, encrypted_password):
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute("INSERT INTO passwords (website, username, password) VALUES (?, ?, ?)", 
              (website, username, encrypted_password))
    conn.commit()
    conn.close()

def get_passwords():
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute("SELECT * FROM passwords")
    results = c.fetchall()
    conn.close()
    return results

def delete_password(password_id):
    """Delete a password entry from the database based on its ID."""
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute("DELETE FROM passwords WHERE id = ?", (password_id,))
    conn.commit()
    conn.close()
