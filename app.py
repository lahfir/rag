import os
import weaviate
from dotenv import load_dotenv
from llama_index import SimpleDirectoryReader
from llama_index.node_parser import SimpleNodeParser
from llama_index.vector_stores import WeaviateVectorStore
from llama_index import VectorStoreIndex, StorageContext

def query_weaviate():
    try:
        load_dotenv()
        key = os.getenv("OPENAI_API_KEY")

        # load the blogs using the reader
        docs = SimpleDirectoryReader('./files').load_data()

        # chunk up the blog posts into nodes
        parser = SimpleNodeParser.from_defaults(chunk_size=1024, chunk_overlap=20)
        nodes = parser.get_nodes_from_documents(docs)

        try:
            client = weaviate.Client(url="http://localhost:8080")
            print("Connected to Weaviate")
        except Exception as e:
            print(f"Failed to connect to Weaviate: {str(e)}")
            return

        try:
            # construct vector store
            vector_store = WeaviateVectorStore(weaviate_client=client, index_name="DataIndex", text_key="content")

            # setting up the storage for the embeddings
            storage_context = StorageContext.from_defaults(vector_store=vector_store)

            # set up the index
            index = VectorStoreIndex(nodes, storage_context=storage_context)

            query_engine = index.as_query_engine()

            try:
                response = query_engine.query("what is attention?")
                # print(response)
                return response
            except Exception as e:
                print(f"Query execution failed: {str(e)}")
                return None

        except Exception as e:
            print(f"Failed to set up vector store and index: {str(e)}")
            return None

    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return None

# Call the function
query_result = query_weaviate()
print(query_result)
