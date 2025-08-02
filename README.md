
# Meu ChatGPT

Minha ideia é criar o meu chatgpt, com as minhas instruções, meus fluxos e minhas ferramentas.

### Como planejo implementar

- Backend Endpoiter com Python e FastAPI.
- Frontend construido com React (TypeScript) e Tailwind CSS.
- Usar LangGraph para fazer a montagem das LLMs.
- Guardar dados de conversas em um banco de dados MongoDB.
- Adotar a Bunny como agente conversador default

### O que quero que tenha nesse meu chatGPT

- Criação de agentes customizados, onde posso definir (com persistencia de dados):
    - Nome do agente
    - Prompt System do agente
    - As ferramentas que o agente poderá ter acesso
    - Modelo de IA padrão e provedor do endpoint
    - Vinculação de uma ou mais bases de conhecimento para um mesmo agente
- Criação de Bases de conhecimento com a possibilidade de usar difentes sistemas de RAG além do RAG tradiciona. Me refiro a usar estrategias de RAG como o Agent RAG, Memory-Augmented RAG, Branching RAG, Corrective RAG, RAG + CoT (Chain-of-Thought), Process-RAG e o Graph RAG.
- Possbilidade de usar Diferentes tipo de aplicação de LangGraph como Agente ou como ferramenta.

### Como o sistema deve se comportar

- Para iniciar uma nova conversa ele terá de clicar em criar uma nova conversa e o usuario poderá definir o Agente utilizado, as bases de conhecimento vinculadas e qual a estrategia de RAG utilizada para a nova conversa.
- Ao criar uma nova conversa é como criar uma nova sessão, tudo o que acontece ali dentro o agente responsavel deve sempre ter acesso.
- Ao indexar um link ou documento, essa referencia subirá para uma RAG com base no que foi escolhido ao iniciar a nova conversa e usando como referencia para acessar a RAG o id da thread.
- Por default todos os agentes deveram escrever a saida em markdown fora de um bloco de codigo markdown pois esse markdown será renderizado.