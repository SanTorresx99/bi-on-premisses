import os
from dotenv import load_dotenv
import fdb

load_dotenv()

def get_connection():
    try:
        dsn = os.getenv("FIREBIRD_DSN")
        print(f"🔗 Conectando ao banco: {dsn}")
        conn = fdb.connect(
            dsn=os.getenv("FIREBIRD_DSN"),
            user=os.getenv("FIREBIRD_USER"),
            password=os.getenv("FIREBIRD_PASSWORD")
        )
        print("✅ Conexão com Firebird realizada com sucesso!")
        return conn
    except Exception as e:
        print("❌ Erro ao conectar ao banco:", e)
        return None
