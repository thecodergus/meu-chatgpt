import requests
import json
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

def test_chat_completion(provider=None, temperature=0.7, top_p=1.0, max_tokens=None):
    """Testa o endpoint de chat completion"""
    url = "http://localhost:8000/v1/chat/completions"
    
    # Dados da requisição
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": "Olá, como você está?"
            }
        ],
        "temperature": temperature,
        "top_p": top_p
    }
    
    # Adiciona max_tokens se especificado
    if max_tokens:
        data["max_tokens"] = max_tokens
    
    # Adiciona o provedor se especificado
    if provider:
        data["provider"] = provider
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print(f"Teste de chat completion com {provider or 'provedor padrão'} bem-sucedido!")
            print("Resposta:", response.json())
        else:
            print(f"Erro na requisição: {response.status_code}")
            print("Detalhes:", response.text)
    except Exception as e:
        print(f"Erro ao conectar à API: {str(e)}")

def test_streaming(provider=None, temperature=0.7, top_p=1.0, max_tokens=None):
    """Testa o endpoint de streaming"""
    url = "http://localhost:8000/v1/chat/completions/stream"
    
    # Dados da requisição
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": "Conte-me uma história curta"
            }
        ],
        "stream": True,
        "temperature": temperature,
        "top_p": top_p
    }
    
    # Adiciona max_tokens se especificado
    if max_tokens:
        data["max_tokens"] = max_tokens
    
    # Adiciona o provedor se especificado
    if provider:
        data["provider"] = provider
    
    try:
        response = requests.post(url, json=data, stream=True)
        if response.status_code == 200:
            print(f"\nTeste de streaming com {provider or 'provedor padrão'} bem-sucedido!")
            print("Resposta streaming:")
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    if decoded_line.startswith('data: '):
                        data = decoded_line[6:]  # Remove 'data: ' prefix
                        if data != '[DONE]':
                            try:
                                json_data = json.loads(data)
                                if 'choices' in json_data and len(json_data['choices']) > 0:
                                    delta = json_data['choices'][0].get('delta', {})
                                    if 'content' in delta:
                                        print(delta['content'], end='', flush=True)
                            except json.JSONDecodeError:
                                pass
            print("\n")  # Nova linha no final
        else:
            print(f"Erro na requisição de streaming: {response.status_code}")
            print("Detalhes:", response.text)
    except Exception as e:
        print(f"Erro ao conectar à API de streaming: {str(e)}")

if __name__ == "__main__":
    print("Testando API FastAPI com LangGraph...")
    
    # Testa com o provedor padrão
    test_chat_completion()
    test_streaming()
    
    # Testa com diferentes parâmetros de temperatura e top_p
    print("\n" + "="*50)
    print("Testando com temperatura alta...")
    test_chat_completion(temperature=0.9, top_p=0.9)
    
    print("\n" + "="*50)
    print("Testando com temperatura baixa...")
    test_chat_completion(temperature=0.1, top_p=0.1)
    
    # Testa com max_tokens limitado
    print("\n" + "="*50)
    print("Testando com max_tokens limitado...")
    test_chat_completion(max_tokens=50)
    
    # Testa com OpenRouter
    print("\n" + "="*50)
    print("Testando com OpenRouter...")
    test_chat_completion("openrouter")
    test_streaming("openrouter")
    
    # Testa com Anthropic
    print("\n" + "="*50)
    print("Testando com Anthropic...")
    test_chat_completion("anthropic")
    test_streaming("anthropic")