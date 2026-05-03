# https://github.com/ollama/ollama-python

from ollama import chat
from ollama import ChatResponse
import sys

# en    English
# uk    Ukrainian 

data_len = {
  "en": "English",
  "uk": "Ukrainian"
}

def translate(source, target, text):

  source_len = data_len[source]
  target_len = data_len[target]

  prompt = f"""
  You are a professional {source_len} ({source}) to {target_len} ({target}) translator. 
  Your goal is to accurately convey the meaning and nuances of the original {source_len} text while adhering to {target_len} grammar, vocabulary, and cultural sensitivities. 
  Produce only the {target_len} translation, without any additional explanations or commentary. Please translate the following {source_len} text into {target_len}: {text}"""

  response: ChatResponse = chat(model='translategemma:4b', messages=[
    {
      'role': 'user',
      'content': prompt,
    }],
    think=False)

  return response.message.content

if __name__ == "__main__":
  arguments = sys.argv[1:]
  text = " ".join(arguments)
  print(translate('en', 'uk', text))