from nltk.stem import LancasterStemmer
import nltk
stem = LancasterStemmer()
a = "we are subscribers"
s =nltk.word_tokenize(a)

for ss in s:
    print(ss)
