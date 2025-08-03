from typing import Dict, Any, Optional
from pydantic import BaseModel

class ToolMetadata(BaseModel):
    """
    Modelo de metadados de uma ferramenta.
    Contém nome, descrição e esquema JSON dos parâmetros esperados.
    """
    name: str
    description: Optional[str] = None
    parameters_schema: Dict[str, Any]