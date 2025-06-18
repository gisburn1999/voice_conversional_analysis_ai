from transformers import pipeline

long_text = "transcripts_prefabricated/before_midnight_generic_version.txt"

long_conversation = []

with open(long_text, 'r') as text:
    for line in text:
        line = line.strip()
        if not line:
            continue
        if line.startswith("SPEAKER 1:"):
            speaker = "A"
            text = line[10:].strip()
        elif line.startswith("SPEAKER 2:"):
            speaker = "B"
            text = line[10:].strip()
        else:
            continue

    long_conversation.append({"speaker": speaker, "text": text})
print(long_conversation)

"""conversation = [
    {'speaker': 'A', 'text': "I'm so annoyed you forgot again."},
    {'speaker': 'B', 'text': "I'm really sorry, it was a busy week."},
    {'speaker': 'A', 'text': "It's always the same!"},
    {'speaker': 'B', 'text': "I promise I'll do better next time."},
    {'speaker': 'A', 'text': "Thanks, I appreciate you saying that."},
]
"""

"""
# Step 2: Setup sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis")

# Step 3: Run sentiment analysis and annotate each utterance
for utterance in conversation:
    sentiment = sentiment_pipeline(utterance['text'])[0]
    utterance['sentiment'] = sentiment['label']
    utterance['score'] = sentiment['score']


# Step 4: Detect conflict and support (basic version)
support_keywords = ['sorry', 'understand', 'thank', 'appreciate', 'here for you', 'support']

for utterance in conversation:
    text = utterance['text'].lower()
    # Tag as conflict if sentiment is NEGATIVE
    utterance['conflict'] = utterance['sentiment'] == "NEGATIVE"
    # Tag as support if any keyword found in text (case-insensitive)
    utterance['support'] = any(word in text for word in support_keywords)

# Step 5: Print the annotated conversation
print("\n=== Conflict & Support Detector ===\n")
for u in conversation:
    tags = []
    if u['conflict']:
        tags.append('CONFLICT ')
    if u['support']:
        tags.append('SUPPORT ')
    tag_text = " | ".join(tags) if tags else ""
    print(f"Speaker {u['speaker']}: {u['text']}")
    print(f"    Sentiment: {u['sentiment']} ({u['score']:.2f}) {tag_text}\n")"""