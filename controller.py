import re
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
import sys, pathlib, fitz

class BookAnalysis():
    def __init__(self):
        self.file = ""
        self.active = True

    def pick_book(self):
        self.file = input("Please, specify the path to a book:\n")
        if self.file == "":
            self.file = "resources/miracle_in_the_andes.txt"
        else:
            self.file
        return self.file

    def _read_book(self):
        if ".txt" in self.file:
            try:
                with open (self.file, "r") as file:
                    self.ebook = file.read()
            except FileNotFoundError:
                print("you did not give a book to analyze")
        elif ".pdf" in self.file:
            self.book = fitz.open(self.file)
            with open ("ebook.txt", "wb") as self.ebook:
                for page in self.book:
                    text = page.get_text("text", sort=True).encode("utf8")
                # with open ("ebook.txt", "wb") as self.ebook:
                    self.ebook.write(text)
                    self.ebook.write(bytes((12,)))
        return self.ebook


    #Extract number of chapters
    def chapters_number(self):
        self._read_book()
        # print(type(self.ebook))
        chapter_pattern = re.compile("Chapter [0-9]+")
        result = re.findall(chapter_pattern, self.ebook)
        len(result)
        print(f"there is {len(result)} chapters in this book.")

    #Extract sentence where a specific word appears
    def word_times(self):
        self._read_book()
        word = input("Pick the word you want to know how many times it appears: ")
        word_pattern = re.compile(fr"[A-Z]{{1}}[^.]*[^a-zA-Z]+{word}[^a-zA-Z]+[^.]*.")
        result = re.findall(word_pattern, self.book)

    #Identify the most commonly used words in the book and put them in an ordered list
    def most_used_words(self):
        self._read_book()
        pattern = re.compile("[a-zA-Z]+")
        result = re.findall(pattern, self.book.lower())

        words ={}
        for word in result:
            if word in words.keys():
                words[word] = words[word] + 1
            else:
                words[word] = 1

        words_list = [{value, key} for (key, value) in words.items()]
        # words_list = sorted(words_list, reverse=True)


        english_stopwords = stopwords.words("english")
        # filtered_words = []
        for count, word in words_list:
            if word not in english_stopwords:
                # filtered_words.append((word,count))
                words_list.append((word,count))
        # filtered_words[:10]
        words_list = sorted(words_list, reverse=True)

    #Identifying the tone of a chapter
    def chapter_analysis(self):
        self._read_book()
        analyzer = SentimentIntensityAnalyzer()
        scores = analyzer.polarity_scores("")

        if scores["pos"] > scores["neg"]:
            print ("This chapter has an overall positive tone")
        else:
            print("This chapter's tone is not so uplifting")

        analyzer.polarity_scores(self.book)

    #Analyzing each chapter's tone
    def chapters_analysis(self):
        self._read_book()
        chapter_pattern = re.compile("Chapter [0-9]+")
        chapters = re.split(chapter_pattern, self.book)
        chapters = chapters[1:]

        analyzer = SentimentIntensityAnalyzer()
        scores = analyzer.polarity_scores("")

        for nb, chapter in enumerate(chapters):
            scores = analyzer.polarity_scores(chapter)
            # print(scores)
            if scores["pos"] > scores["neg"]:
                print (f"Chapter {nb} has an overall positive tone")
            else:
                print(f"Chapter {nb} tone is not so uplifting")

    def quit(self):
        self.active = False
