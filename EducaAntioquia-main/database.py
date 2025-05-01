import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def init_db():
    conn = sqlite3.connect('educaantioquia.db')
    c = conn.cursor()    # Crear tabla de usuarios con campo de grado
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            grado TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def register_user(username, password, email):
    try:
        conn = sqlite3.connect('educaantioquia.db')
        c = conn.cursor()
        
        hashed_password = generate_password_hash(password)
        c.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)', (username, hashed_password, email))
        
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def update_grado(username, grado):
    try:
        conn = sqlite3.connect('educaantioquia.db')
        c = conn.cursor()
        c.execute('UPDATE users SET grado = ? WHERE username = ?', (grado, username))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def get_user_grado(username):
    conn = sqlite3.connect('educaantioquia.db')
    c = conn.cursor()
    c.execute('SELECT grado FROM users WHERE username = ?', (username,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def verify_user(username, password):
    conn = sqlite3.connect('educaantioquia.db')
    c = conn.cursor()
    
    c.execute('SELECT password FROM users WHERE username = ?', (username,))
    result = c.fetchone()
    
    if result and check_password_hash(result[0], password):
        return True
    return False