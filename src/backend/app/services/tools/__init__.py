from .tool_registry import ToolRegistry
from .search_web_tool import SearchWebTool

# Registra ferramentas padrão
ToolRegistry.register(SearchWebTool())