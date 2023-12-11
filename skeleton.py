from llama_index import SimpleDirectoryReader, VectorStoreIndex, ChatMemoryBuffer
import openai

class RAGChatbot:
    def __init__(self, directory, openai_api_key):
        self.directory = directory
        # Set up OpenAI API key
        openai.api_key = openai_api_key

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