"""
Agente inteligente default Bunny para conversas
"""
from .agent_interface import IAgent
from app.services.graph_manager import GraphManager
from app.services.model_factory import ModelFactory

class BunnyAgent(IAgent):
    def __init__(self):
        self.manager = GraphManager()

    @property
    def name(self) -> str:
        return "bunny"

    @property
    def description(self) -> str:
        return "Agente padrão Bunny utiliza LangGraph para processar conversas via LLM"

    def invoke(self, messages: list, **kwargs) -> dict:
        """Invoca o agente Bunny com mensagens e retorna resposta."""
        model = ModelFactory.initialize_model(**kwargs)
        return self.manager.process_messages(model, messages)

    @property
    def tools(self) -> list:
        """Lista de nomes das ferramentas habilitadas para este agente"""
        from app.services.tools.tool_registry import ToolRegistry
        return [metadata.name for metadata in ToolRegistry.list_tools()]