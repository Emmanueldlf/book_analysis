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
        # if self.file == "":
        #     self.file = "resources/miracle_in_the_andes.txt"
        # else:
        #     self.file
        return self.file

    def _read_book(self):
        # if ".txt" in self.file:
            # try:
                # with open (self.file, "r") as file:
                    # self.ebook = file.read()
            # except FileNotFoundError:
                # print("you did not give a book to analyze")
        # elif ".pdf" in self.file:
            # self.ebook = fitz.open(self.file)
            # with open ("ebook.txt", "wb") as self.ebook:
                # for page in self.book:
                    # self.ebook = page.get_text("text", sort=True).encode("utf8")
                    # self.ebook.write(text)
                    # self.ebook.write(bytes((12,)))
        try:
            with open (self.file, "r") as file:
                self.ebook = file.read()
            # self.ebook = fitz.open(self.file)

        except UnicodeDecodeError:
            self.ebook = fitz.open(self.file)
            # with open (self.file, "r") as file:
                # self.ebook = file.read()
        except FileNotFoundError:
            print("you did not give a book to analyze")
        return self.ebook

    def _table(self):
        self._read_book()
        self.toc = self.ebook.get_toc()
        chapter_pattern = re.compile("Chapter [0-9]+")
        self.chapters = {}
        for item in self.toc:
            if chapter_pattern.match(item[1]):
                self.chapters[chapter_pattern.match(item[1]).group()] = item[2]
        # print(self.chapters)


    #Extract number of chapters
    def chapters_number(self):
        self._read_book()
        # print(type(self.ebook))
        try:
            chapter_pattern = re.compile("Chapter [0-9]+")
            result = re.findall(chapter_pattern, self.ebook)
        except TypeError:
            # toc = self.ebook.get_toc()
            self._table()
            result = [key for key in self.chapters.keys() if "Chapter" in key]
            # result = [item[0] for item in self.chapters if "Chapter" in item[0]]
            # self.chapters_nb = len(result)
        # print(result)
        self.chapters_nb = len(result)
        print(f"There are {self.chapters_nb} chapters in this book.")

    #Extract sentence where a specific word appears
    def word_times(self):
        self._read_book()
        word = input("Pick the word you want to know how many times it appears: ")
        try:
            word_pattern = re.compile(fr"[A-Z]{{1}}[^.]*[^a-zA-Z]+{word}[^a-zA-Z]+[^.]*.")
            result = re.findall(word_pattern, self.ebook)
        except TypeError:
            result = 0
            for page in self.ebook:
                self.text = self.ebook[page.number]
                # print(self.text)
                result += len(self.text.search_for(f"{word}"))
                # print(result)
        # print(result)
        print(f"{word} appears {result} times")

    #Identify the most commonly used words in the book and put them in an ordered list
    def most_used_words(self):
        self._read_book()
        result = []
        # words ={}
        english_stopwords = stopwords.words("english")
        # print(english_stopwords)
        try:
            pattern = re.compile("[a-zA-Z]+")
            unfiltered_result = re.findall(pattern, self.ebook.lower())
            for word in unfiltered_result:
                if word not in english_stopwords:
                    result.append(word)
        except AttributeError:
            # result = []
            pattern = re.compile("[a-zA-Z]+")
            for page in self.ebook:
                text = self.ebook[page.number]
                page_words = text.get_text("words", sort=True)
                # all_words = [word for word in page_words if pattern.search(word[4])]
                # all_words = [word[4] for word in page_words if pattern.findall(word[4])]
                # for word in all_words:
                #     if word.lower() not in english_stopwords:
                #         result.append(word)
                for word in page_words:
                    if word[4].lower() not in english_stopwords and pattern.findall(word[4]):
                        result.append(word[4])
        # print(result)
        words = {}
        for word in result:
            if word in words.keys():
                words[word] = words[word] + 1
            else:
                words[word] = 1

        words_list = [(value, key) for (key, value) in words.items()]
        # print(words_list)

        # english_stopwords = stopwords.words("english")
        # filtered_words = []
        # for count, word in words_list:
            # if word not in english_stopwords:
                # filtered_words.append((word,count))
                # words_list.append((word,count))
        # filtered_words[:10]
        sorted_list = sorted(words_list, reverse=True)
        print(f"The top five most used words are {sorted_list[:5]}")

    #Identifying the tone of a chapter
    def chapter_analysis(self):
        # self._read_book()
        # analyzer = SentimentIntensityAnalyzer()
        # scores = analyzer.polarity_scores("")
        self.chapter_nb = input("Please, specify the number of the chapter you want to know the tone of:\n")
        analyzer = SentimentIntensityAnalyzer()
        # scores = analyzer.polarity_scores("")

        try:
            self._read_book()
            # chosen_pattern = re.compile(fr"Chapter {self.chapter_nb}")
            # chosen_chapter = re.match(chosen_pattern, self.ebook)
            # chapter_text_pattern = re.compile(fr"(^Chapter {self.chapter_nb}\s+\w+\s+)(.+\s+)(?!Chapter [0-9]+)", re.M)
            # chapter_text_pattern = re.compile(fr"(Chapter {self.chapter_nb} [a-zA-Z0-9_]+)(.+)(?!Chapter [0-9]+)", re.M)
            # chapter_text_pattern = fr"(^Chapter {self.chapter_nb}\s+\w+\s+)(.+\s+)(?!Chapter [0-9]+)"
            chapter_text_pattern = re.compile(fr"(^Chapter {self.chapter_nb})(\s*\w*\s*)*(.*\s*(?!Chapter [{int(self.chapter_nb) + 1}-9]+))*", re.M)
            # (^Chapter [0-9]+)
            chapter_text = re.search(chapter_text_pattern, self.ebook).group()
            # chapters_text = re.split("(^Chapter [0-9]+)", self.ebook, 2)
            # print(chapter_text)
            # analyzer = SentimentIntensityAnalyzer()
            # scores = analyzer.polarity_scores("")
            scores = analyzer.polarity_scores(chapter_text)

            # if scores["pos"] > scores["neg"]:
            #     print ("This chapter has an overall positive tone")
            # else:
            #     print("This chapter's tone is not so uplifting")

            # analyzer.polarity_scores(self.ebook)
        except AttributeError:
            self._table()
            # chapter_pattern = re.compile("Chapter [0-9]+")
            chosen_chapter = f"Chapter {self.chapter_nb}"
            # chapter_start = self.chapters[chosen_chapter]
            next_chapter = f"Chapter {int(self.chapter_nb) + 1}"
            # chapter_end = self.chapters[next_chapter] - 1
            # print(chapter_end)
            # self.chapters = {}
            # for item in self.toc:
            #     if chapter_pattern.match(item[1]):
            #         self.chapters[chapter_pattern.match(item[1]).group()] = item[2]
            chapter_text = []
            for page in self.ebook.pages(start=self.chapters[chosen_chapter], stop=self.chapters[next_chapter] - 1):
                text = self.ebook[page.number]
                page_text = text.get_text("text", sort=True)
                chapter_text.append(page_text)
            chapter_text =  " ".join(chapter_text)
            # print(chapter_text)
            scores = analyzer.polarity_scores(chapter_text)

        print(scores)
        if scores["pos"] > scores["neg"]:
            print ("This chapter has an overall positive tone")
        else:
            print("This chapter's tone is not so uplifting")

        # analyzer.polarity_scores(self.chapter_text)

    #Analyzing each chapter's tone
    def chapters_analysis(self):
        self._read_book()
        analyzer = SentimentIntensityAnalyzer()
        try:
            chapter_pattern = re.compile("Chapter [0-9]+")
            chapters = re.split(chapter_pattern, self.ebook)
            chapters = chapters[1:]
            # print(chapters)

        # scores = analyzer.polarity_scores("")

            for nb, chapter in enumerate(chapters):
                scores = analyzer.polarity_scores(chapter)
                # print(scores)
                if scores["pos"] > scores["neg"]:
                    print (f"Chapter {nb} has an overall positive tone")
                else:
                    print(f"Chapter {nb} tone is not so uplifting")
        except TypeError:
            self._table()
            chapter_text = []
            # print(self.toc)
            # print(self.chapters)
            # print(self.chapters)
            # print(self.chapters['Chapter 1'])
            # print(self.chapters[1])
            # list_chapters = [index, value, self.chapters[value] for index,value in enumerate(self.chapters)]
            # list_chapters = [(key, value) in self.chapters.items()]
            list_chapters = [(key,value) for (key, value) in self.chapters.items()]
            print(list_chapters)
            # next_chapter = next(list_chapters)
            # print(next_chapter[1])
            for chapter in list_chapters:
                # print(chapter[1])
                # print(list_chapters[list_chapters.index(chapter) + 1][1])
                # print(list_chapters[list_chapters.index(chapter) + 1][1] - 1)
                # print(list_chapters.index(chapter))

                # working code begins
                # chapter_pages_nb= [chapter[1], list_chapters[list_chapters.index(chapter) + 1][1]-1]
                # print(chapter_pages_nb)
                # chapter_text = [self.ebook.get_page_text(page) for page in chapter_pages_nb]
                # chapter_text = " ".join(chapter_text)
                # working code ends
                print(chapter[1])
                # print(list_chapters[list_chapters.index(chapter) + 1][1] - 1)
                try:
                    chapter_text = self.ebook.get_page_text(chapter[1]-list_chapters[list_chapters.index(chapter) + 1][1] - 1)
                except IndexError:
                    chapter_text = self.ebook.get_page_text(chapter[1]-self.ebook.page_count)
                # print(chapter_text)
                scores = analyzer.polarity_scores(chapter_text)
                # print(scores)
                if scores["pos"] > scores["neg"]:
                    print (f"{chapter[0].title()} has an overall positive tone")
                else:
                    print(f"{chapter[0].title()} tone is not so uplifting")

            # for page in self.ebook.pages(start=self.chapters[chosen_chapter], stop=self.chapters[next_chapter] - 1):
            #     text = self.ebook[page.number]
            #     page_text = text.get_text("text", sort=True)
            #     chapter_text.append(page_text)
            # chapter_text =  " ".join(chapter_text)


    def quit(self):
        self.active = False
