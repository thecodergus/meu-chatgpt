"""
Interface de agentes inteligentes
"""
from abc import ABC, abstractmethod

class IAgent(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Retorna o nome do agente"""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Descrição do agente"""
        pass

    @abstractmethod
    def invoke(self, messages: list, **kwargs) -> dict:
        """Invoca o agente com lista de mensagens e retorna resposta"""
        pass

    @property
    @abstractmethod
    def tools(self) -> list:
        """Lista de nomes das ferramentas habilitadas para este agente"""
        pass