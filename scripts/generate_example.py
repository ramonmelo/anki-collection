# https://github.com/ollama/ollama-python

import sys
from textwrap import dedent
from ollama import generate
from ollama import GenerateResponse

def generate_example(text):
  prompt = dedent(f"""\
  Please write one short, simple sentence using the target word provided at the end of this instruction. You must strictly use beginner-level vocabulary (A1 to A2 level) and very basic grammar. Output only the sentence itself, without any extra text, conversational filler, or explanations. The target word is: {text}""")

  response: GenerateResponse = generate(
      model='gemma4:12b', 
      prompt=prompt,
      think=False,
      stream=False
  )

  return response.response

if __name__ == "__main__":
  arguments = sys.argv[1:]
  text = " ".join(arguments)
  print(generate_example(text))