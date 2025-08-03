from abc import ABC, abstractmethod
from typing import Dict, Any
from app.services.tools.tool_metadata import ToolMetadata

class ITool(ABC):
    @property
    @abstractmethod
    def metadata(self) -> ToolMetadata:
        """Metadata da ferramenta"""
        pass

    @abstractmethod
    async def invoke(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Invoca a ferramenta com os parâmetros fornecidos e retorna um dict com resultados"""
        pass