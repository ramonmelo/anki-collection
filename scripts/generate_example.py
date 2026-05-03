# https://github.com/ollama/ollama-python

from ollama import chat
from ollama import ChatResponse
import sys

def generate_example(text):
  prompt = f"""
  Please write one short, simple sentence using the target word provided at the end of this instruction. You must strictly use beginner-level vocabulary (A1 to A2 level) and very basic grammar. Output only the sentence itself, without any extra text, conversational filler, or explanations. The target word is: {text}"""

  response: ChatResponse = chat(model='gemma4:latest', messages=[
    {
      'role': 'user',
      'content': prompt,
    }],
    think=False)

  return response.message.content

if __name__ == "__main__":
  arguments = sys.argv[1:]
  text = " ".join(arguments)
  print(generate_example(text))