import sys
import os
import pandas as pd
from dotenv import load_dotenv
sys.path.append(os.path.abspath('.'))

from backend.db.connection import get_connection

def testar():
    load_dotenv()
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT FIRST 10 * FROM PRODUTO")  # substitua se quiser

        # pegar colunas
        colunas = [desc[0] for desc in cursor.description]
        dados = cursor.fetchall()

        df = pd.DataFrame(dados, columns=colunas)
        print("🟢 DataFrame gerado com sucesso:\n")
        print(df.head())  # mostra só os primeiros 5

        conn.close()
    else:
        print("🔴 Conexão falhou.")

if __name__ == "__main__":
    testar()
