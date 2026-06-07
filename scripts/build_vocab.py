from generate_example import generate_example
from image_extraction import extract_vocabulary_from_folder
from translate import translate

output = extract_vocabulary_from_folder("/home/ramonmelo/Pictures/Screenshots")

for word in output.split('\n'):
  ex = generate_example(word)
  trans = translate('uk', 'en', ex)
  print(f"{word} | {ex} | {trans}")
