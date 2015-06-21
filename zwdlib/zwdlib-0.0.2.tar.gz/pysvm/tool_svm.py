# -*- coding: utf8 -*-
import os


USE_C_VERSION = True



#def create_training_data(path="training", output="training/training.dat"):
#    from tool_evaluations import Evaluation
#    fp = file(output, "w") 
#    for p in os.listdir(path):
#        if p.endswith(".train"):
#            p = os.path.join(path,p)
#            print "creating record:",p.decode(sys.getfilesystemencoding())
#            
#            fp.write(Evaluation.output_train(p))
#    fp.close()
#
#

# def get_path(path):
#     return os.path.join(os.path.dirname(__file__), path)
    
def load_model(path="training.dat.model"):
#     print path
#     path = get_path(path)
    assert os.path.lexists(path) == True
    if not USE_C_VERSION:
        from tool_pysvm import svm
        return svm.svm_model(path)
    else:
        from svmutil import svm_load_model
        return svm_load_model(path)

def load_ranges(path="training.dat.range"):
#     print path
#     path = get_path(path)
    assert os.path.lexists(path) == True
    fp = file(path,"r")
    line = fp.readline()
    ranges = {}
    while line:
        slices = line.split()
        if len(slices) == 3:
            ranges[int(slices[0])] = (float(slices[1]),float(slices[2]))
        line = fp.readline()
    fp.close()
    return ranges

def _output(value, y_min, y_max, lower=-1, upper=1):
    if y_min == 0 and y_max == 0:
        value = 0
    elif value <= y_min:
        value = lower
    elif value >= y_max:
        value = upper
    else:
        value = lower + (upper-lower) * (value - y_min) * 1.0 /(y_max-y_min);
    return value

def scale(data, ranges, lower=-1):
    return [_output(data[i],ranges.get(i+1,(0,0))[0], ranges.get(i+1,(0,0))[1], lower=lower) for i in range(0, len(data))]


def todict(l):
    rtn = {}
    for i in range(0, len(l)):
        if l[i] != 0:
            rtn[i+1] = l[i]
    return rtn 


#class Sample(object):
#    svm_model = load_model()
#    ranges = load_ranges()
#    
#    def __init__(self, data):
#        self.strike = data[0]
#        self.raw = data[1:]
#    
#    def todict(self, l):
#        rtn = {}
#        for i in range(0, len(l)):
#            if l[i] != 0:
#                rtn[i+1] = l[i]
#        return rtn
#            
#    def __cmp__(self, other):
#        raw = [self.raw[i] - other.raw[i] for i in range(0, len(self.raw))]
#        scaled = scale(raw, Sample.ranges)
#        mapping = self.todict(scaled)
#        
#        results = Sample.svm_model.predict(mapping)
#        return results 
#    
#    def __repr__(self):
#        return str(self.strike)
    
if __name__ == "__main__":
    svm_model = load_model()
    ranges = load_ranges()
    print svm_model
#    l = [2,0,]
#    scale({1:19,2:2,3:1})
    
#    import unittest
#    class TestCase(unittest.TestCase):
#        def _testScale(self):
#            ranges = {1: (-3, 3), 2: (-1, 1), 4: (-1, 1), 5: (-19, 19), 6: (-6, 6), 7: (-7, 7), 8: (-1, 1), 10: (-112, 112), 12: (-12, 12), 15: (-5, 5)}
#            raw = [{1:-2,4:-1,5:1,6:4,10:-36,15:-3}.get(i,0) for i in range(1,16)]
#            targets = [{1:-0.666667,4:-1,5:0.0526316,6:0.666667,10:-0.321429,15:-0.6}.get(i,0) for i in range(1,16)]
#            results =  scale(raw, ranges)
#            assert sum([abs(results[i] - targets[i]) < 0.001 for i in range(0, len(results))]) == 15
#            
#            model = load_model()
#            scaled = [{1:-0.5,5:-1,6:1,10:-1}.get(i,0) for i in range(1,16)]
#            print scaled
##            ranges = load_ranges()
##            print ranges
##            scaled = scale(raw, ranges)
##            print scaled
#            d = {1:-0.5,5:-1,6:1,10:-1}
##            scaled = [d.get(i,0) for i in range(1,16)]
##            print scaled
#            print model.predict(d)
            
    
    
