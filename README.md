---
## 🔧 Configuração do Ambiente
Antes de rodar o projeto pela primeira vez:
1. Copie o arquivo de exemplo `.env.example` para `.env`:
cp .env.example .env

2. Edite o arquivo .env e preencha com suas credenciais reais de banco, token JWT e IP da IA local.

##⚠️ Atenção: nunca compartilhe ou comite seu arquivo .env real. Ele contém dados sensíveis.

Exemplo de conteúdo do .env:
# 🔗 Conexão com Firebird
FIREBIRD_DSN=localhost:/caminho/para/seu/DATABASE.FDB
FIREBIRD_USER=user_default_SYSDBA
FIREBIRD_PASSWORD=password_default_masterkey

# 🔐 JWT para autenticação
JWT_SECRET=uma_chave_bem_segura

# 🤖 API da IA local (Ollama)
OLLAMA_API=http://localhost:11434
