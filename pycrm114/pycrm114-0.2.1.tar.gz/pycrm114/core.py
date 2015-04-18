from . import flags
from . import _binding
from pycrm114.errors import CRM114InitializationError


class CRM114(object):
    def __init__(self, classes, flags=flags.CRM114_OSB, storage=None, auto_save=False):
        self.classes = classes
        self.flags = flags
        self.storage = storage
        self.auto_save = auto_save
        self.control_block = None
        self.data_block = None
        self.__init_crm()

    def __init_crm(self):
        cb_location = None
        data_location = None
        if self.storage:
            cb_location = self.storage.control_block_file
            data_location = self.storage.data_block_file
        if data_location:
            self.data_block = _binding.DataBlock.load(open(data_location))
        elif cb_location:
            self.control_block = _binding.ControlBlock.load(open(cb_location))
        else:
            try:
                self.control_block = _binding.ControlBlock(flags=self.flags,
                                  classes=[(cls, True) for cls in self.classes],
                                  start_mem = 8000000)
            except _binding.error as e:
                raise CRM114InitializationError("Unable to initialize (%s)" % e)
            self.data_block = _binding.DataBlock(self.control_block)

    def learn(self, cls, text):
        self.data_block.learn_text(self.classes.index(cls), text)
        if self.auto_save and self.storage:
            self.storage.save(self.control_block, self.data_block)

    def classify(self, text):
        match_result = self.data_block.classify_text(text)
        best_match = match_result.best_match()
        score = [k['prob'] for k in match_result.scores() if k['name'] == best_match][0]
        return {"class": best_match, "score": score}

    def save(self):
        if self.storage:
            return self.storage.save(self.control_block, self.data_block)
