import os
from dotenv import load_dotenv
from openai import OpenAI
from langchain.utilities import BingSearchAPIWrapper

bing_key = os.getenv("BING_SUBSCRIPTION_KEY")
os.environ["BING_SEARCH_URL"] = "https://api.bing.microsoft.com/v7.0/search"

load_dotenv()
client = OpenAI()
key = os.getenv("OPENAI_API_KEY")

class RAGChatbot:
    def __init__(self, openai_api_key = key,
        index_name="RAG", directory='files', engine="gpt-3.5-turbo", \
        system_prompt="Answer all questions like Jarvis from Iron Man"):

        self.search = BingSearchAPIWrapper(k=1)
        self.engine = engine 
        self.key = openai_api_key
        self.directory = directory
        self.key = openai_api_key
        self.index_name = index_name
        self.system_prompt = system_prompt

    def search_web(self, query):
        val =  self.search.results(query,num_results=1)
        # print(val)
        return val

    def set_prompt_with_context(self, context):
        return f"For the text in <<>> \
        respond using the context in () <<{self.system_prompt}>> ({context}) :"

    def get_chat_completion(self,prompt):        
        response = client.chat.completions.create(
        model=self.engine,
        messages=[
            {"role": "system", "content": f"{self.system_prompt}"},
            {"role": "user", "content": prompt}
        ]
        )
        return response

    def chat_loop(self):
        while True:
            user_input = input("You: ")
            search_result  = self.search_web(user_input)
            if user_input.lower() == "exit":
                print("Chatbot: Goodbye!")
                break
            if search_result:
                result = self.get_chat_completion(str(search_result))
                print("Chatbot: ",result.choices[0].message.content)
            else:
                result = self.get_chat_completion(response)
                print("Chatbot: ",result.choices[0].message.content)

chat = RAGChatbot()
chat.chat_loop()