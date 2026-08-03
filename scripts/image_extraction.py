# https://github.com/ollama/ollama-python

import os
import sys
from ollama import generate
from ollama import GenerateResponse
from config import EXTRACT_MODEL

prompt = """\
Extract all the unique vocabulary words from the attached image and output as a list of words, one per line.
Please follow these rules:

1. Look for Ukrainian words. Ignore all other languages.
2. Use basic dictionary forms: If a word is changed because of grammar (like plural nouns or past tense verbs), change it back to its simplest root form. Use the singular form for nouns, the masculine singular form for adjectives, and the basic (infinitive) form for verbs. 
3. Avoid duplicates: Do not repeat words that share the same grammatical root.
4. Skip personal names: Ignore people's names or proper nouns.
5. Do not write introductory text, explanations, or full sentences.
"""

def extract_vocabulary_from_image(img_path: str) -> str:
    response: GenerateResponse = generate(
        model=EXTRACT_MODEL, 
        prompt=prompt,
        images=[img_path],
        think=False,
        stream=False,
        options={
            'temperature': 0,
            'seed': 42
        }
    )

    return response.response

def extract_vocabulary_from_folder(folder_path: str) -> str | None:
    # Supported image formats
    image_extensions = ('.png', '.jpg', '.jpeg', '.webp')
    
    # Collect all image files from the folder
    image_paths = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(image_extensions):
            img = os.path.join(folder_path, filename)
            image_paths.append(img)

    if not image_paths:
        print(f"No images found in the folder: {folder_path}")
        return None

    output = ""

    for img_path in image_paths:
        output += extract_vocabulary_from_image(img_path)

    return output

if __name__ == "__main__":
    # Ensure a folder path argument was provided
    if len(sys.argv) < 2:
        print("Usage: python script.py <path_to_image_folder>")
        sys.exit(1)
        
    target_folder = sys.argv[1]
    
    if not os.path.isdir(target_folder):
        print(f"Error: {target_folder} is not a valid directory.")
        sys.exit(1)
        
    csv_output = extract_vocabulary_from_folder(target_folder)
    if csv_output:
        print(csv_output)