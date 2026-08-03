import argparse
from pathlib import Path

from generate_example import generate_example
from image_extraction import extract_vocabulary_from_folder
from translate import translate
from config import SOURCE_LANG, TARGET_LANG


def build_vocab(folder_path: str) -> None:
  output = extract_vocabulary_from_folder(folder_path)
  words = set()

  for word in output.split('\n'):
    if word not in words:
      words.add(word)

      example = generate_example(word)
      translation = translate(SOURCE_LANG, TARGET_LANG, example)
      print(f"{word} | {example} | {translation}")

if __name__ == "__main__":
  # Set up the parser
  parser = argparse.ArgumentParser(description="Process a command line file path.")
  parser.add_argument("target_path", type=Path, help="The path a directory to check")

  # Parse the arguments
  args = parser.parse_args()

  # Access your path object directly
  input_path = args.target_path

  if input_path.is_dir():
    build_vocab(str(input_path))