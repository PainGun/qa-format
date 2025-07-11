import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent.parent / 'config' / 'qa_app.db'

# --- Inicialización ---
def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)  # Crea la carpeta si no existe
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Configuración
    c.execute('''CREATE TABLE IF NOT EXISTS config (
        clave TEXT PRIMARY KEY,
        valor TEXT
    )''')
    # Usuarios de Slack
    c.execute('''CREATE TABLE IF NOT EXISTS slack_users (
        id TEXT PRIMARY KEY,
        username TEXT,
        real_name TEXT
    )''')
    conn.commit()
    conn.close()

# --- Configuración ---
def set_config(clave, valor):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('REPLACE INTO config (clave, valor) VALUES (?, ?)', (clave, valor))
    conn.commit()
    conn.close()

def get_config(clave):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT valor FROM config WHERE clave = ?', (clave,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

# --- Usuarios de Slack ---
def save_slack_users(users):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for user in users:
        c.execute('REPLACE INTO slack_users (id, username, real_name) VALUES (?, ?, ?)',
                  (user['id'], user.get('name', ''), user.get('real_name', '')))
    conn.commit()
    conn.close()

def get_slack_users():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, username, real_name FROM slack_users')
    users = [dict(id=row[0], username=row[1], real_name=row[2]) for row in c.fetchall()]
    conn.close()
    return users 