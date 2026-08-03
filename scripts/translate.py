# https://github.com/ollama/ollama-python

import sys
from textwrap import dedent
from ollama import generate
from ollama import GenerateResponse
from config import TRANSLATE_MODEL, LANGUAGE_NAMES

def translate(source: str, target: str, text: str) -> str:

  source_len = LANGUAGE_NAMES[source]
  target_len = LANGUAGE_NAMES[target]

  prompt = dedent(f"""\
  You are a professional {source_len} ({source}) to {target_len} ({target}) translator. 
  Your goal is to accurately convey the meaning and nuances of the original {source_len} text while adhering to {target_len} grammar, vocabulary, and cultural sensitivities. 
  Produce only the {target_len} translation, without any additional explanations or commentary. Please translate the following {source_len} text into {target_len}: {text}""")

  response: GenerateResponse = generate(
      model=TRANSLATE_MODEL, 
      prompt=prompt,
      think=False,
      stream=False
  )

  return response.response

if __name__ == "__main__":
  arguments = sys.argv[1:]
  text = " ".join(arguments)
  print(translate('en', 'uk', text))