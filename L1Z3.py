import nltk
import unicodedata
from keras.preprocessing.text import text_to_word_sequence

def strip_from_punctation(s):
    result = []
    punctations = ["Pc", "Pd", "Ps", "Pe", "Pi", "Pf", "Po"]
    start_index = 0
    if len(s) == 0:
        return result
    if len(s) == 1:
        return [s]
    if unicodedata.category(s[0]) in punctations:
        result.append(s[0])
        start_index = 0
    if unicodedata.category(s[0]) in punctations:
        result.append(s[start_index:-1])
        result.append(s[-1])
    else:
        result.append(s[start_index:])
    return result

with open("Dane/cytaty.txt", "r") as infile:
    for line in infile:
        our_tokens = [token for s in line.split(" ") for token in strip_from_punctation(s)]
        nltk_tokens = nltk.word_tokenize(line)
        keras_tokens = text_to_word_sequence(line)
        l1 = len(our_tokens)
        l2 = len(nltk_tokens)
        if l1 > l2:
            nltk_tokens += [""] * (l1 - l2)
        if l2 > l1:
            our_tokens += [""] * (l2 - l1)
        print(f"Ours: {our_tokens}")
        print(f"Keras: {keras_tokens}")
        print(f"NLTK: {nltk_tokens}")
        for t1, t2 in zip(our_tokens, nltk_tokens):
            if t1 != t2:
                print(f"{t1} != {t2}")