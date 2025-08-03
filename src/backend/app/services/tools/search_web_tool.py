from typing import Dict, Any
from app.services.tools.abstract_tool import AbstractTool
from app.services.tools.tool_metadata import ToolMetadata

class SearchWebTool(AbstractTool):
    """
    Ferramenta de busca na web (stub). Retorna lista vazia de resultados.
    """
    def __init__(self):
        metadata = ToolMetadata(
            name="search_web",
            description="Busca resultados na web para uma consulta",
            parameters_schema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "max_results": {"type": "integer"}
                },
                "required": ["query"]
            }
        )
        super().__init__(metadata)

    async def invoke(self, params: Dict[str, Any]) -> Dict[str, Any]:
        query = params.get("query", "")
        max_results = params.get("max_results", 10)
        # Stub: implementar integração real de pesquisa se necessário
        return {"query": query, "results": [], "max_results": max_results}