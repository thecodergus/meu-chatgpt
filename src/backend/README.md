# FastAPI com LangGraph

Este projeto implementa um backend FastAPI com endpoint similar ao da OpenAI para LLMs, utilizando LangGraph por baixo dos panos.

## Funcionalidades

- Endpoint `/v1/chat/completions` compatível com a API da OpenAI
- Integração com LangGraph para processamento de linguagem
- Suporte a múltiplos provedores de LLM (OpenAI, Anthropic e OpenRouter)
- Seleção de provedor através da requisição
- Configuração de temperatura, top_p e max_tokens através da requisição
- Streaming de respostas
- Configuração fácil com variáveis de ambiente
- Tratamento de erros específico por provedor
- Endpoints de health check e métricas de performance
- Documentação automática da API (Swagger/OpenAPI)
- Testes unitários e de integração abrangentes

## Estrutura do Projeto

```
fastapi-langgraph/
├── app/
│   ├── __init__.py
│   ├── main.py              # Arquivo principal da aplicação
│   ├── config.py             # Configuração e validação de variáveis de ambiente
│   ├── .env                  # Variáveis de ambiente (não versionado)
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1.py            # Rotas da API v1
│   │   └── health.py        # Rotas de health check
│   ├── models/
│   │   ├── __init__.py
│   │   └── openai.py        # Modelos de dados compatíveis com OpenAI
│   └── services/
│       ├── __init__.py
│       ├── model_factory.py      # Fábrica de modelos de linguagem
│       ├── message_converter.py  # Conversor de mensagens
│       ├── graph_manager.py      # Gerenciador de grafos LangGraph
│       ├── langgraph_service.py  # Serviço LangGraph
│       └── error_handler.py     # Tratamento de erros
├── requirements.txt         # Dependências do projeto
├── .env.example             # Exemplo de variáveis de ambiente
├── Dockerfile               # Configuração do Docker
├── docker-compose.yml       # Configuração do Docker Compose
├── start.sh                 # Script de inicialização
├── test_api.py              # Script de teste da API
├── tests/                   # Testes unitários e de integração
│   ├── __init__.py
│   ├── test_model_factory.py
│   ├── test_message_converter.py
│   ├── test_error_handler.py
│   ├── test_api.py
│   └── test_health.py
└── README.md                # Documentação do projeto
```

## Instalação

### Usando pip

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure as variáveis de ambiente no arquivo `.env`

3. Execute a aplicação:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

### Usando Docker

1. Configure as variáveis de ambiente no arquivo `.env`

2. Construa e execute com Docker Compose:
   ```bash
   docker-compose up --build
   ```

## Uso

### Endpoint de Chat Completion

```bash
# Usando o provedor padrão (OpenAI) com parâmetros padrão
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [
      {
        "role": "user",
        "content": "Olá, como você está?"
      }
    ]
  }'

# Usando OpenRouter com temperatura, top_p e max_tokens personalizados
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-3.5-turbo",
    "provider": "openrouter",
    "temperature": 0.8,
    "top_p": 0.9,
    "max_tokens": 100,
    "messages": [
      {
        "role": "user",
        "content": "Olá, como você está?"
      }
    ]
  }'

# Usando Anthropic com temperatura baixa e limite de tokens
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-3-haiku-20240307",
    "provider": "anthropic",
    "temperature": 0.1,
    "top_p": 0.1,
    "max_tokens": 50,
    "messages": [
      {
        "role": "user",
        "content": "Olá, como você está?"
      }
    ]
  }'
```

### Streaming

```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-3.5-turbo",
    "provider": "openrouter",
    "temperature": 0.7,
    "top_p": 0.9,
    "max_tokens": 150,
    "messages": [
      {
        "role": "user",
        "content": "Conte-me uma história curta"
      }
    ],
    "stream": true
  }'
```

## Configuração

### Variáveis de Ambiente

- `OPENAI_API_KEY`: Chave da API da OpenAI
- `ANTHROPIC_API_KEY`: Chave da API da Anthropic (opcional)
- `OPENROUTER_API_KEY`: Chave da API da OpenRouter (opcional)
- `USE_ANTHROPIC`: Defina como "true" para usar Anthropic como padrão
- `USE_OPENROUTER`: Defina como "true" para usar OpenRouter como padrão
- `HOST`: Host para o servidor (padrão: 0.0.0.0)
- `PORT`: Porta para o servidor (padrão: 8000)

## Endpoints

- `GET /`: Endpoint de verificação
- `POST /v1/chat/completions`: Endpoint de chat completion (suporta streaming quando `stream: true`)
- `GET /health/status`: Endpoint de health check básico
- `GET /health/detailed`: Endpoint de health check detalhado
- `GET /health/ready`: Endpoint de readiness check

## Tecnologias

- [FastAPI](https://fastapi.tiangolo.com/): Framework web rápido para Python
- [LangGraph](https://github.com/langchain-ai/langgraph): Framework para construção de agentes de linguagem
- [LangChain](https://github.com/langchain-ai/langchain): Framework para aplicações com LLMs
- [LangChain OpenAI](https://github.com/langchain-ai/langchain): Integração com OpenAI
- [LangChain Anthropic](https://github.com/langchain-ai/langchain): Integração com Anthropic
- [Docker](https://www.docker.com/): Plataforma de containerização

## Suporte a Provedores de LLM

### Seleção de Provedor

O provedor pode ser selecionado através do campo `provider` na requisição:

- `openai`: OpenAI (padrão)
- `anthropic`: Anthropic
- `openrouter`: OpenRouter

Se nenhum provedor for especificado, o sistema usará o provedor configurado como padrão através das variáveis de ambiente.

### Parâmetros de Geração

Os seguintes parâmetros podem ser configurados na requisição:

- `temperature`: Controla a aleatoriedade da geração (0.0 a 1.0)
- `top_p`: Controla a diversidade da geração (0.0 a 1.0)
- `max_tokens`: Limita o número máximo de tokens na resposta

### OpenAI
O provedor padrão é o OpenAI. Basta configurar a variável `OPENAI_API_KEY` no arquivo `.env`.

### Anthropic
Para usar o Anthropic como padrão, configure as variáveis:
```
ANTHROPIC_API_KEY=sua_chave_api
USE_ANTHROPIC=true
```

### OpenRouter
Para usar o OpenRouter como padrão, configure as variáveis:
```
OPENROUTER_API_KEY=sua_chave_api
USE_OPENROUTER=true
```

## Testes

### Testes Automatizados
O projeto inclui uma suite completa de testes unitários e de integração. Para executar os testes:
```bash
pytest
```

### Teste da API
Você pode testar a API executando o script de teste:
```bash
python test_api.py
```

## Documentação da API

A documentação automática da API está disponível em:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.