import os
import string

documents_folder = "documents"

inverted_index = {}

for filename in os.listdir(documents_folder):
    file_path = os.path.join(documents_folder, filename)

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    content_words = content.lower().translate(
        str.maketrans("", "", string.punctuation)
    ).split()

    for word in content_words:
        if word not in inverted_index:
            inverted_index[word] = []

        if filename not in inverted_index[word]:
            inverted_index[word].append(filename)

print(inverted_index)
print(inverted_index["python"])