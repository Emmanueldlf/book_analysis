import re

#Test file
ebook = "resources/miracle_in_the_andes.txt"

# opening the file
with open (ebook, "r") as file:
    book = file.read()
book

#Extract number of chapters
chapter_pattern = re.compile("Chapter [0.9+]")
result = re.findall(chapter_pattern, book)
len(result)

#need to explain that line
re.compile(r'Chapter [0-9]', re.UNICODE)

#Extract sentence where a specific word appears
word = input("Pick the word you want to know how many times it appears: ")
word_pattern = re.compile(fr"[A-Z]{{1}}[^.]*[^a-zA-Z]+{word}[^a-zA-Z]+[^.]*.")
result = re.findall(word_pattern, book)

print(result)
