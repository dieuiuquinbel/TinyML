import re
with open('de_cuong_extracted.txt', encoding='utf-8') as f:
    text = f.read()

# Split the single long line into readable lines at sentence-ish boundaries
text = text.replace('\r', '\n').replace('\n\n', '\n')
# Insert newlines around common section markers and punctuation
text = re.sub(r'(?<=[.!?])\s+(?=[A-ZÀ-ỸĐ])', '\n', text)
with open('_de_cuong_wrapped.txt', 'w', encoding='utf-8') as f:
    f.write(text)
print("chars:", len(text))
