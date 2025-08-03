sequenceDiagram
    participant FE as Front-end
    participant API as Back-end API
    participant CS as ConversationService
    participant AR as AgentRegistry
    participant TR as ToolRegistry
    participant LG as LangGraphService

    FE->>API: GET /v1/agents
    API->>AgentService: list_agents(session)
    AgentService-->>API: lista de AgentResponse
    API-->>FE: retorna lista de agentes

    FE->>API: POST /v1/conversations { agent_uuid, tools_enabled }
    API->>CS: create_conversation(session, agent_uuid, tools_enabled)
    CS-->>API: Conversation (thread_uuid, agent_uuid, tools_enabled, messages)
    API-->>FE: CreateConversationResponse { thread_uuid }

    FE->>API: POST /v1/conversations/{thread_uuid}/messages { model, messages }
    API->>CS: append_message(session, thread_uuid, "user", content)
    CS-->>API: Conversation com histórico atualizado
    API->>AgentService: get_agent(session, agent_uuid)
    AgentService-->>API: Agent model
    API->>AR: get(agent_model.name)
    AR-->>API: IAgent instance
    API->>TR: get_metadata(tool_name) para cada ferramenta habilitada
    TR-->>API: ToolMetadata
    API->>LG: process_chat_completion(messages, model, provider, temp, top_p, max_tokens, functions, function_call)
    LG-->>API: resposta do LLM
    API->>CS: append_message(session, thread_uuid, "assistant", response_content)
    CS-->>API: Conversation finalizada
    API-->>FE: ChatCompletionResponse { id, choices, usage }