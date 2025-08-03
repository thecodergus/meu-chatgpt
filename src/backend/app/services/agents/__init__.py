"""
Pacote de agentes inteligentes
"""
from .agent_registry import AgentRegistry
from .bunny_agent import BunnyAgent

# Registra o agente default Bunny na importação do pacote
AgentRegistry.register(BunnyAgent())