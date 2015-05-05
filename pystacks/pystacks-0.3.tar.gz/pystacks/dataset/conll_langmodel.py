from pystacks.dataset.dataset import Dataset
from pystacks.dataset.lang import Vocab, convolve_window
import numpy as np

class Conll2000LangModel(Dataset):

    @classmethod
    def get_windows(cls, window_size, sent, vocab, preprocess):
        windows = []
        words = vocab.sent_to_indices(sent, False, preprocess)
        return convolve_window(window_size, words)

    @classmethod
    def get_data(cls, sents_and_tags, word_vocab, preprocess, window_size):
        x = []
        for sent in sents_and_tags:
            word_indices = word_vocab.sent_to_indices(sent, False, preprocess)
            word_indices = cls.get_windows(window_size, sent, word_vocab, preprocess)
            x += word_indices
        return np.array(x, dtype='int32')

    @classmethod
    def add_time_domain(cls, X, Y):
        # X[0, :] contains the indices for the first example
        # X[1, :] contains the indices for the second example
        # we want the first dimension (0) to be time, but right now it's the example index
        X = X.T # we'll rotate it such that the first dimension is time
        # the next dimension (1) is the example indices, but right now it is a flattened list of indices for all examples, we'll add in a dummy dimension such that X[0, 1, :] contains the features for the second example in the first time step
        X = X.reshape(list(X.shape) + [-1])
        return X, Y

    @classmethod
    def make_data(cls, window_size=3, min_freq=2):
        from nltk.corpus import conll2000
        test_sents = conll2000.sents('test.txt')
        train_sents = conll2000.sents('train.txt')

        num_train = int(len(train_sents) * 0.7)
        dev_sents = train_sents[num_train:]
        train_sents = train_sents[:num_train]

        print 'loaded', len(train_sents), 'training', len(dev_sents), 'dev', len(test_sents), 'test sentences'

        word_vocab = Vocab()

        START = '**start**'
        END = '**end**'
        pad = window_size/2
        preprocess = lambda sent: [START]*pad + [w.lower() for w in sent] + [END]*pad

        print 'collecting vocabulary'
        for sent in train_sents:
            word_indices = word_vocab.sent_to_indices(sent, True, preprocess)
        print len(word_vocab), 'unique words'

        print 'pruning vocab'
        word_vocab = word_vocab.prune_rare_words(min_freq)
        print len(word_vocab), 'unique words'

        print 'converting data to indices'
        training_data = cls.get_data(train_sents, word_vocab, preprocess, window_size)
        dev_data = cls.get_data(dev_sents, word_vocab, preprocess, window_size)
        test_data = cls.get_data(test_sents, word_vocab, preprocess, window_size)

        return {
            'word_vocab': word_vocab,
            'train': cls.add_time_domain(training_data[:, :-1], training_data[:, -1]),
            'dev': cls.add_time_domain(dev_data[:, :-1], dev_data[:, -1]),
            'test': cls.add_time_domain(test_data[:, :-1], test_data[:, -1]),
        }


if __name__ == '__main__':
    Conll2000LangModel.make_data(window_size=5, min_freq=2)
