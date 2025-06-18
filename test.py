def open_existing_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        print(f"Loaded file: {filepath}")
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        content = None
    except Exception as e:
        print(f"Error loading file {filepath}: {e}")
        content = None


open_existing_file("transcripts/20250605_211200_recording.txt")
print(content[:300])  # preview first 300 chars