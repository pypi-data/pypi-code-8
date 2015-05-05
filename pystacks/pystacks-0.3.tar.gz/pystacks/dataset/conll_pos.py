from pystacks.dataset.dataset import Dataset
from pystacks.dataset.lang import Vocab, convolve_window
import numpy as np

class Conll2000POS(Dataset):

    @classmethod
    def get_windows(cls, window_size, sent, vocab, preprocess):
        windows = []
        words = vocab.sent_to_indices(sent, False, preprocess)
        return convolve_window(window_size, words)

    @classmethod
    def get_data(cls, sents_and_tags, word_vocab, tag_vocab, preprocess, window_size):
        x = []
        y = []
        for sent in sents_and_tags:
            words, tags = zip(*sent)
            word_indices = word_vocab.sent_to_indices(words, False, preprocess)
            word_indices = cls.get_windows(window_size, words, word_vocab, preprocess)
            label_indices = tag_vocab.sent_to_indices(tags, False)
            x += word_indices
            y += label_indices
        return np.array(x, dtype='int32'), np.array(y, dtype='int32')

    @classmethod
    def make_data(cls, window_size=3, min_freq=2):
        from nltk.corpus import conll2000
        test_sents = conll2000.tagged_sents('test.txt')
        train_sents = conll2000.tagged_sents('train.txt')

        num_train = int(len(train_sents) * 0.7)
        dev_sents = train_sents[num_train:]
        train_sents = train_sents[:num_train]

        print 'loaded', len(train_sents), 'training', len(dev_sents), 'dev', len(test_sents), 'test sentences'

        word_vocab = Vocab()
        tag_vocab = Vocab(enable_UNK=False)

        START = '**start**'
        END = '**end**'
        pad = window_size/2
        preprocess = lambda sent: [START]*pad + [w.lower() for w in sent] + [END]*pad

        print 'collecting vocabulary'
        for sent in train_sents:
            words, tags = zip(*sent)
            word_indices = word_vocab.sent_to_indices(words, True, preprocess)
            label_indices = tag_vocab.sent_to_indices(tags, True)
        print len(word_vocab), 'unique words'

        print 'pruning vocab'
        word_vocab = word_vocab.prune_rare_words(min_freq)
        print len(word_vocab), 'unique words'

        print 'converting data to indices'
        training_data = cls.get_data(train_sents, word_vocab, tag_vocab, preprocess, window_size)
        dev_data = cls.get_data(dev_sents, word_vocab, tag_vocab, preprocess, window_size)
        test_data = cls.get_data(test_sents, word_vocab, tag_vocab, preprocess, window_size)

        return {
            'word_vocab': word_vocab,
            'tag_vocab': tag_vocab,
            'train': training_data,
            'dev': dev_data,
            'test': test_data,
        }


if __name__ == '__main__':
    Conll2000POS.save_data('connll_pos.pkl', Conll2000POS.make_data(window_size=3, min_freq=2))
