from abc import ABC
from typing import Dict, Any
from app.services.tools.tool_interface import ITool
from app.services.tools.tool_metadata import ToolMetadata

class AbstractTool(ITool, ABC):
    """
    Classe base para ferramentas. Implementa ITool e armazena metadados.
    """
    def __init__(self, metadata: ToolMetadata):
        self._metadata = metadata

    @property
    def metadata(self) -> ToolMetadata:
        return self._metadata

    async def invoke(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Invoca a ferramenta com parâmetros e retorna o resultado.
        Deve ser sobrescrito pelas subclasses.
        """
        raise NotImplementedError("Método invoke deve ser implementado pela ferramenta concreta")