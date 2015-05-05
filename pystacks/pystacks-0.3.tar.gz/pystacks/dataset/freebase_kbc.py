from pystacks.dataset.dataset import Dataset
from pystacks.dataset.lang import Vocab
import numpy as np
import os

class FreebaseKBC(Dataset):

    DATADIR = os.path.join(os.path.dirname(__file__), 'freebase')
    TRAINFILE = os.path.join(DATADIR, 'train.txt')
    TESTFILE = os.path.join(DATADIR, 'test.txt')
    DEVFILE = os.path.join(DATADIR, 'dev.txt')

    @classmethod
    def load_triplets(cls, filename):
        triplets = []
        compatible_e1 = {}
        compatible_e2 = {}
        with open(filename, 'r') as f:
            for line in f:
                terms = line.split()
                if len(terms) == 4:
                    if terms[3] == '-1': continue # skip wrong triplets
                    terms = terms[:3]

                triplets.append(terms)
        return triplets

    @classmethod
    def triplets_to_indices(cls, triplets, entity_vocab=None, relation_vocab=None):
        add_entity = entity_vocab is None
        add_relation = relation_vocab is None

        e1, e2, rel = [], [], []
        for triplet in triplets:
            e1.append(triplet[0])
            rel.append(triplet[1])
            e2.append(triplet[2])

        if entity_vocab is None:
            entity_vocab = Vocab(enable_UNK=False)
        if relation_vocab is None:
            relation_vocab = Vocab(enable_UNK=False)

        e1 = entity_vocab.sent_to_indices(e1, add_word=add_entity)
        e2 = entity_vocab.sent_to_indices(e2, add_word=add_entity)
        rel = relation_vocab.sent_to_indices(rel, add_word=add_relation)

        compatible_e1 = {r:set() for r in xrange(len(relation_vocab))}
        compatible_e2 = {r:set() for r in xrange(len(relation_vocab))}
        for i in xrange(len(rel)):
            r = rel[i]
            compatible_e1[r].add(e1[i])
            compatible_e2[r].add(e2[i])

        for k,v in compatible_e1.items():
            compatible_e1[k] = np.array(list(v))
        for k,v in compatible_e2.items():
            compatible_e2[k] = np.array(list(v))

        data = np.concatenate((
            np.array(e1, dtype='int32').reshape((-1, 1)),
            np.array(rel, dtype='int32').reshape((-1, 1)),
            np.array(e2, dtype='int32').reshape((-1, 1))), axis=1)
        return entity_vocab, compatible_e1, compatible_e2, relation_vocab, data


    @classmethod
    def make_data(cls):
        entity_vocab, compatible_e1, compatible_e2, relation_vocab, train_data = cls.triplets_to_indices(cls.load_triplets(cls.TRAINFILE))
        _, _, _, _, dev_data = cls.triplets_to_indices(cls.load_triplets(cls.DEVFILE), entity_vocab, relation_vocab)
        _, _, _, _, test_data = cls.triplets_to_indices(cls.load_triplets(cls.TESTFILE), entity_vocab, relation_vocab)
        print 'loaded', len(train_data), 'training', len(dev_data), 'dev', len(test_data), 'test triplets', len(entity_vocab), 'word types', len(relation_vocab), 'relation types'

        return {
            'entity_vocab': entity_vocab,
            'relation_vocab': relation_vocab,
            'compatible_e1': compatible_e1,
            'compatible_e2': compatible_e2,
            'train': train_data,
            'dev': dev_data,
            'test': test_data,
        }

if __name__ == '__main__':
    FreebaseKBC.save_data('freebaseKBC.pkl', FreebaseKBC.make_data())

