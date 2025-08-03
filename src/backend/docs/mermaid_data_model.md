classDiagram
    class Agent {
        +string uuid
        +string name
        +string description
        +string prompt
        +string image
        +datetime created_at
        +datetime updated_at
    }
    class Conversation {
        +string thread_uuid
        +string agent_uuid
        +List~string~ tools_enabled
        +JSON messages
        +datetime created_at
        +datetime updated_at
    }
    Agent "1" --> "*" Conversation : conversations