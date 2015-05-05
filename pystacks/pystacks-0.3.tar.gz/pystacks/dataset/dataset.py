import cPickle as pkl

class Dataset(object):

    @classmethod
    def make_data(self):
        raise NotImplementedError

    @classmethod
    def save_data(self, to_file, data):
        with open(to_file, 'wb') as f:
            pkl.dump(data, f)

    @classmethod
    def load_data(self, from_file):
        with open(from_file, 'rb') as f:
            return pkl.load(f)
