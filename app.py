import os
import weaviate
from dotenv import load_dotenv
load_dotenv() 
key = os.getenv("OPENAI_API_KEY")
# pip install --pre -U "weaviate-client==4.*"
# connect to your weaviate instance
try:
    client = weaviate.Client(url="http://localhost:8080", additional_headers={ 'X-OpenAI-Api-Key': key})
    print("connected")
except Exception as e:
    print(str(e))



# https://weaviate.io/developers/weaviate/tutorials/connect