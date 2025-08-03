from langgraph.graph import StateGraph, MessagesState, START
from langgraph.checkpoint.memory import InMemorySaver
import uuid

class GraphManager:
    """Gerenciador de grafos LangGraph"""
    
    def __init__(self):
        self.graph = self._create_graph()
    
    def _create_graph(self):
        """Cria o grafo LangGraph para processamento"""
        # Cria o grafo
        builder = StateGraph(MessagesState)
        
        # Adiciona o nó que chama o modelo
        builder.add_node("llm", self._call_model)
        
        # Define a conexão entre os nós
        builder.add_edge(START, "llm")
        
        # Compila o grafo com persistência em memória
        checkpointer = InMemorySaver()
        return builder.compile(checkpointer=checkpointer)
    
    def _call_model(self, state: MessagesState):
        """Chama o modelo de linguagem com o estado atual"""
        # Converte as mensagens para o formato esperado pelo modelo
        messages = state["messages"]
        
        # Chama o modelo
        response = self.model.invoke(messages)
        
        # Retorna a resposta
        return {"messages": response}
    
    def process_messages(self, model, messages):
        """Processa mensagens usando o grafo LangGraph"""
        # Salva o modelo como atributo da instância
        self.model = model
        
        # Cria uma configuração única para esta execução
        config = {"configurable": {"thread_id": str(uuid.uuid4())}}
        
        # Invoca o grafo
        response = self.graph.invoke({"messages": messages}, config=config)
        return response
        
        # Retorna a resposta
    def stream_messages(self, model, messages):
        """Processa mensagens usando o grafo LangGraph com streaming"""
        # Salva o modelo como atributo da instância
        self.model = model

        # Cria uma configuração única para esta execução
        config = {"configurable": {"thread_id": str(uuid.uuid4())}}

        # Invoca o grafo com streaming
        response = self.graph.stream({"messages": messages}, config=config)

        # Retorna o gerador de streaming
        return response