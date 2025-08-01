from typing import List, Dict
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

class MessageConverter:
    """Conversor de mensagens entre diferentes formatos"""
    
    @staticmethod
    def convert_to_langchain_messages(messages: List[Dict[str, str]]):
        """Converte mensagens do formato da API para o formato do LangChain"""
        langchain_messages = []
        for msg in messages:
            if msg["role"] == "system":
                langchain_messages.append(SystemMessage(content=msg["content"]))
            elif msg["role"] == "user":
                langchain_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                langchain_messages.append(AIMessage(content=msg["content"]))
        return langchain_messages
    
    @staticmethod
    def extract_assistant_response(response_messages):
        """Extrai a última mensagem do assistente da resposta"""
        assistant_messages = [msg for msg in response_messages if isinstance(msg, AIMessage)]
        if assistant_messages:
            return assistant_messages[-1].content
        else:
            return "Desculpe, não consegui gerar uma resposta."