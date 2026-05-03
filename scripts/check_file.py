
import sys

def check_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines):
        if line.startswith('#'):
            continue
        if not line.strip():
            continue
            
        parts = line.split('\t')
        if len(parts) != 8:
            print(f"Line {i+1}: Wrong column count ({len(parts)}). Expected 8.")
            print(f"Content: {repr(line)}")
        
        # Check for missing translation (Col 2)
        if not parts[1].strip():
            print(f"Line {i+1}: Missing translation in Column 2.")
            print(f"Vocab: {parts[0]}")
            
        # Check for empty example or tags
        if len(parts) >= 5 and not parts[4].strip():
            print(f"Line {i+1}: Missing example phrase in Column 5.")
        if len(parts) >= 6 and not parts[5].strip():
            print(f"Line {i+1}: Missing example translation in Column 6.")
        if len(parts) >= 8 and not parts[7].strip():
            print(f"Line {i+1}: Missing tags in Column 8.")