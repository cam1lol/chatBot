import sqlite3

# Nombre del archivo de la base de datos
DB_NAME = "chatbot.db"

def create_tables():
    """Crea la tabla de conversaciones si no existe."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            user_message TEXT NOT NULL,
            bot_response TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()
    print("✅ Base de datos y tabla 'conversations' creadas correctamente.")

def check_columns():
    """Verifica si la columna session_id existe en la tabla, si no, la agrega."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Consultar la estructura de la tabla
    cursor.execute("PRAGMA table_info(conversations)")
    columns = [col[1] for col in cursor.fetchall()]

    if "session_id" not in columns:
        cursor.execute("ALTER TABLE conversations ADD COLUMN session_id TEXT NOT NULL DEFAULT 'default_session'")
        conn.commit()
        print("✅ Se agregó la columna 'session_id' a la tabla 'conversations'.")
    
    conn.close()

if __name__ == "__main__":
    create_tables()  # Crea la tabla si no existe
    check_columns()  # Verifica si 'session_id' existe y la agrega si falta
