stop_file = "nepali_stopwords.txt"
stop_words = []
with open(stop_file, encoding='utf-8') as fp:
    lines = fp.readlines()
    stop_words =list( map(lambda x:x.strip(), lines))



punctuation_file = "nepali_punctuation.txt"
punctuation_words = []
with open(punctuation_file, encoding='utf-8') as fp:
    lines = fp.readlines()
    punctuation_words =list( map(lambda x:x.strip(), lines))
punctuation_words


#Preprocessin main function
from snowballstemmer import NepaliStemmer

def preprocess_text(cat_data, stop_words, punctuation_words):
    if isinstance(cat_data, list):
        # If the input is a list, join the elements into a single string
        cat_data = ' '.join(cat_data)
    
    stemmer = NepaliStemmer()  # initialize the Nepali stemmer
    new_cat = []
    noise = "1,2,3,4,5,6,7,8,9,0,०,१,२,३,४,५,६,७,८,९".split(",")

    words = cat_data.strip().split(" ")
    nwords = ""

    for word in words:
        # apply Nepali stemming to the word
        if word not in punctuation_words and word not in stop_words:
            word = stemmer.stemWord(word)

            is_noise = False
            for n in noise:
                if n in word:
                    is_noise = True
                    break
            if not is_noise and len(word) > 1:
                word = word.replace("(", "")
                word = word.replace(")", "")
                nwords += word + " "

    new_cat.append(nwords.strip())

    return new_cat
print(preprocess_text([" संघ खारेजीले अन्योल र अनिश्चितता मात्रै"],stop_words, punctuation_words))
