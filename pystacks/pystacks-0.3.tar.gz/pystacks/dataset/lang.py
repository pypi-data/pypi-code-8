import numpy as np
# TODO: test this class

def convolve_window(window_size, l):
    if len(l) < window_size:
        return None
    return [l[i:i+window_size] for i, _ in enumerate(l[:-window_size+1])]


class Vocab(object):

    UNK = '**unk**'

    def __init__(self, enable_UNK=True):
        self._word2index = {}
        self._index2word = []
        self._counts = []
        self.enable_UNK = enable_UNK
        if enable_UNK:
            self.add_word(Vocab.UNK, _inc_count=0)
            self.UNK_INDEX = self._word2index[Vocab.UNK] # cache for faster read

    def __len__(self):
        return len(self._index2word)

    def add_word(self, word, _inc_count=1):
        if word not in self._word2index:
            self._word2index[word] = len(self._index2word)
            self._index2word += [word]
            self._counts += [0]
        self._counts[self._word2index[word]] += _inc_count

    def get_word(self, index):
        return self._index2word[index]

    def get_index(self, word):
        return self._word2index.get(word, self.UNK_INDEX) if self.enable_UNK else self._word2index[word]

    def prune_rare_words(self, min_freq=5):
        v = Vocab()
        for word, count in zip(self._index2word, self._counts):
            if count >= min_freq:
                v.add_word(word, _inc_count=count)
        return v

    def sents_to_indices(self, sents, add_word=True, preprocess=None):
        return [self.sent_to_indices(sent, add_word, preprocess) for sent in sents]

    def sent_to_indices(self, sent, add_word=True, preprocess=None):
        if preprocess is not None:
            sent = preprocess(sent)
        if add_word: [self.add_word(w) for w in sent]
        return [self.get_index(w) for w in sent]

    def merge(self, another):
        for word, count in zip(another._index2word, another._counts):
            if word in self._index2word:
                my_index = self._word2index[word]
                self._counts[my_index] += count
            else:
                self.add_word(word, _inc_count=count)