from typing import Dict, List, Optional
from app.services.tools.tool_interface import ITool
from app.services.tools.tool_metadata import ToolMetadata

class ToolRegistry:
    """
    Registry for tools: holds instances and metadata for each registered tool.
    """
    _tools: Dict[str, ITool] = {}

    @classmethod
    def register(cls, tool: ITool) -> None:
        """
        Register a tool instance. Uses tool.metadata.name as the key.
        """
        metadata: ToolMetadata = tool.metadata
        cls._tools[metadata.name] = tool

    @classmethod
    def get_tool(cls, name: str) -> Optional[ITool]:
        """
        Retrieve a tool instance by name.
        """
        return cls._tools.get(name)

    @classmethod
    def list_tools(cls) -> List[ToolMetadata]:
        """
        List metadata for all registered tools.
        """
        return [tool.metadata for tool in cls._tools.values()]

    @classmethod
    def get_metadata(cls, name: str) -> Optional[ToolMetadata]:
        """
        Get metadata for a specific tool name.
        """
        tool = cls.get_tool(name)
        return tool.metadata if tool else None