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
            user_message TEXT NOT NULL,
            bot_response TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("✅ Base de datos y tabla creadas correctamente.")
