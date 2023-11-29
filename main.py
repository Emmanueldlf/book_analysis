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

#Extract the 5 most commonly used words in the book
pattern = re.compile("[a-zA-Z]+")
result = re.findall(pattern, book.lower())
result[:5]

words ={}
for word in result:
    if word in words.keys():
        words[word] = words[word] + 1
    else:
        words[word] = 1

words_list = [{value, key} for (key, value) in words.items()]
sorted(words_list, reverse=True)
print(sorted(words_list)[:5])
