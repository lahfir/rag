import os
import weaviate
from dotenv import load_dotenv
from llama_index import SimpleDirectoryReader, SimpleNodeParser, WeaviateVectorStore, VectorStoreIndex, ChatMemoryBuffer
import openai

class RAGChatbot:
    def __init__(self, openai_api_key,
        index_name, directory='files', engine, weaviate_uri="http://localhost:8080", 
        system_prompt=None):
        self.engine = engine 
        self.key = openai_api_key
        self.weaviate_uri = weaviate_uri
        self.directory = directory
        self.key = os.getenv("OPENAI_API_KEY")
        self.index_name = index_name
        self.system_prompt = system_prompt


    
    def set_prompt_with_context(self, context):
        prompt = f"For the text in <<>> \
        respond using the context in () <<{self.system_prompt}>> ({context}) :"


    def connect_to_vectordb(self):
        docs = SimpleDirectoryReader(self.directory).load_data()
        parser = SimpleNodeParser.from_defaults(chunk_size=1024, chunk_overlap=20)
        nodes = parser.get_nodes_from_documents(docs)
        try:
            client = weaviate.Client(url=self.weaviate_uri)
            print("Connected to Weaviate")
            return client, nodes
        except Exception as e:
            print(f"Failed to connect to Weaviate: {str(e)}")
            return

    def get_query_engine(self, client, nodes):
        try:
            vector_store = WeaviateVectorStore(weaviate_client=client, index_name=self.index_name, text_key="content")
            storage_context = StorageContext.from_defaults(vector_store=vector_store)
            index = VectorStoreIndex(nodes, storage_context=storage_context)
            query_engine = index.as_query_engine()
            return query_engine
        except Exception as e:
            print(str(e))

    def connect_to_chat_engine(self):
        data = SimpleDirectoryReader(input_dir=self.directory).load_data()
        index = VectorStoreIndex.from_documents(data)
        memory = ChatMemoryBuffer.from_defaults(token_limit=1500)
        chat_engine = index.as_chat_engine(chat_mode="context", \
        memory=memory, system_prompt=self.system_prompt)
        return chat_engine

    def get_chat_completion(prompt):        
        response = openai.Completion.create(
            engine=“text-davinci-002”,
            prompt=prompt,
            temperature=0.5,
            max_tokens=50,
            n=1,
            stop=None,
            )

    def chat_loop(self):
        db, nodes = self.connect_to_vectordb()
        query_engine = self.get_query_engine(db, nodes)

        while True:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                print("Chatbot: Goodbye!")
                break
            retrieval_result = vector_database.query(user_input)  # This line seems to be using an undefined variable
            if retrieval_result:
                context = retrieval_result
                result = self.get_chat_completion(context=response)
                print(result)
            else:
                result = self.get_chat_completion(context=response)
            print("Chatbot:", response.choices[0].text)