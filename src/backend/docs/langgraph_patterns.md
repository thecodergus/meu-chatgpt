# Padrões de Código: LangGraph Agentes LLM em Python

Este documento descreve os principais padrões de implementação utilizados no projeto para criar agentes inteligentes baseados em LangGraph.

## 1. GraphManager e ModelFactory  
- **GraphManager** encapsula o fluxo de estados do LangGraph e expõe métodos como `process_messages`.  
  Referência: [`app/services/graph_manager.py:1`](app/services/graph_manager.py:1)  
- **ModelFactory** isola a inicialização do modelo LLM permitindo configurações dinâmicas.  
  Referência: [`app/services/model_factory.py:1`](app/services/model_factory.py:1)  

## 2. Interface de Agente (IAgent)  
Define assinatura comum para todos os agentes:  
- Propriedades `name` e `description`  
- Método `invoke(messages, **kwargs)`  
- Propriedade `tools` retornando lista de nomes de ferramentas  
Referência: [`app/services/agents/agent_interface.py:6`](app/services/agents/agent_interface.py:6)  

## 3. Registro de Agentes (Registry)  
- **AgentRegistry** mantém instâncias de agentes registrados por nome.  
- Métodos: `register(agent)`, `get(name)` e `get_tool_names(name)`.  
Referência: [`app/services/agents/agent_registry.py:7`](app/services/agents/agent_registry.py:7)  

## 4. Ferramentas (Tool Pattern)  
- **ITool** define interface comum para ferramentas com `invoke(params)` e `metadata`.  
  Referência: [`app/services/tools/tool_interface.py:1`](app/services/tools/tool_interface.py:1)  
- **ToolMetadata** encapsula `name`, `description` e `parameters` (esquema JSON).  
  Referência: [`app/services/tools/tool_metadata.py:1`](app/services/tools/tool_metadata.py:1)  
- **AbstractTool** implementa ITool e fornece base para criar novas ferramentas.  
  Referência: [`app/services/tools/abstract_tool.py:1`](app/services/tools/abstract_tool.py:1)  
- **ToolRegistry** armazena instâncias e expõe métodos `list_tools()` e `get_metadata(name)`.  
  Referência: [`app/services/tools/tool_registry.py:1`](app/services/tools/tool_registry.py:1)  

## 5. Definições de Função Dinâmicas  
No endpoint de conversa, montamos `FunctionDefinition` com base em ferramentas habilitadas:  
```python
from ..models.openai import FunctionDefinition
for tool_name in enabled_tool_names:
    metadata = ToolRegistry.get_metadata(tool_name)
    functions.append(FunctionDefinition(
        name=metadata.name,
        description=metadata.description,
        parameters=metadata.parameters
    ))
```
Referência: [`app/api/v1.py:211`](app/api/v1.py:211)  

## 6. Endpoints FastAPI  
- **POST /v1/conversations** aceita `agent_uuid` e `tools_enabled`.  
- **POST /v1/conversations/{thread_uuid}/messages** injeta funções e chama LangGraph via `LangGraphService.process_chat_completion`.  
Referência: [`app/api/v1.py:200`](app/api/v1.py:200)  

## 7. Exemplo de Fluxo  
1. Front-end pede lista de agentes (`GET /v1/agents`).  
2. Usuário seleciona agente e ferramentas (`tools_enabled`).  
3. Cria conversa (`POST /v1/conversations`).  
4. Envia mensagem (`POST /v1/conversations/{thread_uuid}/messages`) com funções geradas dinamicamente.  
5. Resposta do LangGraph retorna JSON compatível com OpenAI.

Estes padrões garantem modularidade, extensibilidade e facilidade de manutenção na criação de agentes LLM com LangGraph.