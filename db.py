import psycopg2
from sqlalchemy import make_url
from llama_index.indices.vector_store import VectorStoreIndex
from llama_index.vector_stores import PGVectorStore

# import logging
# import sys

# Uncomment to see debug logs
# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
# https://docs.llamaindex.ai/en/latest/examples/vector_stores/postgres.html


from llama_index import SimpleDirectoryReader, StorageContext
from llama_index.indices.vector_store import VectorStoreIndex
from llama_index.vector_stores import PGVectorStore
import textwrap
import openai
import os

from dotenv import load_dotenv
load_dotenv() 

key = os.getenv("OPENAI_API_KEY")
openai.api_key = key

documents = SimpleDirectoryReader("files").load_data()
print("Document ID:", documents[0].doc_id)


connection_string = "postgresql://postgres:password@localhost:5432"
db_name = "rag_db"
conn = psycopg2.connect(connection_string)
conn.autocommit = True

with conn.cursor() as c:
    print('connected')
    c.execute(f"DROP DATABASE IF EXISTS {db_name}")
    c.execute(f"CREATE DATABASE {db_name}")
    c.execute("CREATE EXTENSION IF NOT EXISTS vector")

url = make_url(connection_string)
vector_store = PGVectorStore.from_params(
    database=db_name,
    host=url.host,
    password=url.password,
    port=url.port,
    user=url.username,
    table_name="rag_data",
    embed_dim=1536,  # openai embedding dimension
)

storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context, show_progress=True
)
query_engine = index.as_query_engine()

response = query_engine.query("What is attention?")

# docker run -d -p 5432:5432 --name my-postgres -e  POSTGRES_PASSWORD=password postgres