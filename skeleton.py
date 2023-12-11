import os
import weaviate
from dotenv import load_dotenv
from llama_index import SimpleDirectoryReader
from llama_index.node_parser import SimpleNodeParser
from llama_index.vector_stores import WeaviateVectorStore
from llama_index import VectorStoreIndex, StorageContext
from llama_index import SimpleDirectoryReader, VectorStoreIndex, ChatMemoryBuffer
import openai

class RAGChatbot:
    def __init__(self, directory,openai_api_key, \
                 weaviate_uri="http://localhost:8080", \
                 system_prompt=None \
                 
                 ):
        self.key = os.getenv("OPENAI_API_KEY")
        self.weaviate_uri = weaviate_uri

        self.directory = directory
        # Set up OpenAI API key
        openai.api_key = self.key

    
    def connect_to_weaviate_client(self): 
        key = os.getenv("OPENAI_API_KEY")

        # load the blogs using the reader
        docs = SimpleDirectoryReader('./files').load_data()

        # chunk up the blog posts into nodes
        parser = SimpleNodeParser.from_defaults(chunk_size=1024, chunk_overlap=20)
        nodes = parser.get_nodes_from_documents(docs)

        try:
            client = weaviate.Client(url=self.weaviate_uri)
            print("Connected to Weaviate")
            return client
        except Exception as e:
            print(f"Failed to connect to Weaviate: {str(e)}")
            return

    def get_query_engine(self, client)

        try:
            # construct vector store
            vector_store = WeaviateVectorStore(weaviate_client=client, index_name="DataIndex", text_key="content")

            # setting up the storage for the embeddings
            storage_context = StorageContext.from_defaults(vector_store=vector_store)

            # set up the index
            index = VectorStoreIndex(nodes, storage_context=storage_context)

            query_engine = index.as_query_engine()
            return query_engine
        except Exception as e:
            print(str(e))



    def connect_to_llama_index(self):
        # Connect to LlamaIndex and create a vector store index
        data = SimpleDirectoryReader(input_dir=self.directory).load_data()
        index = VectorStoreIndex.from_documents(data)
        # Configure chat engine from llama_index.memory
        memory = ChatMemoryBuffer.from_defaults(token_limit=1500)
        chat_engine = index.as_chat_engine(
            chat_mode="context",
            memory=memory,
            system_prompt="Your system prompt here"
        )
        return chat_engine

    def chat_loop(self, chat_engine):
        # Chat loop
        while True:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                print("Chatbot: Goodbye!")
                break
            # Query the vector database
            retrieval_result = vector_database.query(user_input)
            if retrieval_result:
                # If context is found, use the retrieval mechanism
                response = retrieval_result
            else:
                # If no context is found, use ChatGPT
                response = chat_engine(user_input)
            print("Chatbot:", response)

    def start_chat(self):
        chat_engine = self.connect_to_llama_index()
        self.chat_loop(chat_engine)