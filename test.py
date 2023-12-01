from controller import BookAnalysis

book = BookAnalysis()

while book.active:
    user_action = input("\nDo you want to pick a book to analyze? Know the number of chapters? Know how many times a specific word appears? Know the words the most used? Knows a chapter's tone? Knows all chapters tone? \n")
    match user_action.title():
        case 'Pick':
            book.pick_book()
        case 'Chapters':
            book.chapters_number()
        case 'Word':
            book.word_times()
        case 'Used':
            book.most_used_words()
        case 'Chapter':
            book.chapter_analysis()
        case 'Chapters':
            book.chapters_analysis()
        case 'Quit':
            # active = False
            book.quit()
