import numpy as np
from collections import defaultdict as dd
from typing import List, Dict, Set
import nltk

class IndexSearch:

    def _to_lemma_mapping(self,) -> Dict[str, str]:
        all_lemmas = {}
        for line in open('Dane/polimorfologik-2.1.txt', encoding='utf-8'):
            L = line.split(';')[:2]
            if L[1].lower() not in all_lemmas or L[0].lower() == L[1].lower():
                all_lemmas[L[1].lower()] = L[0].lower()
        return all_lemmas

    def _load_quotes(self) -> List[List[str]]:
        result = []
        with open("Dane/tokenized_quotes.txt", encoding='utf-8') as f:
            for line in f:
                result.append(nltk.word_tokenize(line))
                # result.append(line.split(" "))
        return result
    
    def _to_lemmas(self, words):
        result = []
        for w in words:
            if w in self.lemma_mapping:
                result.append(self.lemma_mapping[w])
            else:
                result.append(w)
        return result
    

    def _get_reverse_index(self, lemmas_dict, quotes):
        result = dd(lambda:set())
        for i, quote in enumerate(quotes):
            for word in quote:
                word = word.lower()
                if word in lemmas_dict:
                    lemma = lemmas_dict[word]
                    result[lemma].add(i)
                else:
                    result[word].add(i)
        return result

    def __init__(self) -> None:
        print("Loading quotes")
        self.quotes = self._load_quotes()
        print("Quotes loaded")
        print("Creating lemmas mapping")
        self.lemma_mapping = self._to_lemma_mapping()
        # print(self.lemma_mapping)
        # print("Lemmas mapping created")
        # print(self.lemma_mapping)
        print("Creating reverse index")
        self.reverse_index = self._get_reverse_index(self.lemma_mapping, self.quotes)
        # print(self.reverse_index)
        print("Reverse index created")
        # print(self.reverse_index)
        

    def query(self, words: str) -> Set[int]:
        if words[-1] == "\n":
            words = words[:-1]
        splitted_words = self._to_lemmas(nltk.word_tokenize(words))
        
        # print(splitted_words)
        result = self.reverse_index[splitted_words[0]].copy()
        # print(result)
        for word in splitted_words:
            result &= self.reverse_index[word]
            # print(result)
        return result

    def highlight(self, words):
        indices = self.query(words)
        words = self._to_lemmas(nltk.word_tokenize(words))
        # print(indices)
        for i in indices:
            quote = self.quotes[i]
            for word in quote:
                if word in self.lemma_mapping and self.lemma_mapping[word] in words:
                    print(f"[{word}]", end=" ")
                else:
                    print(word, end=" ")
            print("\n")
    
    def group(self, lines):
        result = dd(lambda:set())
        for i, line in enumerate(lines):
            query_result = frozenset(self.query(line))
            # print(query_result)
            result[query_result].add(i)
            # for j in query_result:
            #     result[j].add(i)
        for _, v in result.items():
            for i in v:
                print(lines[i][:-1])
            print()

indexSearch = IndexSearch()

def mainA():
    indexSearch.highlight("dziewczynka z zapałkami")

def mainB():
    with open("Dane/przypadkowe_trigramy.txt", "r", encoding='utf-8') as f:
        indexSearch.group([line for line in f])

if __name__ == "__main__":
    # print(indexSearch.reverse_index["dla"])
    mainA()
    mainB()