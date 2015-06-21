'''
Created on 2014-8-2

@author: Winston Zhong
'''
from pysvm.tool_svm import scale, todict
from svm import gen_svm_nodearray, libsvm

class TrainingRecordBase(object):
    def get_scaled(self):
        if not hasattr(self, "_scaled"):
            self._scaled = scale(self.values(), self.ranges, lower=0) 
        return self._scaled
            
    
    def predict(self):
#         scaled = scale(self.values(), self.ranges)
#         print scaled
#         m = todict(self.get_scaled())
#         results = self.svm_model.predict(m)
#         return results 
#         x0, max_idx = gen_svm_nodearray(m)
#         label = libsvm.svm_predict(self.svm_model, gen_svm_nodearray(m)[0])
#         return label
        return libsvm.svm_predict(self.svm_model, gen_svm_nodearray(todict(self.get_scaled()))[0])
    
    def is_ok(self):
        raise ValueError, 'not implemented'
    
    
    def self_validation(self):
        for x in dir(self):
            if x.startswith('train_') and not x.startswith('train__'):
                raise ValueError, x
    
    def get_training_function(self):
        return [x for x in dir(self) if x.startswith('train__')]
    
    def get_json_data(self):
        if not hasattr(self, 'json_data'):
            self.json_data = {}
            for x in self.get_training_function():
                self.json_data[x.split("__")[1]] = getattr(self, x)()
        return self.json_data
    
    def values(self):
        d = self.get_json_data()
        keys = d.keys()
        keys.sort()
        return [d.get(k) for k in keys]
#         return self.get_json_data().values()
    
    def build(self):
        v = self.values()
        r = ["%d:%s" % (i+1, v[i]) for i in range(len(v)) if v[i]]
        return "%s1 %s\n" % (('-','+')[self.is_ok()], ' '.join(r))
        
if __name__ == '__main__':
    pass