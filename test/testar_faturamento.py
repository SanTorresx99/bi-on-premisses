from backend.services.faturamento import carregar_dados_faturamento

try:
    df = carregar_dados_faturamento()
    print("✅ Dados carregados com sucesso!")
    print(df.head())  # Exibe as 5 primeiras linhas
except Exception as e:
    print("❌ Erro ao carregar dados de faturamento:", e)
