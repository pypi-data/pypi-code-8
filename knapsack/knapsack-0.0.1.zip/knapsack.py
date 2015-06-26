try:
    from functools import lru_cache
except ImportError:
    # For Python2
    # pip install backports.functools_lru_cache
    from backports.functools_lru_cache import lru_cache
class knapsack:
    """
    Maximize sum of selected weight.
    Sum of selected size is les than capacity.
    Algorithm: Dynamic Optimization
    """
    def __init__(self, size, weight):
        self.size = size
        self.weight = weight
    @lru_cache()
    def solve(self, cap, i=0):
        if cap < 0: return -sum(self.weight)
        if i == len(self.size): return 0
        res1 = self.solve(cap,  i + 1)
        res2 = self.solve(cap - self.size[i], i + 1) + self.weight[i]
        return max(res1, res2)
