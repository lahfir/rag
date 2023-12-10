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