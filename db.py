import psycopg2
from sqlalchemy import make_url
from llama_index.indices.vector_store import VectorStoreIndex
from llama_index.vector_stores import PGVectorStore


connection_string = "postgresql://postgres:password@localhost:5432"
db_name = "vector_db"
conn = psycopg2.connect(connection_string)
conn.autocommit = True

with conn.cursor() as c:
    print('connected')
    c.execute(f"DROP DATABASE IF EXISTS {db_name}")
    c.execute(f"CREATE DATABASE {db_name}")

url = make_url(connection_string)
vector_store = PGVectorStore.from_params(
    database=db_name,
    host=url.host,
    password=url.password,
    port=url.port,
    user=url.username,
    table_name="paul_graham_essay",
    embed_dim=1536,  # openai embedding dimension
)


# docker run -d -p 5432:5432 --name my-postgres -e  POSTGRES_PASSWORD=password postgres