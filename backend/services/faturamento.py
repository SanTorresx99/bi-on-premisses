# backend/services/faturamento.py

import pandas as pd
from backend.db.connection import get_connection
from pathlib import Path

def carregar_dados_faturamento(data_inicio, data_fim):
    try:
        conn = get_connection()
        sql_path = Path(__file__).parent.parent / "sql" / "faturamento.sql"

        with open(sql_path, "r", encoding="utf-8") as file:
            query = file.read()

        # Substituir parâmetros diretamente no SQL (por não suportar bind com fdb + pandas)
        query = query.format(
            data_inicio=data_inicio.strftime('%Y-%m-%d'),
            data_fim=data_fim.strftime('%Y-%m-%d')
        )

        print(f"🔗 Conectando ao banco: {conn.dsn if hasattr(conn, 'dsn') else 'sem DSN'}")

        df = pd.read_sql(query, conn)

        print("🟢 DataFrame gerado com sucesso:")
        print(df.head())
        return df

    except Exception as e:
        print(f"Erro ao carregar dados de faturamento: {e}")
        return pd.DataFrame()


if __name__ == "__main__":
    import datetime
    data_ini = datetime.date.today() - datetime.timedelta(days=30)
    data_fim = datetime.date.today()
    df_teste = carregar_dados_faturamento(data_ini, data_fim)
    print(df_teste.head())
