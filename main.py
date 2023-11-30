import re
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer

class BookAnalysis():
    def __init__(self):
        self.ebook = input("Write down the path to a text file:")
        if self.ebook == "":
            self.ebook = "resources/miracle_in_the_andes.txt"
        else:
            self.ebook
        with open (self.ebook, "r") as file:
            book = file.read()
        self.active = True


    #Extract number of chapters
    def chapters_number(self):
        chapter_pattern = re.compile("Chapter [0-9]+")
        result = re.findall(chapter_pattern, book)
        len(result)
        print(f"there is {len(result)} chapters in this book.")

    #Extract sentence where a specific word appears
    def words_times(self):
        word = input("Pick the word you want to know how many times it appears: ")
        word_pattern = re.compile(fr"[A-Z]{{1}}[^.]*[^a-zA-Z]+{word}[^a-zA-Z]+[^.]*.")
        result = re.findall(word_pattern, book)

    #Identify the most commonly used words in the book and put them in an ordered list
    def most_used_words(self):
        pattern = re.compile("[a-zA-Z]+")
        result = re.findall(pattern, book.lower())

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
        analyzer = SentimentIntensityAnalyzer()
        scores = analyzer.polarity_scores("")

        if scores["pos"] > scores["neg"]:
            print ("This chapter has an overall positive tone")
        else:
            print("This chapter's tone is not so uplifting")

        analyzer.polarity_scores(book)

    #Analyzing each chapter's tone
    def chapters_analysis(self):
        chapter_pattern = re.compile("Chapter [0-9]+")
        chapters = re.split(chapter_pattern, book)
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
