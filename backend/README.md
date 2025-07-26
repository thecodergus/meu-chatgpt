# Meu ChatGPT Backend

Clone customizado do ChatGPT com múltiplas integrações LLM, agentes inteligentes, RAG, memória e processamento de áudio.

## Como rodar localmente

1. Instale o [uv](https://github.com/astral-sh/uv) (gerenciador de pacotes Python ultrarrápido).
2. Instale as dependências:
   ```sh
   uv pip install -r requirements/base.txt
   ```
3. Execute a API:
   ```sh
   uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload
   ```

## Estrutura do projeto

Veja o arquivo `estrutura_projeto` para detalhes.
