from pymongo import MongoClient
import os

def create_ttl_index():
    """
    Cria índice TTL em conversations.createdAt com expiração de 7 dias.
    """
    mongo_uri = os.getenv("DATABASE_URL")
    if not mongo_uri:
        raise ValueError("DATABASE_URL não encontrada")
    client = MongoClient(mongo_uri)
    # Obtém o nome do banco de forma segura, usando env ou padrão do URI
    db_name = os.getenv("DATABASE_NAME", client.get_default_database().name)
    db = client[db_name]
    conversations = db["conversations"]
    # Cria índice TTL em createdAt (604800 segundos = 7 dias)
    conversations.create_index([("createdAt", 1)], expireAfterSeconds=604800)
    print("Índice TTL criado em conversations.createdAt expirando após 604800 segundos")

if __name__ == "__main__":
    create_ttl_index()