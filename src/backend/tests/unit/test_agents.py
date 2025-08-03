import pytest
from app.services.agents.bunny_agent import BunnyAgent
from app.services.agents.agent_registry import AgentRegistry

def test_bunny_agent_tools_list():
    bunny = BunnyAgent()
    # Registra agent para teste
    AgentRegistry.register(bunny)
    assert bunny.name == "bunny"
    tools = bunny.tools
    assert isinstance(tools, list)
    # Verifica que todos os nomes de ferramenta são strings
    assert all(isinstance(t, str) for t in tools)

def test_agent_registry_get_tool_names():
    bunny = BunnyAgent()
    AgentRegistry.register(bunny)
    names = AgentRegistry.get_tool_names("bunny")
    assert names == bunny.tools