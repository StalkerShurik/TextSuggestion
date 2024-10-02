import numpy as np
from tqdm import tqdm
from typing import List

class PrefixTreeNode:
    def __init__(self):
        self.children: dict[str, PrefixTreeNode] = {}
        self.is_end_of_word = False

    def get_all_words(self, prefix, all_words):
        for sym, next_node in self.children.items():
            next_node.get_all_words(prefix + sym, all_words)

        if self.is_end_of_word:
            all_words.append(prefix)

    def add_word(self, word, i):
        if i == len(word):
            self.is_end_of_word = True
        else: 
            if word[i] not in self.children.keys():
                self.children[word[i]] = PrefixTreeNode()
            
            self.children[word[i]].add_word(word, i+1)

class PrefixTree:
    def __init__(self, vocabulary: List[str]):

        self.root = PrefixTreeNode()
        
        for word in vocabulary:
            self.root.add_word(word, 0)

    def search_prefix(self, prefix) -> List[str]:

        cur_node = self.root

        for sym in prefix:
            if sym not in cur_node.children.keys():
                return []
            cur_node = cur_node.children[sym]

        all_words = []
        cur_node.get_all_words(prefix, all_words)

        return all_words
    

class WordCompletor:
    def __init__(self, corpus):
        
        self.vocab: dict[str, float] = {}
        self.corpus_size = 0 

        for text in tqdm(corpus):
            self.corpus_size += len(text)
            for word in text:
                if word in self.vocab.keys():
                    self.vocab[word] += 1
                else:
                    self.vocab[word] = 1

        for key in self.vocab:
            self.vocab[key] /= self.corpus_size

        self.prefix_tree = PrefixTree(self.vocab.keys())

    def get_words_and_probs(self, prefix: str) -> (List[str], List[float]):
        words, probs = [], []

        words = self.prefix_tree.search_prefix(prefix)

        for word in words:
            probs.append(self.vocab[word])

        return (words, probs)

class NgramNode:
    def __init__(self):
        self.children: dict[str, PrefixTreeNode] = {}
        self.end_of_n_gramm = 0

    def add_n_gramm(self, n_gramm, i):
        if i == len(n_gramm):
            self.end_of_n_gramm += 1
        else: 
            if n_gramm[i] not in self.children.keys():
                self.children[n_gramm[i]] = NgramNode()
            self.children[n_gramm[i]].add_n_gramm(n_gramm, i+1)

class NGramLanguageModel:
    def __init__(self, corpus, n):

        self.n = n
        self.corpus_size = 0
        self.root = NgramNode()

        for text in corpus:
            self.corpus_size += len(text)
            for i in range(len(text) - n):
                self.root.add_n_gramm(text[i:i+n+1], 0)
                
    def get_next_words_and_probs(self, prefix: list) -> (List[str], List[float]):
        """
        Возвращает список слов, которые могут идти после prefix,
        а так же список вероятностей этих слов
        """

        next_words, probs = [], []
        
        cur_node = self.root

        if len(prefix) < self.n:
           return [], []

        prefix = prefix[-self.n:]

        for i in range(self.n):
            if prefix[i] not in cur_node.children.keys():
                return [], []
            cur_node = cur_node.children[prefix[i]]

        normalize = 0

        for key in cur_node.children:
            next_words.append(key)

            cnt = cur_node.children[key].end_of_n_gramm
            normalize += cnt
            probs.append(cnt)

        for i in range(len(probs)):
            probs[i] /= normalize

        return next_words, probs

class TextSuggestion:
    def __init__(self, word_completor, n_gram_model):
        self.word_completor = word_completor
        self.n_gram_model = n_gram_model

    def suggest_text(self, text: list, n_words=3, n_texts=1) -> list[list[str]]:
        """
        Возвращает возможные варианты продолжения текста (по умолчанию только один)
        
        text: строка или список слов – написанный пользователем текст
        n_words: число слов, кNоторые дописывает n-граммная модель
        n_texts: число возвращаемых продолжений (пока что только одно)
        
        return: list[list[srt]] – список из n_texts списков слов, по 1 + n_words слов в каждом
        Первое слово – это то, которое WordCompletor дополнил до целого.
        """

        suggestions = []

        words, probs = self.word_completor.get_words_and_probs(text[-1])
        
        if len(probs) > 0:
            completed_word = words[np.argmax(np.array(probs))]
        else:
            completed_word = ""

        if completed_word != "":
            suggestions.append(completed_word)
            fixed_prefix = text[:-1]
            fixed_prefix.append(completed_word)

        else:
            suggestions.append("DONT_KNOW_TOKEN")
            fixed_prefix = text

        for i in range(n_words):
            words, probs = self.n_gram_model.get_next_words_and_probs(fixed_prefix[-self.n_gram_model.n:])
            if len(probs) == 0:
                break
            next_word = words[np.argmax(np.array(probs))]
            suggestions.append(next_word)
            fixed_prefix.append(next_word)

        return [suggestions]