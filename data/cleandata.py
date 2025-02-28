with open("speeches_text.txt", "r", encoding="utf8") as f:
    text = f.read()

text = text.replace(".", " . ")
text = text.replace("?", " ? ")
text = text.replace("!", " ! ")

words = text.lower().split()

output = " ".join(words)

with open("dataset.txt", "w") as f:
    f.write(output)