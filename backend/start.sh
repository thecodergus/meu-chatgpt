#!/bin/bash

# Script para iniciar o servidor FastAPI com LangGraph

# Verifica se o Python está instalado
if ! command -v python3 &> /dev/null
then
    echo "Python3 não encontrado. Por favor, instale o Python3."
    exit 1
fi

# Verifica se o pip está instalado
if ! command -v pip3 &> /dev/null
then
    echo "pip3 não encontrado. Por favor, instale o pip3."
    exit 1
fi

# Instala as dependências
echo "Instalando dependências..."
pip3 install -r requirements.txt

# Verifica se o arquivo .env existe
if [ ! -f .env ]; then
    echo "Arquivo .env não encontrado. Criando um novo a partir do exemplo..."
    if [ -f .env.example ]; then
        cp .env.example .env
    else
        echo "OPENAI_API_KEY=sua_openai_api_key_aqui" > .env
        echo "ANTHROPIC_API_KEY=sua_anthropic_api_key_aqui" >> .env
        echo "OPENROUTER_API_KEY=sua_openrouter_api_key_aqui" >> .env
        echo "USE_ANTHROPIC=false" >> .env
        echo "USE_OPENROUTER=false" >> .env
    fi
    echo "Por favor, configure suas variáveis de ambiente no arquivo .env"
fi

# Inicia o servidor
echo "Iniciando servidor FastAPI..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload