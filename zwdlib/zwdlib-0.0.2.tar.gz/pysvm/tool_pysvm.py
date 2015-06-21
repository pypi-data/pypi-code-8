# -*- coding: utf-8 -*-
import sys
import copy
import math
import random
import re

INF = sys.maxint

def array_copy(src, srcpos, dst, dstpos, length):
    for i in range(srcpos, length):
        dst[i + dstpos] = src[i]



class svm_problem:
    l = 0
    y = None
    x = None
    
class svm_node:
    index = 0
    value = float()
    
class svm_parameter:
    C_SVC = 0
    NU_SVC = 1
    ONE_CLASS = 2
    EPSILON_SVR = 3
    NU_SVR = 4
    LINEAR = 0
    POLY = 1
    RBF = 2
    SIGMOID = 3
    PRECOMPUTED = 4
    svm_type = 0
    kernel_type = 0
    degree = 0
    gamma = float()
    coef0 = float()
    cache_size = float()
    eps = float()
    C = float()
    nr_weight = 0
    weight_label = None
    weight = None
    nu = float()
    p = float()
    shrinking = 0
    probability = 0

    def clone(self):
        return copy.copy(self)

class svm_model:
    param = None
    nr_class = 0
    l = 0
    SV = None
    sv_coef = None
    rho = None
    probA = None
    probB = None
    label = None
    nSV = None


    def svmnodes_from_dict(self, d={}):
        keys = d.keys()
        keys.sort()
        rtn = []
        for i in keys:
            node = svm_node()
            node.index = i
            node.value = d[i]
            rtn.append(node)
        return rtn
    
    def predict(self, d):
        return svm.svm_predict(self, self.svmnodes_from_dict(d))
    

class head_t(object):
    def __init__(self):
        self.prev = None
        self.next = None
        self.data = None
        self.len = 0

class Cache(object):
    """ porting svm.c

    """
    l = 0
    size = long()
    head = None
    lru_head = head_t()

    def __init__(self, l_, size_):
        self.l = l_
        self.size = size_
        self.head = [head_t() for __idx0 in range(self.l)]
        ## for-while
        i = 0
        while i < self.l:
            self.head[i] = head_t()
            i += 1
        self.size /= 4
        self.size -= self.l * 16 / 4
        self.size = max(self.size, 2 * self.l)
        self.lru_head = head_t()
        self.lru_head.next = self.lru_head.prev = self.lru_head

    def lru_delete(self, h):
        h.prev.next = h.next
        h.next.prev = h.prev

    def lru_insert(self, h):
        h.next = self.lru_head
        h.prev = self.lru_head.prev
        h.prev.next = h
        h.next.prev = h

    def get_data(self, index, data, len):
        h = self.head[index]
        if h.len > 0:
            self.lru_delete(h)
        more = len - h.len
        if more > 0:
            while self.size < more:
                old = self.lru_head.next
                self.lru_delete(old)
                self.size += old.len
                old.data = None
                old.len = 0
            new_data = [float() for __idx0 in range(len)]
            if h.data is not None:
#                System.arraycopy(h.data, 0, new_data, 0, h.len)
                array_copy(h.data, 0, new_data, 0, h.len)
            h.data = new_data
            self.size -= more
            _ = h.len
            h.len = len
            len = _
            False
        self.lru_insert(h)
        data[0] = h.data
        return len

    def swap_index(self, i, j):
        if (i == j):
            return
        if self.head[i].len > 0:
            self.lru_delete(self.head[i])
        if self.head[j].len > 0:
            self.lru_delete(self.head[j])
        _ = self.head[i].data
        self.head[i].data = self.head[j].data
        self.head[j].data = _
        False
        _ = self.head[i].len
        self.head[i].len = self.head[j].len
        self.head[j].len = _
        False
        if self.head[i].len > 0:
            self.lru_insert(self.head[i])
        if self.head[j].len > 0:
            self.lru_insert(self.head[j])
        if i > j:
            _ = i
            i = j
            j = _
            False
        ## for-while
        h = self.lru_head.next
        while (h != self.lru_head):
            if h.len > i:
                if h.len > j:
                    _ = h.data[i]
                    h.data[i] = h.data[j]
                    h.data[j] = _
                    False
                else:
                    self.lru_delete(h)
                    self.size += h.len
                    h.data = None
                    h.len = 0
            h = h.next

class QMatrix(object):
    """ porting svm.c  for QMatrix

    """

    def get_Q(self, column, len):
        pass

    def get_QD(self):
        pass

    def swap_index(self, i, j):
        pass

class Kernel(QMatrix):
    """ porting svm.c  for Kernel

    """
    x = None
    x_square = None
    kernel_type = 0
    degree = 0
    gamma = float()
    coef0 = float()

    def get_Q(self, column, len):
        pass

    def get_QD(self):
        pass

    def swap_index(self, i, j):
        _ = self.x[i]
        self.x[i] = self.x[j]
        self.x[j] = _
        False
        if self.x_square is not None:
            _ = self.x_square[i]
            self.x_square[i] = self.x_square[j]
            self.x_square[j] = _
            False

    @classmethod
    def powi(cls, base, times):
        tmp = base
        ret = 1.0
        ## for-while
        t = times
        while t > 0:
            if (t % 2 == 1):
                ret *= tmp
            tmp = tmp * tmp
            t /= 2
        return ret

    def kernel_function(self, i, j):
        if self.kernel_type == svm_parameter.LINEAR:
            return self.dot(self.x[i], self.x[j])
        elif self.kernel_type == svm_parameter.POLY:
            return self.powi(self.gamma * self.dot(self.x[i], self.x[j]) + self.coef0, self.degree)
        elif self.kernel_type == svm_parameter.RBF:
            return math.exp(-self.gamma * self.x_square[i] + self.x_square[j] - 2 * self.dot(self.x[i], self.x[j]))
        elif self.kernel_type == svm_parameter.SIGMOID:
            return math.tanh(self.gamma * self.dot(self.x[i], self.x[j]) + self.coef0)
        elif self.kernel_type == svm_parameter.PRECOMPUTED:
            return self.x[i][self.x[j][0].value].value
        else:
            return 0

    def __init__(self, l, x_, param):
        self.kernel_type = param.kernel_type
        self.degree = param.degree
        self.gamma = param.gamma
        self.coef0 = param.coef0
        self.x = x_.clone()
        if (self.kernel_type == svm_parameter.RBF):
            self.x_square = [float() for __idx0 in range(l)]
            ## for-while
            i = 0
            while i < l:
                self.x_square[i] = self.dot(self.x[i], self.x[i])
                i += 1
        else:
            self.x_square = None

    @classmethod
    def dot(cls, x, y):
        sum = 0
        xlen = len(x)
        ylen = len(y)
        i = 0
        j = 0
        while i < xlen and j < ylen:
            if (x[i].index == y[j].index):
                sum += x[i].value * y[j].value
                i += 1
                j += 1
            else:
                if x[i].index > y[j].index:
                    j += 1
                else:
                    i += 1
        return sum

    @classmethod
    def k_function(cls, x, y, param):
        if param.kernel_type == svm_parameter.LINEAR:
            return cls.dot(x, y)
        elif param.kernel_type == svm_parameter.POLY:
            return cls.powi(param.gamma * cls.dot(x, y) + param.coef0, param.degree)
        elif param.kernel_type == svm_parameter.RBF:
            sum = 0
            xlen = len(x)
            ylen = len(y)
            i = 0
            j = 0
            while i < xlen and j < ylen:
                if (x[i].index == y[j].index):
                    d = x[i].value - y[j].value
                    i += 1
                    j += 1
                    
                    sum += d * d
                else:
                    if x[i].index > y[j].index:
                        sum += y[j].value * y[j].value
                        j += 1
                    else:
                        sum += x[i].value * x[i].value
                        i += 1
            while i < xlen:
                sum += x[i].value * x[i].value
                i += 1
            while j < ylen:
                sum += y[j].value * y[j].value
                j += 1
            return math.exp(-param.gamma * sum)
        elif param.kernel_type == svm_parameter.SIGMOID:
            return math.tanh(param.gamma * cls.dot(x, y) + param.coef0)
        elif param.kernel_type == svm_parameter.PRECOMPUTED:
            return x[y[0].value].value
        else:
            return 0

class Solver(object):
    """ porting svm.c  for Solver

    """
    class SolutionInfo(object):
        """ porting svm.c  for SolutionInfo

        """
        obj = float()
        rho = float()
        upper_bound_p = float()
        upper_bound_n = float()
        r = float()
    active_size = 0
    y = None
    G = None
    LOWER_BOUND = 0
    UPPER_BOUND = 1
    FREE = 2
    alpha_status = None
    alpha = None
    Q = QMatrix()
    QD = None
    eps = float()
    Cp = float()
    Cn = float()
    p = None
    active_set = None
    G_bar = None
    l = 0
    unshrink = bool()
    INF = sys.maxint#java.lang.Double.POSITIVE_INFINITY

    def get_C(self, i):
        return self.Cp if self.y[i] > 0 else self.Cn

    def update_alpha_status(self, i):
        if self.alpha[i] >= self.get_C(i):
            self.alpha_status[i] = self.UPPER_BOUND
        else:
            if self.alpha[i] <= 0:
                self.alpha_status[i] = self.LOWER_BOUND
            else:
                self.alpha_status[i] = self.FREE

    def is_upper_bound(self, i):
        return (self.alpha_status[i] == self.UPPER_BOUND)

    def is_lower_bound(self, i):
        return (self.alpha_status[i] == self.LOWER_BOUND)

    def is_free(self, i):
        return (self.alpha_status[i] == self.FREE)

    def swap_index(self, i, j):
        self.Q.swap_index(i, j)
        _ = self.y[i]
        self.y[i] = self.y[j]
        self.y[j] = _
        False
        _ = self.G[i]
        self.G[i] = self.G[j]
        self.G[j] = _
        False
        _ = self.alpha_status[i]
        self.alpha_status[i] = self.alpha_status[j]
        self.alpha_status[j] = _
        False
        _ = self.alpha[i]
        self.alpha[i] = self.alpha[j]
        self.alpha[j] = _
        False
        _ = self.p[i]
        self.p[i] = self.p[j]
        self.p[j] = _
        False
        _ = self.active_set[i]
        self.active_set[i] = self.active_set[j]
        self.active_set[j] = _
        False
        _ = self.G_bar[i]
        self.G_bar[i] = self.G_bar[j]
        self.G_bar[j] = _
        False

    def reconstruct_gradient(self):
        if (self.active_size == self.l):
            return
        i = 0
        j = 0
        nr_free = 0
        ## for-while
        j = self.active_size
        while j < self.l:
            self.G[j] = self.G_bar[j] + self.p[j]
            j += 1
        ## for-while
        j = 0
        while j < self.active_size:
            if self.is_free(j):
                nr_free += 1
            j += 1
        if 2 * nr_free < self.active_size:
            svm.info("\nWarning: using -h 0 may be faster\n")
        if nr_free * self.l > 2 * self.active_size * self.l - self.active_size:
            ## for-while
            i = self.active_size
            while i < self.l:
                Q_i = self.Q.get_Q(i, self.active_size)
                ## for-while
                j = 0
                while j < self.active_size:
                    if self.is_free(j):
                        self.G[i] += self.alpha[j] * Q_i[j]
                    j += 1
                i += 1
        else:
            ## for-while
            i = 0
            while i < self.active_size:
                if self.is_free(i):
                    Q_i = self.Q.get_Q(i, self.l)
                    alpha_i = self.alpha[i]
                    ## for-while
                    j = self.active_size
                    while j < self.l:
                        self.G[j] += alpha_i * Q_i[j]
                        j += 1
                i += 1

    def Solve(self, l,
                    Q,
                    p_,
                    y_,
                    alpha_,
                    Cp,
                    Cn,
                    eps,
                    si,
                    shrinking):
        self.l = self.l
        self.Q = self.Q
        self.QD = self.Q.get_QD()
        self.p = p_.clone()
        self.y = y_.clone()
        self.alpha = alpha_.clone()
        self.Cp = self.Cp
        self.Cn = self.Cn
        self.eps = self.eps
        self.unshrink = False
        self.alpha_status = [0 for __idx0 in range(self.l)]
        ## for-while
        i = 0
        while i < self.l:
            self.update_alpha_status(i)
            i += 1
        self.active_set = [int() for __idx0 in range(self.l)]
        ## for-while
        i = 0
        while i < self.l:
            self.active_set[i] = i
            i += 1
        self.active_size = self.l
        self.G = [float() for __idx0 in range(self.l)]
        self.G_bar = [float() for __idx0 in range(self.l)]
        i = 0
        ## for-while
        i = 0
        while i < self.l:
            self.G[i] = self.p[i]
            self.G_bar[i] = 0
            i += 1
        ## for-while
        i = 0
        while i < self.l:
            if not self.is_lower_bound(i):
                Q_i = self.Q.get_Q(i, self.l)
                alpha_i = self.alpha[i]
                j = 0
                ## for-while
                j = 0
                while j < self.l:
                    self.G[j] += alpha_i * Q_i[j]
                    j += 1
                if self.is_upper_bound(i):
                    ## for-while
                    j = 0
                    while j < self.l:
                        self.G_bar[j] += self.get_C(i) * Q_i[j]
                        j += 1
            i += 1
        iter = 0
        counter = min(self.l, 1000) + 1
        working_set = [int() for __idx0 in range(2)]
        while True:
            counter -= 1
            if (counter == 0):
                counter = min(self.l, 1000)
                if (shrinking != 0):
                    self.do_shrinking()
                svm.info(".")
            if (self.select_working_set(working_set) != 0):
                self.reconstruct_gradient()
                self.active_size = self.l
                svm.info("*")
                if (self.select_working_set(working_set) != 0):
                    break
                else:
                    counter = 1
            i = working_set[0]
            j = working_set[1]
            iter += 1
            Q_i = self.Q.get_Q(i, self.active_size)
            Q_j = self.Q.get_Q(j, self.active_size)
            C_i = self.get_C(i)
            C_j = self.get_C(j)
            old_alpha_i = self.alpha[i]
            old_alpha_j = self.alpha[j]
            if (self.y[i] != self.y[j]):
                quad_coef = Q_i[i] + Q_j[j] + 2 * Q_i[j]
                if quad_coef <= 0:
                    quad_coef = 1e-12
                delta = -self.G[i] - self.G[j] / quad_coef
                diff = self.alpha[i] - self.alpha[j]
                self.alpha[i] += delta
                self.alpha[j] += delta
                if diff > 0:
                    if self.alpha[j] < 0:
                        self.alpha[j] = 0
                        self.alpha[i] = diff
                else:
                    if self.alpha[i] < 0:
                        self.alpha[i] = 0
                        self.alpha[j] = -diff
                if diff > C_i - C_j:
                    if self.alpha[i] > C_i:
                        self.alpha[i] = C_i
                        self.alpha[j] = C_i - diff
                else:
                    if self.alpha[j] > C_j:
                        self.alpha[j] = C_j
                        self.alpha[i] = C_j + diff
            else:
                quad_coef = Q_i[i] + Q_j[j] - 2 * Q_i[j]
                if quad_coef <= 0:
                    quad_coef = 1e-12
                delta = self.G[i] - self.G[j] / quad_coef
                sum = self.alpha[i] + self.alpha[j]
                self.alpha[i] -= delta
                self.alpha[j] += delta
                if sum > C_i:
                    if self.alpha[i] > C_i:
                        self.alpha[i] = C_i
                        self.alpha[j] = sum - C_i
                else:
                    if self.alpha[j] < 0:
                        self.alpha[j] = 0
                        self.alpha[i] = sum
                if sum > C_j:
                    if self.alpha[j] > C_j:
                        self.alpha[j] = C_j
                        self.alpha[i] = sum - C_j
                else:
                    if self.alpha[i] < 0:
                        self.alpha[i] = 0
                        self.alpha[j] = sum
            delta_alpha_i = self.alpha[i] - old_alpha_i
            delta_alpha_j = self.alpha[j] - old_alpha_j
            ## for-while
            k = 0
            while k < self.active_size:
                self.G[k] += Q_i[k] * delta_alpha_i + Q_j[k] * delta_alpha_j
                k += 1
            ui = self.is_upper_bound(i)
            uj = self.is_upper_bound(j)
            self.update_alpha_status(i)
            self.update_alpha_status(j)
            k = 0
            if (ui != self.is_upper_bound(i)):
                Q_i = self.Q.get_Q(i, self.l)
                if ui:
                    ## for-while
                    k = 0
                    while k < self.l:
                        self.G_bar[k] -= C_i * Q_i[k]
                        k += 1
                else:
                    ## for-while
                    k = 0
                    while k < self.l:
                        self.G_bar[k] += C_i * Q_i[k]
                        k += 1
            if (uj != self.is_upper_bound(j)):
                Q_j = self.Q.get_Q(j, self.l)
                if uj:
                    ## for-while
                    k = 0
                    while k < self.l:
                        self.G_bar[k] -= C_j * Q_j[k]
                        k += 1
                else:
                    ## for-while
                    k = 0
                    while k < self.l:
                        self.G_bar[k] += C_j * Q_j[k]
                        k += 1
        si.rho = self.calculate_rho()
        v = 0
        i = 0
        ## for-while
        i = 0
        while i < self.l:
            v += self.alpha[i] * self.G[i] + self.p[i]
            i += 1
        si.obj = v / 2
        ## for-while
        i = 0
        while i < self.l:
            alpha_[self.active_set[i]] = self.alpha[i]
            i += 1
        si.upper_bound_p = self.Cp
        si.upper_bound_n = self.Cn
        svm.info("\noptimization finished, #iter = " + iter + "\n")

    def select_working_set(self, working_set):
        Gmax = -self.INF
        Gmax2 = -self.INF
        Gmax_idx = -1
        Gmin_idx = -1
        obj_diff_min = self.INF
        ## for-while
        t = 0
        while t < self.active_size:
            if (self.y[t] == +1):
                if not self.is_upper_bound(t):
                    if -self.G[t] >= Gmax:
                        Gmax = -self.G[t]
                        Gmax_idx = t
            else:
                if not self.is_lower_bound(t):
                    if self.G[t] >= Gmax:
                        Gmax = self.G[t]
                        Gmax_idx = t
            t += 1
        i = Gmax_idx
        Q_i = None
        if (i != -1):
            Q_i = self.Q.get_Q(i, self.active_size)
        ## for-while
        j = 0
        while j < self.active_size:
            if (self.y[j] == +1):
                if not self.is_lower_bound(j):
                    grad_diff = Gmax + self.G[j]
                    if self.G[j] >= Gmax2:
                        Gmax2 = self.G[j]
                    if grad_diff > 0:
                        obj_diff = float()
                        quad_coef = Q_i[i] + self.QD[j] - 2.0 * self.y[i] * Q_i[j]
                        if quad_coef > 0:
                            obj_diff = -grad_diff * grad_diff / quad_coef
                        else:
                            obj_diff = -grad_diff * grad_diff / 1e-12
                        if obj_diff <= obj_diff_min:
                            Gmin_idx = j
                            obj_diff_min = obj_diff
            else:
                if not self.is_upper_bound(j):
                    grad_diff = Gmax - self.G[j]
                    if -self.G[j] >= Gmax2:
                        Gmax2 = -self.G[j]
                    if grad_diff > 0:
                        obj_diff = float()
                        quad_coef = Q_i[i] + self.QD[j] + 2.0 * self.y[i] * Q_i[j]
                        if quad_coef > 0:
                            obj_diff = -grad_diff * grad_diff / quad_coef
                        else:
                            obj_diff = -grad_diff * grad_diff / 1e-12
                        if obj_diff <= obj_diff_min:
                            Gmin_idx = j
                            obj_diff_min = obj_diff
            j += 1
        if Gmax + Gmax2 < self.eps:
            return 1
        working_set[0] = Gmax_idx
        working_set[1] = Gmin_idx
        return 0

    def be_shrunk(self, i, Gmax1, Gmax2):
        if self.is_upper_bound(i):
            if (self.y[i] == +1):
                return -self.G[i] > Gmax1
            else:
                return -self.G[i] > Gmax2
        else:
            if self.is_lower_bound(i):
                if (self.y[i] == +1):
                    return self.G[i] > Gmax2
                else:
                    return self.G[i] > Gmax1
            else:
                return False

    def do_shrinking(self):
        i = 0
        Gmax1 = -self.INF
        Gmax2 = -self.INF
        ## for-while
        i = 0
        while i < self.active_size:
            if (self.y[i] == +1):
                if not self.is_upper_bound(i):
                    if -self.G[i] >= Gmax1:
                        Gmax1 = -self.G[i]
                if not self.is_lower_bound(i):
                    if self.G[i] >= Gmax2:
                        Gmax2 = self.G[i]
            else:
                if not self.is_upper_bound(i):
                    if -self.G[i] >= Gmax2:
                        Gmax2 = -self.G[i]
                if not self.is_lower_bound(i):
                    if self.G[i] >= Gmax1:
                        Gmax1 = self.G[i]
            i += 1
        if (self.unshrink == False) and Gmax1 + Gmax2 <= self.eps * 10:
            self.unshrink = True
            self.reconstruct_gradient()
            self.active_size = self.l
        ## for-while
        i = 0
        while i < self.active_size:
            if self.be_shrunk(i, Gmax1, Gmax2):
                self.active_size -= 1
                while self.active_size > i:
                    if not self.be_shrunk(self.active_size, Gmax1, Gmax2):
                        self.swap_index(i, self.active_size)
                        break
                    self.active_size -= 1
            i += 1

    def calculate_rho(self):
        r = float()
        nr_free = 0
        ub = self.INF
        lb = -self.INF
        sum_free = 0
        ## for-while
        i = 0
        while i < self.active_size:
            yG = self.y[i] * self.G[i]
            if self.is_lower_bound(i):
                if self.y[i] > 0:
                    ub = min(ub, yG)
                else:
                    lb = max(lb, yG)
            else:
                if self.is_upper_bound(i):
                    if self.y[i] < 0:
                        ub = min(ub, yG)
                    else:
                        lb = max(lb, yG)
                else:
                    nr_free += 1
                    sum_free += yG
            i += 1
        if nr_free > 0:
            r = sum_free / nr_free
        else:
            r = ub + lb / 2
        return r

class Solver_NU(Solver):
    """ porting svm.c  for Solver_NU

    """
    si = Solver.SolutionInfo()

    def Solve(self, l,
                    Q,
                    p,
                    y,
                    alpha,
                    Cp,
                    Cn,
                    eps,
                    si,
                    shrinking):
        self.si = self.si
        super.Solve(l, Q, p, y, alpha, Cp, Cn, eps, self.si, shrinking)

    def select_working_set(self, working_set):
        Gmaxp = -INF
        Gmaxp2 = -INF
        Gmaxp_idx = -1
        Gmaxn = -INF
        Gmaxn2 = -INF
        Gmaxn_idx = -1
        Gmin_idx = -1
        obj_diff_min = INF
        ## for-while
        t = 0
        while t < self.active_size:
            if (self.y[t] == +1):
                if not self.is_upper_bound(t):
                    if -self.G[t] >= Gmaxp:
                        Gmaxp = -self.G[t]
                        Gmaxp_idx = t
            else:
                if not self.is_lower_bound(t):
                    if self.G[t] >= Gmaxn:
                        Gmaxn = self.G[t]
                        Gmaxn_idx = t
            t += 1
        ip = Gmaxp_idx
        in_ = Gmaxn_idx
        Q_ip = None
        Q_in = None
        if (ip != -1):
            Q_ip = self.Q.get_Q(ip, self.active_size)
        if (in_ != -1):
            Q_in = self.Q.get_Q(in_, self.active_size)
        ## for-while
        j = 0
        while j < self.active_size:
            if (self.y[j] == +1):
                if not self.is_lower_bound(j):
                    grad_diff = Gmaxp + self.G[j]
                    if self.G[j] >= Gmaxp2:
                        Gmaxp2 = self.G[j]
                    if grad_diff > 0:
                        obj_diff = float()
                        quad_coef = Q_ip[ip] + self.QD[j] - 2 * Q_ip[j]
                        if quad_coef > 0:
                            obj_diff = -grad_diff * grad_diff / quad_coef
                        else:
                            obj_diff = -grad_diff * grad_diff / 1e-12
                        if obj_diff <= obj_diff_min:
                            Gmin_idx = j
                            obj_diff_min = obj_diff
            else:
                if not self.is_upper_bound(j):
                    grad_diff = Gmaxn - self.G[j]
                    if -self.G[j] >= Gmaxn2:
                        Gmaxn2 = -self.G[j]
                    if grad_diff > 0:
                        obj_diff = float()
                        quad_coef = Q_in[in_] + self.QD[j] - 2 * Q_in[j]
                        if quad_coef > 0:
                            obj_diff = -grad_diff * grad_diff / quad_coef
                        else:
                            obj_diff = -grad_diff * grad_diff / 1e-12
                        if obj_diff <= obj_diff_min:
                            Gmin_idx = j
                            obj_diff_min = obj_diff
            j += 1
        if max(Gmaxp + Gmaxp2, Gmaxn + Gmaxn2) < self.eps:
            return 1
        if (self.y[Gmin_idx] == +1):
            working_set[0] = Gmaxp_idx
        else:
            working_set[0] = Gmaxn_idx
        working_set[1] = Gmin_idx
        return 0

    def be_shrunk(self, i,
                        Gmax1,
                        Gmax2,
                        Gmax3,
                        Gmax4):
        if self.is_upper_bound(i):
            if (self.y[i] == +1):
                return -self.G[i] > Gmax1
            else:
                return -self.G[i] > Gmax4
        else:
            if self.is_lower_bound(i):
                if (self.y[i] == +1):
                    return self.G[i] > Gmax2
                else:
                    return self.G[i] > Gmax3
            else:
                return False

    def do_shrinking(self):
        Gmax1 = -INF
        Gmax2 = -INF
        Gmax3 = -INF
        Gmax4 = -INF
        i = 0
        ## for-while
        i = 0
        while i < self.active_size:
            if not self.is_upper_bound(i):
                if (self.y[i] == +1):
                    if -self.G[i] > Gmax1:
                        Gmax1 = -self.G[i]
                else:
                    if -self.G[i] > Gmax4:
                        Gmax4 = -self.G[i]
            if not self.is_lower_bound(i):
                if (self.y[i] == +1):
                    if self.G[i] > Gmax2:
                        Gmax2 = self.G[i]
                else:
                    if self.G[i] > Gmax3:
                        Gmax3 = self.G[i]
            i += 1
        if (self.unshrink == False) and max(Gmax1 + Gmax2, Gmax3 + Gmax4) <= self.eps * 10:
            self.unshrink = True
            self.reconstruct_gradient()
            self.active_size = self.l
        ## for-while
        i = 0
        while i < self.active_size:
            if self.be_shrunk(i, Gmax1, Gmax2, Gmax3, Gmax4):
                self.active_size -= 1
                while self.active_size > i:
                    if not self.be_shrunk(self.active_size, Gmax1, Gmax2, Gmax3, Gmax4):
                        self.swap_index(i, self.active_size)
                        break
                    self.active_size -= 1
            i += 1

    def calculate_rho(self):
        nr_free1 = 0
        nr_free2 = 0
        ub1 = INF
        ub2 = INF
        lb1 = -INF
        lb2 = -INF
        sum_free1 = 0
        sum_free2 = 0
        ## for-while
        i = 0
        while i < self.active_size:
            if (self.y[i] == +1):
                if self.is_lower_bound(i):
                    ub1 = min(ub1, self.G[i])
                else:
                    if self.is_upper_bound(i):
                        lb1 = max(lb1, self.G[i])
                    else:
                        nr_free1 += 1
                        sum_free1 += self.G[i]
            else:
                if self.is_lower_bound(i):
                    ub2 = min(ub2, self.G[i])
                else:
                    if self.is_upper_bound(i):
                        lb2 = max(lb2, self.G[i])
                    else:
                        nr_free2 += 1
                        sum_free2 += self.G[i]
            i += 1
        r1 = float()
        r2 = float()
        if nr_free1 > 0:
            r1 = sum_free1 / nr_free1
        else:
            r1 = ub1 + lb1 / 2
        if nr_free2 > 0:
            r2 = sum_free2 / nr_free2
        else:
            r2 = ub2 + lb2 / 2
        self.si.r = r1 + r2 / 2
        return r1 - r2 / 2

class SVC_Q(Kernel):
    """ porting svm.c  for SVC_Q

    """
    y = None
    cache = None
    QD = None

    def __init__(self, prob, param, y_):
        self.y = y_.clone()
        self.cache = Cache(prob.l, param.cache_size * 1 << 20)
        self.QD = [float() for __idx0 in range(prob.l)]
        ## for-while
        i = 0
        while i < prob.l:
            self.QD[i] = self.kernel_function(i, i)
            i += 1

    def get_Q(self, i, len):
        data = [float() for __idx0 in range(1)]
        start = 0
        j = 0
        start = self.cache.get_data(i, data, len)
        if start < len:
            ## for-while
            j = start
            while j < len:
                data[0][j] = self.y[i] * self.y[j] * self.kernel_function(i, j)
                j += 1
        return data[0]

    def get_QD(self):
        return self.QD

    def swap_index(self, i, j):
        self.cache.swap_index(i, j)
        super.swap_index(i, j)
        _ = self.y[i]
        self.y[i] = self.y[j]
        self.y[j] = _
        False
        _ = self.QD[i]
        self.QD[i] = self.QD[j]
        self.QD[j] = _
        False

class ONE_CLASS_Q(Kernel):
    """ porting svm.c  for ONE_CLASS_Q

    """
    cache = None
    QD = None

    def __init__(self, prob, param):
        self.cache = Cache(prob.l, param.cache_size * 1 << 20)
        self.QD = [float() for __idx0 in range(prob.l)]
        ## for-while
        i = 0
        while i < prob.l:
            self.QD[i] = self.kernel_function(i, i)
            i += 1

    def get_Q(self, i, len):
        data = [float() for __idx0 in range(1)]
        start = 0
        j = 0
        start = self.cache.get_data(i, data, len)
        if start < len:
            ## for-while
            j = start
            while j < len:
                data[0][j] = self.kernel_function(i, j)
                j += 1
        return data[0]

    def get_QD(self):
        return self.QD

    def swap_index(self, i, j):
        self.cache.swap_index(i, j)
        super.swap_index(i, j)
        _ = self.QD[i]
        self.QD[i] = self.QD[j]
        self.QD[j] = _
        False

class SVR_Q(Kernel):
    """ porting svm.c  for SVR_Q

    """
    l = 0
    cache = None
    sign = None
    index = None
    next_buffer = 0
    buffer = None
    QD = None

    def __init__(self, prob, param):
        self.l = prob.l
        self.cache = Cache(self.l, param.cache_size * 1 << 20)
        self.QD = [float() for __idx0 in range(2 * self.l)]
        self.sign = [0 for __idx0 in range(2 * self.l)]
        self.index = [int() for __idx0 in range(2 * self.l)]
        ## for-while
        k = 0
        while k < self.l:
            self.sign[k] = 1
            self.sign[k + self.l] = -1
            self.index[k] = k
            self.index[k + self.l] = k
            self.QD[k] = self.kernel_function(k, k)
            self.QD[k + self.l] = self.QD[k]
            k += 1
        self.buffer = [float() for __idx0 in range(2 * self.l)]
        self.next_buffer = 0

    def swap_index(self, i, j):
        _ = self.sign[i]
        self.sign[i] = self.sign[j]
        self.sign[j] = _
        False
        _ = self.index[i]
        self.index[i] = self.index[j]
        self.index[j] = _
        False
        _ = self.QD[i]
        self.QD[i] = self.QD[j]
        self.QD[j] = _
        False

    def get_Q(self, i, len):
        data = [float() for __idx0 in range(1)]
        j = 0
        real_i = self.index[i]
        if self.cache.get_data(real_i, data, self.l) < self.l:
            ## for-while
            j = 0
            while j < self.l:
                data[0][j] = self.kernel_function(real_i, j)
                j += 1
        buf = self.buffer[self.next_buffer]
        self.next_buffer = 1 - self.next_buffer
        si = self.sign[i]
        ## for-while
        j = 0
        while j < len:
            buf[j] = si * self.sign[j] * data[0][self.index[j]]
            j += 1
        return buf

    def get_QD(self):
        return self.QD

class svm(object):
    """ porting svm.c  for svm

    """
    class decision_function(object):
        """ porting svm.c  for decision_function

        """
        alpha = None
        rho = float()
    LIBSVM_VERSION = 289

#    def print(self, s):
#        System.out.print(s)
#        print s

#    svm_print_string = svm_print_interface()

    @classmethod
    def info(cls, s):
#        cls.svm_print_string.cls.print(s)
        print s

    @classmethod
    def solve_c_svc(cls, prob,
                         param,
                         alpha,
                         si,
                         Cp,
                         Cn):
        l = prob.l
        minus_ones = [float() for __idx0 in range(l)]
        y = [0 for __idx0 in range(l)]
        i = 0
        ## for-while
        i = 0
        while i < l:
            alpha[i] = 0
            minus_ones[i] = -1
            if prob.y[i] > 0:
                y[i] = +1
            else:
                y[i] = -1
            i += 1
        s = Solver()
        s.Solve(l, SVC_Q(prob, param, y), minus_ones, y, alpha, Cp, Cn, param.eps, si, param.shrinking)
        sum_alpha = 0
        ## for-while
        i = 0
        while i < l:
            sum_alpha += alpha[i]
            i += 1
        if (Cp == Cn):
            svm.cls.info("nu = " + sum_alpha / Cp * prob.l + "\n")
        ## for-while
        i = 0
        while i < l:
            alpha[i] *= y[i]
            i += 1

    @classmethod
    def solve_nu_svc(cls, prob, param, alpha, si):
        i = 0
        l = prob.l
        nu = param.nu
        y = [0 for __idx0 in range(l)]
        ## for-while
        i = 0
        while i < l:
            if prob.y[i] > 0:
                y[i] = +1
            else:
                y[i] = -1
            i += 1
        sum_pos = nu * l / 2
        sum_neg = nu * l / 2
        ## for-while
        i = 0
        while i < l:
            if (y[i] == +1):
                alpha[i] = min(1.0, sum_pos)
                sum_pos -= alpha[i]
            else:
                alpha[i] = min(1.0, sum_neg)
                sum_neg -= alpha[i]
            i += 1
        zeros = [float() for __idx0 in range(l)]
        ## for-while
        i = 0
        while i < l:
            zeros[i] = 0
            i += 1
        s = Solver_NU()
        s.Solve(l, SVC_Q(prob, param, y), zeros, y, alpha, 1.0, 1.0, param.eps, si, param.shrinking)
        r = si.r
        svm.cls.info("C = " + 1 / r + "\n")
        ## for-while
        i = 0
        while i < l:
            alpha[i] *= y[i] / r
            i += 1
        si.rho /= r
        si.obj /= r * r
        si.upper_bound_p = 1 / r
        si.upper_bound_n = 1 / r

    @classmethod
    def solve_one_class(cls, prob, param, alpha, si):
        l = prob.l
        zeros = [float() for __idx0 in range(l)]
        ones = [0 for __idx0 in range(l)]
        i = 0
        n = param.nu * prob.l
        ## for-while
        i = 0
        while i < n:
            alpha[i] = 1
            i += 1
        if n < prob.l:
            alpha[n] = param.nu * prob.l - n
        ## for-while
        i = n + 1
        while i < l:
            alpha[i] = 0
            i += 1
        ## for-while
        i = 0
        while i < l:
            zeros[i] = 0
            ones[i] = 1
            i += 1
        s = Solver()
        s.Solve(l, ONE_CLASS_Q(prob, param), zeros, ones, alpha, 1.0, 1.0, param.eps, si, param.shrinking)

    @classmethod
    def solve_epsilon_svr(cls, prob, param, alpha, si):
        l = prob.l
        alpha2 = [float() for __idx0 in range(2 * l)]
        linear_term = [float() for __idx0 in range(2 * l)]
        y = [0 for __idx0 in range(2 * l)]
        i = 0
        ## for-while
        i = 0
        while i < l:
            alpha2[i] = 0
            linear_term[i] = param.p - prob.y[i]
            y[i] = 1
            alpha2[i + l] = 0
            linear_term[i + l] = param.p + prob.y[i]
            y[i + l] = -1
            i += 1
        s = Solver()
        s.Solve(2 * l, SVR_Q(prob, param), linear_term, y, alpha2, param.C, param.C, param.eps, si, param.shrinking)
        sum_alpha = 0
        ## for-while
        i = 0
        while i < l:
            alpha[i] = alpha2[i] - alpha2[i + l]
            sum_alpha += abs(alpha[i])
            i += 1
        svm.cls.info("nu = " + sum_alpha / param.C * l + "\n")

    @classmethod
    def solve_nu_svr(cls, prob, param, alpha, si):
        l = prob.l
        C = param.C
        alpha2 = [float() for __idx0 in range(2 * l)]
        linear_term = [float() for __idx0 in range(2 * l)]
        y = [0 for __idx0 in range(2 * l)]
        i = 0
        sum = C * param.nu * l / 2
        ## for-while
        i = 0
        while i < l:
            alpha2[i] = alpha2[i + l] = min(sum, C)
            sum -= alpha2[i]
            linear_term[i] = -prob.y[i]
            y[i] = 1
            linear_term[i + l] = prob.y[i]
            y[i + l] = -1
            i += 1
        s = Solver_NU()
        s.Solve(2 * l, SVR_Q(prob, param), linear_term, y, alpha2, C, C, param.eps, si, param.shrinking)
        svm.cls.info("epsilon = " + -si.r + "\n")
        ## for-while
        i = 0
        while i < l:
            alpha[i] = alpha2[i] - alpha2[i + l]
            i += 1

    @classmethod
    def svm_train_one(cls, prob, param, Cp, Cn):
        alpha = [float() for __idx0 in range(prob.l)]
        si = Solver.SolutionInfo()
        if param.svm_type == svm_parameter.C_SVC:
            cls.solve_c_svc(prob, param, alpha, si, Cp, Cn)
        elif param.svm_type == svm_parameter.NU_SVC:
            cls.solve_nu_svc(prob, param, alpha, si)
        elif param.svm_type == svm_parameter.ONE_CLASS:
            cls.solve_one_class(prob, param, alpha, si)
        elif param.svm_type == svm_parameter.EPSILON_SVR:
            cls.solve_epsilon_svr(prob, param, alpha, si)
        elif param.svm_type == svm_parameter.NU_SVR:
            cls.solve_nu_svr(prob, param, alpha, si)
        svm.cls.info("obj = " + si.obj + ", rho = " + si.rho + "\n")
        nSV = 0
        nBSV = 0
        ## for-while
        i = 0
        while i < prob.l:
            if abs(alpha[i]) > 0:
                nSV += 1
                if prob.y[i] > 0:
                    if abs(alpha[i]) >= si.upper_bound_p:
                        nBSV += 1
                else:
                    if abs(alpha[i]) >= si.upper_bound_n:
                        nBSV += 1
            i += 1
        svm.cls.info("nSV = " + nSV + ", nBSV = " + nBSV + "\n")
        f = cls.decision_function()
        f.alpha = alpha
        f.rho = si.rho
        return f

    @classmethod
    def sigmoid_train(cls, l, dec_values, labels, probAB):
        A = float()
        B = float()
        prior1 = 0
        prior0 = 0
        i = 0
        ## for-while
        i = 0
        while i < l:
            if labels[i] > 0:
                prior1 += 1
            else:
                prior0 += 1
            i += 1
        max_iter = 100
        min_step = 1e-10
        sigma = 1e-12
        eps = 1e-5
        hiTarget = prior1 + 1.0 / prior1 + 2.0
        loTarget = 1 / prior0 + 2.0
        t = [float() for __idx0 in range(l)]
        fApB = float()
        p = float()
        q = float()
        h11 = float()
        h22 = float()
        h21 = float()
        g1 = float()
        g2 = float()
        det = float()
        dA = float()
        dB = float()
        gd = float()
        stepsize = float()
        newA = float()
        newB = float()
        newf = float()
        d1 = float()
        d2 = float()
        iter = 0
        A = 0.0
        B = math.log(prior0 + 1.0 / prior1 + 1.0)
        fval = 0.0
        ## for-while
        i = 0
        while i < l:
            if labels[i] > 0:
                t[i] = hiTarget
            else:
                t[i] = loTarget
            fApB = dec_values[i] * A + B
            if fApB >= 0:
                fval += t[i] * fApB + math.log(1 + math.exp(-fApB))
            else:
                fval += t[i] - 1 * fApB + math.log(1 + math.exp(fApB))
            i += 1
        ## for-while
        iter = 0
        while iter < max_iter:
            h11 = sigma
            h22 = sigma
            h21 = 0.0
            g1 = 0.0
            g2 = 0.0
            ## for-while
            i = 0
            while i < l:
                fApB = dec_values[i] * A + B
                if fApB >= 0:
                    p = math.exp(-fApB) / 1.0 + math.exp(-fApB)
                    q = 1.0 / 1.0 + math.exp(-fApB)
                else:
                    p = 1.0 / 1.0 + math.exp(fApB)
                    q = math.exp(fApB) / 1.0 + math.exp(fApB)
                d2 = p * q
                h11 += dec_values[i] * dec_values[i] * d2
                h22 += d2
                h21 += dec_values[i] * d2
                d1 = t[i] - p
                g1 += dec_values[i] * d1
                g2 += d1
                i += 1
            if abs(g1) < eps and abs(g2) < eps:
                break
            det = h11 * h22 - h21 * h21
            dA = -h22 * g1 - h21 * g2 / det
            dB = --h21 * g1 + h11 * g2 / det
            gd = g1 * dA + g2 * dB
            stepsize = 1
            while stepsize >= min_step:
                newA = A + stepsize * dA
                newB = B + stepsize * dB
                newf = 0.0
                ## for-while
                i = 0
                while i < l:
                    fApB = dec_values[i] * newA + newB
                    if fApB >= 0:
                        newf += t[i] * fApB + math.log(1 + math.exp(-fApB))
                    else:
                        newf += t[i] - 1 * fApB + math.log(1 + math.exp(fApB))
                    i += 1
                if newf < fval + 0.0001 * stepsize * gd:
                    A = newA
                    B = newB
                    fval = newf
                    break
                else:
                    stepsize = stepsize / 2.0
            if stepsize < min_step:
                svm.cls.info("Line search fails in two-class probability estimates\n")
                break
            iter += 1
        if iter >= max_iter:
            svm.cls.info("Reaching maximal iterations in two-class probability estimates\n")
        probAB[0] = A
        probAB[1] = B

    @classmethod
    def sigmoid_predict(cls, decision_value, A, B):
        fApB = decision_value * A + B
        if fApB >= 0:
            return math.exp(-fApB) / 1.0 + math.exp(-fApB)
        else:
            return 1.0 / 1 + math.exp(fApB)

    @classmethod
    def multiclass_probability(cls, k, r, p):
        t = 0
        j = 0
        iter = 0
        max_iter = max(100, k)
        Q = [float() for __idx0 in range(k)]
        Qp = [float() for __idx0 in range(k)]
        pQp = float()
        eps = 0.005 / k
        ## for-while
        t = 0
        while t < k:
            p[t] = 1.0 / k
            Q[t][t] = 0
            ## for-while
            j = 0
            while j < t:
                Q[t][t] += r[j][t] * r[j][t]
                Q[t][j] = Q[j][t]
                j += 1
            ## for-while
            j = t + 1
            while j < k:
                Q[t][t] += r[j][t] * r[j][t]
                Q[t][j] = -r[j][t] * r[t][j]
                j += 1
            t += 1
        ## for-while
        iter = 0
        while iter < max_iter:
            pQp = 0
            ## for-while
            t = 0
            while t < k:
                Qp[t] = 0
                ## for-while
                j = 0
                while j < k:
                    Qp[t] += Q[t][j] * p[j]
                    j += 1
                pQp += p[t] * Qp[t]
                t += 1
            max_error = 0
            ## for-while
            t = 0
            while t < k:
                error = abs(Qp[t] - pQp)
                if error > max_error:
                    max_error = error
                t += 1
            if max_error < eps:
                break
            ## for-while
            t = 0
            while t < k:
                diff = -Qp[t] + pQp / Q[t][t]
                p[t] += diff
                pQp = pQp + diff * diff * Q[t][t] + 2 * Qp[t] / 1 + diff / 1 + diff
                ## for-while
                j = 0
                while j < k:
                    Qp[j] = Qp[j] + diff * Q[t][j] / 1 + diff
                    p[j] /= 1 + diff
                    j += 1
                t += 1
            iter += 1
        if iter >= max_iter:
            svm.cls.info("Exceeds max_iter in multiclass_prob\n")

    @classmethod
    def svm_binary_svc_probability(cls, prob,
                                        param,
                                        Cp,
                                        Cn,
                                        probAB):
        i = 0
        nr_fold = 5
        perm = [int() for __idx0 in range(prob.l)]
        dec_values = [float() for __idx0 in range(prob.l)]
        ## for-while
        i = 0
        while i < prob.l:
            perm[i] = i
            i += 1
        ## for-while
        i = 0
        while i < prob.l:
            j = i + random.random() * prob.l - i
            _ = perm[i]
            perm[i] = perm[j]
            perm[j] = _
            False
            i += 1
        ## for-while
        i = 0
        while i < nr_fold:
            begin = i * prob.l / nr_fold
            end = i + 1 * prob.l / nr_fold
            j = 0
            k = 0
            subprob = svm_problem()
            subprob.l = prob.l - end - begin
            subprob.x = [svm_node() for __idx0 in range(subprob.l)]
            subprob.y = [float() for __idx0 in range(subprob.l)]
            k = 0
            ## for-while
            j = 0
            while j < begin:
                subprob.x[k] = prob.x[perm[j]]
                subprob.y[k] = prob.y[perm[j]]
                k += 1
                j += 1
            ## for-while
            j = end
            while j < prob.l:
                subprob.x[k] = prob.x[perm[j]]
                subprob.y[k] = prob.y[perm[j]]
                k += 1
                j += 1
            p_count = 0
            n_count = 0
            ## for-while
            j = 0
            while j < k:
                if subprob.y[j] > 0:
                    p_count += 1
                else:
                    n_count += 1
                j += 1
            if (p_count == 0) and (n_count == 0):
                ## for-while
                j = begin
                while j < end:
                    dec_values[perm[j]] = 0
                    j += 1
            else:
                if p_count > 0 and (n_count == 0):
                    ## for-while
                    j = begin
                    while j < end:
                        dec_values[perm[j]] = 1
                        j += 1
                else:
                    if (p_count == 0) and n_count > 0:
                        ## for-while
                        j = begin
                        while j < end:
                            dec_values[perm[j]] = -1
                            j += 1
                    else:
                        subparam = param.clone()
                        subparam.probability = 0
                        subparam.C = 1.0
                        subparam.nr_weight = 2
                        subparam.weight_label = [int() for __idx0 in range(2)]
                        subparam.weight = [float() for __idx0 in range(2)]
                        subparam.weight_label[0] = +1
                        subparam.weight_label[1] = -1
                        subparam.weight[0] = Cp
                        subparam.weight[1] = Cn
                        submodel = cls.svm_train(subprob, subparam)
                        ## for-while
                        j = begin
                        while j < end:
                            dec_value = [float() for __idx0 in range(1)]
                            cls.svm_predict_values(submodel, prob.x[perm[j]], dec_value)
                            dec_values[perm[j]] = dec_value[0]
                            dec_values[perm[j]] *= submodel.label[0]
                            j += 1
            i += 1
        cls.sigmoid_train(prob.l, dec_values, prob.y, probAB)

    @classmethod
    def svm_svr_probability(cls, prob, param):
        i = 0
        nr_fold = 5
        ymv = [float() for __idx0 in range(prob.l)]
        mae = 0
        newparam = param.clone()
        newparam.probability = 0
        cls.svm_cross_validation(prob, newparam, nr_fold, ymv)
        ## for-while
        i = 0
        while i < prob.l:
            ymv[i] = prob.y[i] - ymv[i]
            mae += abs(ymv[i])
            i += 1
        mae /= prob.l
        std = math.sqrt(2 * mae * mae)
        count = 0
        mae = 0
        ## for-while
        i = 0
        while i < prob.l:
            if abs(ymv[i]) > 5 * std:
                count = count + 1
            else:
                mae += abs(ymv[i])
            i += 1
        mae /= prob.l - count
        svm.cls.info("Prob. model for test data: target value = predicted value + z,\nz: Laplace distribution e^(-|z|/sigma)/(2sigma),sigma=" + mae + "\n")
        return mae

    @classmethod
    def svm_group_classes(cls, prob,
                               nr_class_ret,
                               label_ret,
                               start_ret,
                               count_ret,
                               perm):
        l = prob.l
        max_nr_class = 16
        nr_class = 0
        label = [int() for __idx0 in range(max_nr_class)]
        count = [int() for __idx0 in range(max_nr_class)]
        data_label = [int() for __idx0 in range(l)]
        i = 0
        ## for-while
        i = 0
        while i < l:
            this_label = prob.y[i]
            j = 0
            ## for-while
            j = 0
            while j < nr_class:
                if (this_label == label[j]):
                    count[j] += 1
                    break
                j += 1
            data_label[i] = j
            if (j == nr_class):
                if (nr_class == max_nr_class):
                    max_nr_class *= 2
                    new_data = [int() for __idx0 in range(max_nr_class)]
#                    System.arraycopy(label, 0, new_data, 0, label.length)
                    array_copy(label, 0, new_data, 0, label.length)
                    label = new_data
                    new_data = [int() for __idx0 in range(max_nr_class)]
#                    System.arraycopy(count, 0, new_data, 0, count.length)
                    array_copy(count, 0, new_data, 0, count.length)
                    count = new_data
                label[nr_class] = this_label
                count[nr_class] = 1
                nr_class += 1
            i += 1
        start = [int() for __idx0 in range(nr_class)]
        start[0] = 0
        ## for-while
        i = 1
        while i < nr_class:
            start[i] = start[i - 1] + count[i - 1]
            i += 1
        ## for-while
        i = 0
        while i < l:
            perm[start[data_label[i]]] = i
            start[data_label[i]] += 1
            i += 1
        start[0] = 0
        ## for-while
        i = 1
        while i < nr_class:
            start[i] = start[i - 1] + count[i - 1]
            i += 1
        nr_class_ret[0] = nr_class
        label_ret[0] = label
        start_ret[0] = start
        count_ret[0] = count

    @classmethod
    def svm_train(cls, prob, param):
        model = svm_model()
        model.param = param
        if (param.svm_type == svm_parameter.ONE_CLASS) or (param.svm_type == svm_parameter.EPSILON_SVR) or (param.svm_type == svm_parameter.NU_SVR):
            model.nr_class = 2
            model.label = None
            model.nSV = None
            model.probA = None
            model.probB = None
            model.sv_coef = [float() for __idx0 in range(1)]
            if (param.probability == 1) and (param.svm_type == svm_parameter.EPSILON_SVR) or (param.svm_type == svm_parameter.NU_SVR):
                model.probA = [float() for __idx0 in range(1)]
                model.probA[0] = cls.svm_svr_probability(prob, param)
            f = cls.svm_train_one(prob, param, 0, 0)
            model.rho = [float() for __idx0 in range(1)]
            model.rho[0] = f.rho
            nSV = 0
            i = 0
            ## for-while
            i = 0
            while i < prob.l:
                if abs(f.alpha[i]) > 0:
                    nSV += 1
                i += 1
            model.l = nSV
            model.SV = [svm_node() for __idx0 in range(nSV)]
            model.sv_coef[0] = [float() for __idx0 in range(nSV)]
            j = 0
            ## for-while
            i = 0
            while i < prob.l:
                if abs(f.alpha[i]) > 0:
                    model.SV[j] = prob.x[i]
                    model.sv_coef[0][j] = f.alpha[i]
                    j += 1
                i += 1
        else:
            l = prob.l
            tmp_nr_class = [int() for __idx0 in range(1)]
            tmp_label = [int() for __idx0 in range(1)]
            tmp_start = [int() for __idx0 in range(1)]
            tmp_count = [int() for __idx0 in range(1)]
            perm = [int() for __idx0 in range(l)]
            cls.svm_group_classes(prob, tmp_nr_class, tmp_label, tmp_start, tmp_count, perm)
            nr_class = tmp_nr_class[0]
            label = tmp_label[0]
            start = tmp_start[0]
            count = tmp_count[0]
            x = [svm_node() for __idx0 in range(l)]
            i = 0
            ## for-while
            i = 0
            while i < l:
                x[i] = prob.x[perm[i]]
                i += 1
            weighted_C = [float() for __idx0 in range(nr_class)]
            ## for-while
            i = 0
            while i < nr_class:
                weighted_C[i] = param.C
                i += 1
            ## for-while
            i = 0
            while i < param.nr_weight:
                j = 0
                ## for-while
                j = 0
                while j < nr_class:
                    if (param.weight_label[i] == label[j]):
                        break
                    j += 1
                if (j == nr_class):
#                    System.err.cls.print("warning: class label " + param.weight_label[i] + " specified in weight is not found\n")
                    print >> sys.stderr, "error", "warning: class label " + param.weight_label[i] + " specified in weight is not found\n"

                else:
                    weighted_C[j] *= param.weight[i]
                i += 1
            nonzero = [bool() for __idx0 in range(l)]
            ## for-while
            i = 0
            while i < l:
                nonzero[i] = False
                i += 1
            f = [cls.decision_function() for __idx0 in range(nr_class * nr_class - 1 / 2)]
            probA = None
            probB = None
            if (param.probability == 1):
                probA = [float() for __idx0 in range(nr_class * nr_class - 1 / 2)]
                probB = [float() for __idx0 in range(nr_class * nr_class - 1 / 2)]
            p = 0
            ## for-while
            i = 0
            while i < nr_class:
                ## for-while
                j = i + 1
                while j < nr_class:
                    sub_prob = svm_problem()
                    si = start[i]
                    sj = start[j]
                    ci = count[i]
                    cj = count[j]
                    sub_prob.l = ci + cj
                    sub_prob.x = [svm_node() for __idx0 in range(sub_prob.l)]
                    sub_prob.y = [float() for __idx0 in range(sub_prob.l)]
                    k = 0
                    ## for-while
                    k = 0
                    while k < ci:
                        sub_prob.x[k] = x[si + k]
                        sub_prob.y[k] = +1
                        k += 1
                    ## for-while
                    k = 0
                    while k < cj:
                        sub_prob.x[ci + k] = x[sj + k]
                        sub_prob.y[ci + k] = -1
                        k += 1
                    if (param.probability == 1):
                        probAB = [float() for __idx0 in range(2)]
                        cls.svm_binary_svc_probability(sub_prob, param, weighted_C[i], weighted_C[j], probAB)
                        probA[p] = probAB[0]
                        probB[p] = probAB[1]
                    f[p] = cls.svm_train_one(sub_prob, param, weighted_C[i], weighted_C[j])
                    ## for-while
                    k = 0
                    while k < ci:
                        if not nonzero[si + k] and abs(f[p].alpha[k]) > 0:
                            nonzero[si + k] = True
                        k += 1
                    ## for-while
                    k = 0
                    while k < cj:
                        if not nonzero[sj + k] and abs(f[p].alpha[ci + k]) > 0:
                            nonzero[sj + k] = True
                        k += 1
                    p += 1
                    j += 1
                i += 1
            model.nr_class = nr_class
            model.label = [int() for __idx0 in range(nr_class)]
            ## for-while
            i = 0
            while i < nr_class:
                model.label[i] = label[i]
                i += 1
            model.rho = [float() for __idx0 in range(nr_class * nr_class - 1 / 2)]
            ## for-while
            i = 0
            while i < nr_class * nr_class - 1 / 2:
                model.rho[i] = f[i].rho
                i += 1
            if (param.probability == 1):
                model.probA = [float() for __idx0 in range(nr_class * nr_class - 1 / 2)]
                model.probB = [float() for __idx0 in range(nr_class * nr_class - 1 / 2)]
                ## for-while
                i = 0
                while i < nr_class * nr_class - 1 / 2:
                    model.probA[i] = probA[i]
                    model.probB[i] = probB[i]
                    i += 1
            else:
                model.probA = None
                model.probB = None
            nnz = 0
            nz_count = [int() for __idx0 in range(nr_class)]
            model.nSV = [int() for __idx0 in range(nr_class)]
            ## for-while
            i = 0
            while i < nr_class:
                nSV = 0
                ## for-while
                j = 0
                while j < count[i]:
                    if nonzero[start[i] + j]:
                        nSV += 1
                        nnz += 1
                    j += 1
                model.nSV[i] = nSV
                nz_count[i] = nSV
                i += 1
            svm.cls.info("Total nSV = " + nnz + "\n")
            model.l = nnz
            model.SV = [svm_node() for __idx0 in range(nnz)]
            p = 0
            ## for-while
            i = 0
            while i < l:
                if nonzero[i]:
                    model.SV[p] = x[i]
                    p += 1
                i += 1
            nz_start = [int() for __idx0 in range(nr_class)]
            nz_start[0] = 0
            ## for-while
            i = 1
            while i < nr_class:
                nz_start[i] = nz_start[i - 1] + nz_count[i - 1]
                i += 1
            model.sv_coef = [float() for __idx0 in range(nr_class - 1)]
            ## for-while
            i = 0
            while i < nr_class - 1:
                model.sv_coef[i] = [float() for __idx0 in range(nnz)]
                i += 1
            p = 0
            ## for-while
            i = 0
            while i < nr_class:
                ## for-while
                j = i + 1
                while j < nr_class:
                    si = start[i]
                    sj = start[j]
                    ci = count[i]
                    cj = count[j]
                    q = nz_start[i]
                    k = 0
                    ## for-while
                    k = 0
                    while k < ci:
                        if nonzero[si + k]:
                            model.sv_coef[j - 1][q] = f[p].alpha[k]
                            q += 1
                        k += 1
                    q = nz_start[j]
                    ## for-while
                    k = 0
                    while k < cj:
                        if nonzero[sj + k]:
                            model.sv_coef[i][q] = f[p].alpha[ci + k]
                            q += 1
                        k += 1
                    p += 1
                    j += 1
                i += 1
        return model

    @classmethod
    def svm_cross_validation(cls, prob, param, nr_fold, target):
        i = 0
        fold_start = [int() for __idx0 in range(nr_fold + 1)]
        l = prob.l
        perm = [int() for __idx0 in range(l)]
        if (param.svm_type == svm_parameter.C_SVC) or (param.svm_type == svm_parameter.NU_SVC) and nr_fold < l:
            tmp_nr_class = [int() for __idx0 in range(1)]
            tmp_label = [int() for __idx0 in range(1)]
            tmp_start = [int() for __idx0 in range(1)]
            tmp_count = [int() for __idx0 in range(1)]
            cls.svm_group_classes(prob, tmp_nr_class, tmp_label, tmp_start, tmp_count, perm)
            nr_class = tmp_nr_class[0]
            label = tmp_label[0]
            start = tmp_start[0]
            count = tmp_count[0]
            fold_count = [int() for __idx0 in range(nr_fold)]
            c = 0
            index = [int() for __idx0 in range(l)]
            ## for-while
            i = 0
            while i < l:
                index[i] = perm[i]
                i += 1
            ## for-while
            c = 0
            while c < nr_class:
                ## for-while
                i = 0
                while i < count[c]:
                    j = i + random.random() * count[c] - i
                    _ = index[start[c] + j]
                    index[start[c] + j] = index[start[c] + i]
                    index[start[c] + i] = _
                    False
                    i += 1
                c += 1
            ## for-while
            i = 0
            while i < nr_fold:
                fold_count[i] = 0
                ## for-while
                c = 0
                while c < nr_class:
                    fold_count[i] += i + 1 * count[c] / nr_fold - i * count[c] / nr_fold
                    c += 1
                i += 1
            fold_start[0] = 0
            ## for-while
            i = 1
            while i <= nr_fold:
                fold_start[i] = fold_start[i - 1] + fold_count[i - 1]
                i += 1
            ## for-while
            c = 0
            while c < nr_class:
                ## for-while
                i = 0
                while i < nr_fold:
                    begin = start[c] + i * count[c] / nr_fold
                    end = start[c] + i + 1 * count[c] / nr_fold
                    ## for-while
                    j = begin
                    while j < end:
                        perm[fold_start[i]] = index[j]
                        fold_start[i] += 1
                        j += 1
                    i += 1
                c += 1
            fold_start[0] = 0
            ## for-while
            i = 1
            while i <= nr_fold:
                fold_start[i] = fold_start[i - 1] + fold_count[i - 1]
                i += 1
        else:
            ## for-while
            i = 0
            while i < l:
                perm[i] = i
                i += 1
            ## for-while
            i = 0
            while i < l:
                j = i + random.random() * l - i
                _ = perm[i]
                perm[i] = perm[j]
                perm[j] = _
                False
                i += 1
            ## for-while
            i = 0
            while i <= nr_fold:
                fold_start[i] = i * l / nr_fold
                i += 1
        ## for-while
        i = 0
        while i < nr_fold:
            begin = fold_start[i]
            end = fold_start[i + 1]
            j = 0
            k = 0
            subprob = svm_problem()
            subprob.l = l - end - begin
            subprob.x = [svm_node() for __idx0 in range(subprob.l)]
            subprob.y = [float() for __idx0 in range(subprob.l)]
            k = 0
            ## for-while
            j = 0
            while j < begin:
                subprob.x[k] = prob.x[perm[j]]
                subprob.y[k] = prob.y[perm[j]]
                k += 1
                j += 1
            ## for-while
            j = end
            while j < l:
                subprob.x[k] = prob.x[perm[j]]
                subprob.y[k] = prob.y[perm[j]]
                k += 1
                j += 1
            submodel = cls.svm_train(subprob, param)
            if (param.probability == 1) and (param.svm_type == svm_parameter.C_SVC) or (param.svm_type == svm_parameter.NU_SVC):
                prob_estimates = [float() for __idx0 in range(cls.svm_get_nr_class(submodel))]
                ## for-while
                j = begin
                while j < end:
                    target[perm[j]] = cls.svm_predict_probability(submodel, prob.x[perm[j]], prob_estimates)
                    j += 1
            else:
                ## for-while
                j = begin
                while j < end:
                    target[perm[j]] = cls.svm_predict(submodel, prob.x[perm[j]])
                    j += 1
            i += 1

    @classmethod
    def svm_get_svm_type(cls, model):
        return model.param.svm_type

    @classmethod
    def svm_get_nr_class(cls, model):
        return model.nr_class

    @classmethod
    def svm_get_labels(cls, model, label):
        if model.label is not None:
            ## for-while
            i = 0
            while i < model.nr_class:
                label[i] = model.label[i]
                i += 1

    @classmethod
    def svm_get_svr_probability(cls, model):
        if (model.param.svm_type == svm_parameter.EPSILON_SVR) or (model.param.svm_type == svm_parameter.NU_SVR) and model.probA is not None:
            return model.probA[0]
        else:
            #System.err.cls.print("Model doesn't contain information for SVR probability inference\n")
            print >> sys.stderr, "Error", "Model doesn't contain information for SVR probability inference\n"
            return 0

    @classmethod
    def svm_predict_values(cls, model, x, dec_values):
        if (model.param.svm_type == svm_parameter.ONE_CLASS) or (model.param.svm_type == svm_parameter.EPSILON_SVR) or (model.param.svm_type == svm_parameter.NU_SVR):
            sv_coef = model.sv_coef[0]
            sum = 0
            ## for-while
            i = 0
            while i < model.l:
                sum += sv_coef[i] * Kernel.k_function(x, model.SV[i], model.param)
                i += 1
            sum -= model.rho[0]
            dec_values[0] = sum
        else:
            i = 0
            nr_class = model.nr_class
            l = model.l
            kvalue = [float() for __idx0 in range(l)]
            ## for-while
            i = 0
            while i < l:
                kvalue[i] = Kernel.k_function(x, model.SV[i], model.param)
                i += 1
            start = [int() for __idx0 in range(nr_class)]
            start[0] = 0
            ## for-while
            i = 1
            while i < nr_class:
                start[i] = start[i - 1] + model.nSV[i - 1]
                i += 1
            p = 0
            ## for-while
            i = 0
            while i < nr_class:
                ## for-while
                j = i + 1
                while j < nr_class:
                    sum = 0
                    si = start[i]
                    sj = start[j]
                    ci = model.nSV[i]
                    cj = model.nSV[j]
                    k = 0
                    coef1 = model.sv_coef[j - 1]
                    coef2 = model.sv_coef[i]
                    ## for-while
                    k = 0
                    while k < ci:
                        sum += coef1[si + k] * kvalue[si + k]
                        k += 1
                    ## for-while
                    k = 0
                    while k < cj:
                        sum += coef2[sj + k] * kvalue[sj + k]
                        k += 1
                    sum -= model.rho[p]
                    dec_values[p] = sum
                    p += 1
                    j += 1
                i += 1

    @classmethod
    def svm_predict(cls, model, x):
        if (model.param.svm_type == svm_parameter.ONE_CLASS) or (model.param.svm_type == svm_parameter.EPSILON_SVR) or (model.param.svm_type == svm_parameter.NU_SVR):
            res = [float() for __idx0 in range(1)]
            cls.svm_predict_values(model, x, res)
            if (model.param.svm_type == svm_parameter.ONE_CLASS):
                return 1 if res[0] > 0 else -1
            else:
                return res[0]
        else:
            i = 0
            nr_class = model.nr_class
            dec_values = [float() for __idx0 in range(nr_class * nr_class - 1 / 2)]
            cls.svm_predict_values(model, x, dec_values)
            vote = [int() for __idx0 in range(nr_class)]
            ## for-while
            i = 0
            while i < nr_class:
                vote[i] = 0
                i += 1
            pos = 0
            ## for-while
            i = 0
            while i < nr_class:
                ## for-while
                j = i + 1
                while j < nr_class:
                    if dec_values[pos] > 0:
                        vote[i] += 1
                    else:
                        vote[j] += 1
                    pos += 1
                    j += 1
                i += 1
            vote_max_idx = 0
            ## for-while
            i = 1
            while i < nr_class:
                if vote[i] > vote[vote_max_idx]:
                    vote_max_idx = i
                i += 1
            return model.label[vote_max_idx]

    @classmethod
    def svm_predict_probability(cls, model, x, prob_estimates):
        if (model.param.svm_type == svm_parameter.C_SVC) or (model.param.svm_type == svm_parameter.NU_SVC) and model.probA is not None and model.probB is not None:
            i = 0
            nr_class = model.nr_class
            dec_values = [float() for __idx0 in range(nr_class * nr_class - 1 / 2)]
            cls.svm_predict_values(model, x, dec_values)
            min_prob = 1e-7
            pairwise_prob = [float() for __idx0 in range(nr_class)]
            k = 0
            ## for-while
            i = 0
            while i < nr_class:
                ## for-while
                j = i + 1
                while j < nr_class:
                    pairwise_prob[i][j] = min(max(cls.sigmoid_predict(dec_values[k], model.probA[k], model.probB[k]), min_prob), 1 - min_prob)
                    pairwise_prob[j][i] = 1 - pairwise_prob[i][j]
                    k += 1
                    j += 1
                i += 1
            cls.multiclass_probability(nr_class, pairwise_prob, prob_estimates)
            prob_max_idx = 0
            ## for-while
            i = 1
            while i < nr_class:
                if prob_estimates[i] > prob_estimates[prob_max_idx]:
                    prob_max_idx = i
                i += 1
            return model.label[prob_max_idx]
        else:
            return cls.svm_predict(model, x)

    svm_type_table = ["c_svc","nu_svc","one_class","epsilon_svr","nu_svr"]
    
    kernel_type_table = ["linear","polynomial","rbf","sigmoid","precomputed"]

    @classmethod
    def svm_save_model(cls, model_file_name, model):
#        fp = DataOutputStream(BufferedOutputStream(FileOutputStream(model_file_name)))
        raise NotImplementedError
        fp = None
        param = model.param
        fp.writeBytes("svm_type " + cls.svm_type_table[param.svm_type] + "\n")
        fp.writeBytes("kernel_type " + cls.kernel_type_table[param.kernel_type] + "\n")
        if (param.kernel_type == svm_parameter.POLY):
            fp.writeBytes("degree " + param.degree + "\n")
        if (param.kernel_type == svm_parameter.POLY) or (param.kernel_type == svm_parameter.RBF) or (param.kernel_type == svm_parameter.SIGMOID):
            fp.writeBytes("gamma " + param.gamma + "\n")
        if (param.kernel_type == svm_parameter.POLY) or (param.kernel_type == svm_parameter.SIGMOID):
            fp.writeBytes("coef0 " + param.coef0 + "\n")
        nr_class = model.nr_class
        l = model.l
        fp.writeBytes("nr_class " + nr_class + "\n")
        fp.writeBytes("total_sv " + l + "\n")
        fp.writeBytes("rho")
        ## for-while
        i = 0
        while i < nr_class * nr_class - 1 / 2:
            fp.writeBytes(" " + model.rho[i])
            i += 1
        fp.writeBytes("\n")
        if model.label is not None:
            fp.writeBytes("label")
            ## for-while
            i = 0
            while i < nr_class:
                fp.writeBytes(" " + model.label[i])
                i += 1
            fp.writeBytes("\n")
        if model.probA is not None:
            fp.writeBytes("probA")
            ## for-while
            i = 0
            while i < nr_class * nr_class - 1 / 2:
                fp.writeBytes(" " + model.probA[i])
                i += 1
            fp.writeBytes("\n")
        if model.probB is not None:
            fp.writeBytes("probB")
            ## for-while
            i = 0
            while i < nr_class * nr_class - 1 / 2:
                fp.writeBytes(" " + model.probB[i])
                i += 1
            fp.writeBytes("\n")
        if model.nSV is not None:
            fp.writeBytes("nr_sv")
            ## for-while
            i = 0
            while i < nr_class:
                fp.writeBytes(" " + model.nSV[i])
                i += 1
            fp.writeBytes("\n")
        fp.writeBytes("SV\n")
        sv_coef = model.sv_coef
        SV = model.SV
        ## for-while
        i = 0
        while i < l:
            ## for-while
            j = 0
            while j < nr_class - 1:
                fp.writeBytes(sv_coef[j][i] + " ")
                j += 1
            p = SV[i]
            if (param.kernel_type == svm_parameter.PRECOMPUTED):
                fp.writeBytes("0:" + p[0].value)
            else:
                ## for-while
                j = 0
                while j < p.length:
                    fp.writeBytes(p[j].index + ":" + p[j].value + " ")
                    j += 1
            fp.writeBytes("\n")
            i += 1
        fp.close()

    @classmethod
    def atof(cls, s):
#        return Double.valueOf(s).doubleValue()
        return float(s)

    @classmethod
    def atoi(cls, s):
#        return Integer.parseInt(s)
        return int(s)

    @classmethod
    def svm_model(cls, model_file_name):
#        fp = BufferedReader(FileReader(model_file_name))
        fp = open(model_file_name,'r')
        model = svm_model()
        param = svm_parameter()
        model.param = param
        model.rho = None
        model.probA = None
        model.probB = None
        model.label = None
        model.nSV = None
        while True:
            cmd = fp.readline().strip()
            arg = cmd[cmd.find(' ')+ 1:]
            if cmd.startswith("svm_type"):
                ## for-while
                i = 0
                while i < len(cls.svm_type_table):
                    if (arg.find(cls.svm_type_table[i]) != -1):
                        param.svm_type = i
                        break
                    i += 1
                if (i == len(cls.svm_type_table)):
                    print >> sys.stderr, "error", "unknown svm type.\n"
                    return
            elif cmd.startswith("kernel_type"):
                ## for-while
                i = 0
                while i < len(cls.kernel_type_table):
                    if (arg.find(cls.kernel_type_table[i]) != -1):
                        param.kernel_type = i
                        break
                    i += 1
                if (i == len(cls.kernel_type_table)):
                    print >> sys.stderr, "error", "unknown kernel function.\n"
                    return
            elif cmd.startswith("degree"):
                param.degree = cls.atoi(arg)
            elif cmd.startswith("gamma"):
                param.gamma = cls.atof(arg)
            elif cmd.startswith("coef0"):
                param.coef0 = cls.atof(arg)
            elif cmd.startswith("nr_class"):
                model.nr_class = cls.atoi(arg)
            elif cmd.startswith("total_sv"):
                model.l = cls.atoi(arg)
            elif cmd.startswith("rho"):
                n = model.nr_class * (model.nr_class - 1) / 2
                model.rho = [float() for __idx0 in range(n)]
                st = re.split('\s*', arg)
                ## for-while
                i = 0
                while i < n:
                    model.rho[i] = cls.atof(st.pop(0))
                    i += 1
            elif cmd.startswith("label"):
                n = model.nr_class
                model.label = [int() for __idx0 in range(n)]
                st = re.split('\s*', arg)
                ## for-while
                i = 0
                while i < n:
                    model.label[i] = cls.atoi(st.pop(0))
                    i += 1
            elif cmd.startswith("probA"):
                n = model.nr_class * (model.nr_class - 1) / 2
                model.probA = [float() for __idx0 in range(n)]
                st = re.split('\s*', arg)
                ## for-while
                i = 0
                while i < n:
                    model.probA[i] = cls.atof(st.pop(0))
                    i += 1
            elif cmd.startswith("probB"):
                n = model.nr_class * (model.nr_class - 1) / 2
                model.probB = [float() for __idx0 in range(n)]
                st = re.split('\s*', arg)
                ## for-while
                i = 0
                while i < n:
                    model.probB[i] = cls.atof(st.pop(0))
                    i += 1
            elif cmd.startswith("nr_sv"):
                n = model.nr_class
                model.nSV = [int() for __idx0 in range(n)]
                st = re.split('\s*', arg)
                ## for-while
                i = 0
                while i < n:
                    model.nSV[i] = cls.atoi(st.pop(0))
                    i += 1
            elif cmd.startswith("SV"):
                break
            else:
                #System.err.cls.print("unknown text in model file: [" + cmd + "]\n")
                print >> sys.stderr, "error", "unknown text in model file: [" + cmd + "]\n"
                return
        m = model.nr_class - 1
        l = model.l
        model.sv_coef = [[0 for __idx1 in range(l)] for __idx0 in range(m)]
        model.SV = [0 for __idx0 in range(l)]
        ## for-while
        i = 0
        while i < l:
            line = fp.readline()
#            st = StringTokenizer(line, " \t\n\r\f:")
            st = re.split('[\s:]*', line)
            ## for-while
            k = 0
            while k < m:
                model.sv_coef[k][i] = cls.atof(st.pop(0))
                k += 1
#            n = st.countTokens() / 2
            n = len(st) / 2
            model.SV[i] = [0 for __idx0 in range(n)]
            ## for-while
            j = 0
            while j < n:
                model.SV[i][j] = svm_node()
                model.SV[i][j].index = cls.atoi(st.pop(0))
                model.SV[i][j].value = cls.atof(st.pop(0))
                j += 1
            i += 1
        fp.close()
        return model

    @classmethod
    def svm_check_parameter(cls, prob, param):
        svm_type = param.svm_type
        if (svm_type != svm_parameter.C_SVC) and (svm_type != svm_parameter.NU_SVC) and (svm_type != svm_parameter.ONE_CLASS) and (svm_type != svm_parameter.EPSILON_SVR) and (svm_type != svm_parameter.NU_SVR):
            return "unknown svm type"
        kernel_type = param.kernel_type
        if (kernel_type != svm_parameter.LINEAR) and (kernel_type != svm_parameter.POLY) and (kernel_type != svm_parameter.RBF) and (kernel_type != svm_parameter.SIGMOID) and (kernel_type != svm_parameter.PRECOMPUTED):
            return "unknown kernel type"
        if param.degree < 0:
            return "degree of polynomial kernel < 0"
        if param.cache_size <= 0:
            return "cache_size <= 0"
        if param.eps <= 0:
            return "eps <= 0"
        if (svm_type == svm_parameter.C_SVC) or (svm_type == svm_parameter.EPSILON_SVR) or (svm_type == svm_parameter.NU_SVR):
            if param.C <= 0:
                return "C <= 0"
        if (svm_type == svm_parameter.NU_SVC) or (svm_type == svm_parameter.ONE_CLASS) or (svm_type == svm_parameter.NU_SVR):
            if param.nu <= 0 or param.nu > 1:
                return "nu <= 0 or nu > 1"
        if (svm_type == svm_parameter.EPSILON_SVR):
            if param.p < 0:
                return "p < 0"
        if (param.shrinking != 0) and (param.shrinking != 1):
            return "shrinking != 0 and shrinking != 1"
        if (param.probability != 0) and (param.probability != 1):
            return "probability != 0 and probability != 1"
        if (param.probability == 1) and (svm_type == svm_parameter.ONE_CLASS):
            return "one-class SVM probability output not supported yet"
        if (svm_type == svm_parameter.NU_SVC):
            l = prob.l
            max_nr_class = 16
            nr_class = 0
            label = [int() for __idx0 in range(max_nr_class)]
            count = [int() for __idx0 in range(max_nr_class)]
            i = 0
            ## for-while
            i = 0
            while i < l:
                this_label = prob.y[i]
                j = 0
                ## for-while
                j = 0
                while j < nr_class:
                    if (this_label == label[j]):
                        count[j] += 1
                        break
                    j += 1
                if (j == nr_class):
                    if (nr_class == max_nr_class):
                        max_nr_class *= 2
                        new_data = [int() for __idx0 in range(max_nr_class)]
                        #System.arraycopy(label, 0, new_data, 0, label.length)
                        array_copy(label, 0, new_data, 0, label.length)
                        label = new_data
                        new_data = [int() for __idx0 in range(max_nr_class)]
                        #System.arraycopy(count, 0, new_data, 0, count.length)
                        array_copy(count, 0, new_data, 0, count.length)
                        count = new_data
                    label[nr_class] = this_label
                    count[nr_class] = 1
                    nr_class += 1
                i += 1
            ## for-while
            i = 0
            while i < nr_class:
                n1 = count[i]
                ## for-while
                j = i + 1
                while j < nr_class:
                    n2 = count[j]
                    if param.nu * n1 + n2 / 2 > min(n1, n2):
                        return "specified nu is infeasible"
                    j += 1
                i += 1
        return

    @classmethod
    def svm_check_probability_model(cls, model):
        if (model.param.svm_type == svm_parameter.C_SVC) or (model.param.svm_type == svm_parameter.NU_SVC) and model.probA is not None and model.probB is not None or (model.param.svm_type == svm_parameter.EPSILON_SVR) or (model.param.svm_type == svm_parameter.NU_SVR) and model.probA is not None:
            return 1
        else:
            return 0

if __name__ == "__main__":
    import unittest
    class TestCase(unittest.TestCase):
        def _testLoadModel(self):
            print svm.svm_model("training/training.dat.model")
        
        def testPredict(self):
            model = svm.svm_model("training/training.dat.model")
            d = {1: 0.60000000000000009, 2: -0.46153846153846156, 12: -0.19999999999999996, 15: 1}
            print model.predict(d)
            
            d = {1: -0.19999999999999996, 2: -0.076923076923076872, 11: -1, 12: 0.050000000000000044, 10: -1}
            print model.predict(d)
            
            d = {2: -0.38461538461538458, 12: -0.25}
            print model.predict(d)
            
            
    
    unittest.main()


