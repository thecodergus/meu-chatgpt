"""
Registro de agentes inteligentes disponíveis
"""
from typing import Dict, List
from .agent_interface import IAgent

class AgentRegistry:
    _agents: Dict[str, IAgent] = {}

    @classmethod
    def register(cls, agent: IAgent) -> None:
        """Registra instância de agente pelo seu nome"""
        cls._agents[agent.name] = agent

    @classmethod
    def get(cls, name: str) -> IAgent:
        """Retorna instância de agente pelo nome"""
        return cls._agents[name]

    @classmethod
    def list(cls) -> Dict[str, IAgent]:
        """Retorna dicionário nome->instância de todos os agentes registrados"""
        return dict(cls._agents)

    @classmethod
    def get_tool_names(cls, name: str) -> List[str]:
        """
        Retorna lista de nomes das ferramentas habilitadas para o agente especificado
        """
        agent = cls.get(name)
        return agent.tools