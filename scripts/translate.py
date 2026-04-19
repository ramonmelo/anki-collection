# https://github.com/ollama/ollama-python

from ollama import chat
from ollama import ChatResponse

# en    English
# uk    Ukrainian 

response: ChatResponse = chat(model='translategemma:4b', messages=[
  {
    'role': 'user',
    'content': """
    You are a professional English (en) to Ukrainian (uk) translator. 
    Your goal is to accurately convey the meaning and nuances of the original English text while adhering to Ukrainian grammar, vocabulary, and cultural sensitivities. 
    Produce only the Ukrainian translation, without any additional explanations or commentary. Please translate the following English text into Ukrainian: Hello, how are you doing today?""",
  }
])
print(response['message']['content'])
# or access fields directly from the response object
print(response.message.content)