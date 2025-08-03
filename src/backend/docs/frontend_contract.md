# Contrato Front-end: Seleção de Agente e Ferramentas

Este documento descreve os endpoints e estruturas de request/response para integração do front-end com o back-end de agentes e ferramentas.

## Endpoints de Agentes

### Listar Agentes  
**GET** `/v1/agents`

**Response**: `200 OK`  
```json
[
  {
    "uuid": "string",
    "name": "string",
    "description": "string|null",
    "prompt": "string|null",
    "image": "string|null",
    "created_at": "ISO 8601 datetime",
    "updated_at": "ISO 8601 datetime"
  }
]
```

### Obter Agente  
**GET** `/v1/agents/{agent_uuid}`

**Response**: `200 OK`  
```json
{
  "uuid": "string",
  "name": "string",
  "description": "string|null",
  "prompt": "string|null",
  "image": "string|null",
  "created_at": "ISO 8601 datetime",
  "updated_at": "ISO 8601 datetime"
}
```

## Endpoints de Conversas

### Criar Conversa  
**POST** `/v1/conversations`

**Request Body**:  
```json
{
  "agent_uuid": "string|null",
  "tools_enabled": ["string", ...]
}
```
- `agent_uuid`: UUID do agente selecionado, ou `null` para usar o padrão `bunny`.  
- `tools_enabled`: Lista de nomes de ferramentas habilitadas (opcional). Se omitido, serão usadas as ferramentas padrão do agente.

**Response**: `200 OK`  
```json
{
  "thread_uuid": "string"
}
```

### Enviar Mensagem  
**POST** `/v1/conversations/{thread_uuid}/messages`

**Request Body**: Mesma estrutura de [`ChatCompletionRequest`](app/models/openai.py:29)  
```json
{
  "model": "string",
  "messages": [
    {
      "role": "system|user|assistant|tool",
      "content": "string",
      "function_call": { "name": "string", "arguments": "string" }
    },
    ...
  ],
  "functions": [
    {
      "name": "string",
      "description": "string|null",
      "parameters": { /* JSON Schema */ }
    },
    ...
  ],
  "function_call": "auto|{name}"
}
```
- `functions`: Definições de função geradas dinamicamente com base em [`ToolMetadata`](app/services/tools/tool_metadata.py:1)

**Response**: `200 OK`  
Mesma estrutura de [`ChatCompletionResponse`](app/models/openai.py:57)

**Exemplo de FunctionDefinition**:  
```json
{
  "name": "search_web",
  "description": "Realiza buscas na web",
  "parameters": {
    "type": "object",
    "properties": {
      "query": { "type": "string", "description": "Termo de busca" }
    },
    "required": ["query"]
  }
}
```

## Observações
- O endpoint de mensagens injeta automaticamente a lista de funções conforme o agente e as ferramentas habilitadas.  
- O front-end deve apresentar ao usuário a lista de agentes disponível em [`/v1/agents`](docs/frontend_contract.md).  
- A seleção de ferramentas pode ser feita via interface, enviando `tools_enabled`.

## Versionamento  
Este contrato segue a versão de API prefixada em `/v1`.