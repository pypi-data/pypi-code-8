# coding: utf-8
"""
Copyright: Saito Tsutomu
License: Python Software Foundation License
"""
from __future__ import print_function, division

def addvar(lowBound=0, var_count=[0], *args, **kwargs):
    """変数作成用ユーティリティ"""
    from pulp import LpVariable
    var_count[0] += 1
    return LpVariable('v%d' % var_count[0], lowBound=lowBound, *args, **kwargs)

def min_node_cover(g):
    """
    最小頂点被覆問題
    入力
        g: グラフ
    出力
        頂点リスト
    """
    from networkx import maximal_independent_set
    return list(set(g.nodes()) - set(maximal_independent_set(g)))

def vrp(g, nv, capa):
    """
    運搬経路問題
    入力
        g: グラフ(node:demand, edge:cost)
        nv: 運搬車数
        capa: 運搬車容量
    出力
        頂点リスト
    """
    from pulp import LpProblem, LpBinary, lpDot, lpSum, value
    rv = range(nv)
    m = LpProblem()
    x = [{(i, j):addvar(cat=LpBinary) for i, j in g.edges()} for v in rv]
    w = [[addvar() for i in g.nodes()] for v in rv]
    m += lpSum(g.adj[i][j]['cost'] * lpSum(x[v][i, j] for v in rv) for i, j in g.edges())
    for v in rv:
        xv, wv = x[v], w[v]
        m += lpSum(xv[0, j] for j in g.nodes() if j) == 1
        for h in g.nodes():
            m += wv[h] <= capa
            m += lpSum(xv[i, j] for i, j in g.edges() if i == h) \
              == lpSum(xv[i, j] for i, j in g.edges() if j == h)
        for i, j in g.edges():
            if i == 0:
                m += wv[j] >= g.node[j]['demand'] - capa * (1 - xv[i, j])
            else:
                m += wv[j] >= wv[i] + g.node[j]['demand'] - capa * (1 - xv[i, j])
    for h in g.nodes()[1:]:
        m += lpSum(x[v][i, j] for v in rv for i, j in g.edges() if i == h) == 1
    if m.solve() != 1: return None
    return [[(i, j) for i, j in g.edges() if value(x[v][i, j]) > 0.5] for v in rv]

def tsp(point):
    """
    巡回セールスマン問題
        全探索
    入力
        point: 座標のリスト
    出力
        点番号リスト
    """
    from math import sqrt
    from itertools import permutations
    n = len(point)
    bst, mn, r = None, 1e100, range(1, n)
    for d in permutations(r):
        e = [point[i] for i in [0] + list(d) + [0]]
        s = sqrt(sum((e[i][0] - e[i + 1][0])**2
                   + (e[i][1] - e[i + 1][1])**2 for i in range(n)))
        if s < mn:
            mn = s
            bst = [0] + list(d)
    return bst

def set_covering(n, cand, is_partition=False):
    """
    集合被覆問題
    入力
        n: 要素数
        cand: 部分集合のリスト
    出力
        選択された部分集合の番号リスト
    """
    from pulp import LpProblem, LpBinary, lpDot, lpSum, value
    m = LpProblem()
    vv = [addvar(cat=LpBinary) for c in cand]
    m += lpDot([w for w, c in cand], vv) # obj func
    ee = [[] for j in range(n)]
    for v, (w, c) in zip(vv, cand):
        for k in c: ee[k].append(v)
    for e in ee:
        if e:
            if is_partition:
                m += lpSum(e) == 1
            else:
                m += lpSum(e) >= 1
    if m.solve() != 1: return None
    return [i for i, v in enumerate(vv) if value(v) > 0.5]

def set_partition(n, cand):
    """
    集合分割問題
    入力
        n: 要素数
        cand: 部分集合のリスト
    出力
        選択された部分集合の番号リスト
    """
    return set_covering(n, cand, True)

def one_machine_jobshop(p):
    """
    ジョンソン法
        2台のフローショップ型のジョブスケジュールを求める
    入力
        p: (前工程処理時間, 後工程処理時間)の製品ごとのリスト
    出力
        処理時間と処理順のリスト
    """
    from numpy import array, inf
    def proctime(p, l):
        n = len(p)
        t = [[0, 0] for i in range(n + 1)]
        for i in range(1, n + 1):
            t1, t2 = p[l[i - 1]]
            t[i][0] = t[i - 1][0] + t1
            t[i][1] = max(t[i - 1][1], t[i][0]) + t2
        return t[n][1]
    a, l1, l2 = array(p, dtype=float).flatten(), [], []
    for i in range(a.size // 2):
        j = a.argmin()
        k = j // 2
        if j % 2 == 0:
            l1.append(k)
        else:
            l2.append(k)
        a[2 * k] = a[2 * k + 1] = inf
    l = l1 + l2[::-1]
    return proctime(p, l), l

def shift_scheduling(ndy, nst, shift, proh, need):
    """
    勤務スケジューリング問題
    入力
        ndy: 日数
        nst: スタッフ数
        shift: シフト(1文字)のリスト
        proh: 禁止パターン(シフトの文字列)のリスト
        need: シフトごとの必要人数リスト(日ごと)
    出力
        日ごとスタッフごとのシフトの番号のテーブル
    """
    from pulp import LpProblem, LpBinary, lpDot, lpSum, value
    nsh = len(shift)
    rdy, rst, rsh = range(ndy), range(nst), range(nsh)
    dsh = {sh:k for k, sh in enumerate(shift)}
    m = LpProblem()
    v = [[[addvar(cat=LpBinary) for k in rsh] for j in rst] for i in rdy]
    for i in rdy:
        for j in rst:
            m += lpSum(v[i][j]) == 1
        for sh, dd in need.items():
            m += lpSum(v[i][j][dsh[sh]] for j in rst) >= dd[i]
    for prh in proh:
        n, pr = len(prh), [dsh[sh] for sh in prh]
        for j in rst:
            for i in range(ndy - n + 1):
                m += lpSum(v[i + h][j][pr[h]] for h in range(n)) <= n - 1
    if m.solve() != 1: return None
    return [[int(value(lpDot(rsh, v[i][j]))) for j in rst] for i in rdy]

def knapsack(size, weight, capacity):
    """
    ナップサック問題
        価値の最大化
    入力
        size: 荷物の大きさのリスト
        weight: 荷物の価値のリスト
        capacity: 容量
    出力
        ビンごとの荷物の大きさリスト
    """
    from pulp import LpProblem, LpMaximize, LpBinary, lpDot, lpSum, value
    m = LpProblem(sense=LpMaximize)
    v = [addvar(cat=LpBinary) for s in size]
    m += lpDot(weight, v)
    m += lpDot(size, v) <= capacity
    if m.solve() != 1: return None
    return [value(m.objective), [i for i in range(len(size)) if value(v[i]) > 0.5]]

def binpacking(c, w):
    """
    ビンパッキング問題
        列生成法で解く(近似解法)
    入力
        c: ビンの大きさ
        w: 荷物の大きさのリスト
    出力
        ビンごとの荷物の大きさリスト
    """
    from pulp import LpProblem, LpAffineExpression, \
         LpMinimize, LpMaximize, LpBinary, lpDot, lpSum, value
    n = len(w)
    rn = range(n)
    mkp = LpProblem('knapsack', LpMaximize) # 子問題
    mkpva = [addvar(cat=LpBinary) for i in rn]
    mkp.addConstraint(lpDot(w, mkpva) <= c)
    mdl = LpProblem('dual', LpMaximize) # 双対問題
    mdlva = [addvar() for i in rn]
    for i, v in enumerate(mdlva): v.w = w[i]
    mdl.setObjective(lpSum(mdlva))
    for i in rn:
        mdl.addConstraint(mdlva[i] <= 1)
    while True:
        mdl.solve()
        mkp.setObjective(lpDot([value(v) for v in mdlva], mkpva))
        mkp.solve()
        if mkp.status != 1 or value(mkp.objective) < 1 + 1e-6: break
        mdl.addConstraint(lpDot([value(v) for v in mkpva], mdlva) <= 1)
    nwm = LpProblem('primal', LpMinimize) # 主問題
    nm = len(mdl.constraints)
    rm = range(nm)
    nwmva = [addvar(cat=LpBinary) for i in rm]
    nwm.setObjective(lpSum(nwmva))
    dict = {}
    for v, q in mdl.objective.items():
        dict[v] = LpAffineExpression() >= q
    const = list(mdl.constraints.values())
    for i, q in enumerate(const):
        for v in q:
            dict[v].addterm(nwmva[i], 1)
    for q in dict.values(): nwm.addConstraint(q)
    nwm.solve()
    if nwm.status != 1: return None
    w0, result = list(w), [[] for i in range(len(const))]
    for i, va in enumerate(nwmva):
        if value(va) < 0.5: continue
        for v in const[i]:
            if v.w in w0:
                w0.remove(v.w)
                result[i].append(v.w)
    return [r for r in result if r]

class TwoDimPacking:
    """
    2次元パッキング
        ギロチンカットで元板からアイテムを切り出す(近似解法)
    入力
        width, height: 元板の大きさ
        items: アイテムの(横,縦)のリスト
    出力
        容積率と入ったアイテムの(横,縦,x,y)のリスト
    """
    def __init__(self, width, height, items=None):
        self.width = width
        self.height = height
        self.items = items
    @staticmethod
    def calc(pp, w, h):
        plw, plh, ofw, ofh = pp
        if w > plw or h > plh: return None
        if w * (plh - h) <= h * (plw - w):
            return (w * (plh - h), (w, plh - h, ofw, ofh + h), (plw - w, plh, ofw + w, ofh))
        else: return (h * (plw - w), (plw - w, h, ofw + w, ofh), (plw, plh - h, ofw, ofh + h))
    def solve(self, iters=100):
        from random import shuffle, seed
        bst, self.pos = 0, []
        seed(1)
        for cnt in range(iters):
            tmp, szs, plates = [], list(self.items), [(self.width, self.height, 0, 0)]
            shuffle(szs)
            while len(szs) > 0 and len(plates) > 0:
                mni, mnr, (w, h), szs = -1, [1e9], szs[0], szs[1:]
                for i in range(len(plates)):
                    res = TwoDimPacking.calc(plates[i], w, h)
                    if res and res[0] < mnr[0]: mni, mnr = i, res
                if mni >= 0:
                    tmp.append((w, h) + plates[i][2:])
                    plates[i:i + 1] = [p for p in mnr[1: 3] if p[0] * p[1] > 0]
            sm = sum(r[0] * r[1] for r in tmp)
            if sm > bst: bst, self.result = sm, tmp
        self.rate = bst / self.width / self.height
        return self.rate, self.result

def facility_location(p, point, cand=None):
    """
    施設配置問題
        P-メディアン問題：総距離の和の最小化
    入力
        p: 施設数上限
        point: 顧客位置のリスト
        cand: 施設候補位置のリスト
    出力
        顧客ごとの施設番号リスト
    """
    from math import sqrt
    from pulp import LpProblem, LpBinary, lpDot, lpSum, value
    if not cand: cand = point
    rp, rc = range(len(point)), range(len(cand))
    m = LpProblem()
    x = [[addvar(cat=LpBinary) for c in cand] for p in point]
    y = [addvar(cat=LpBinary) for c in cand]
    m += lpSum(x[i][j] * sqrt((point[i][0] - cand[j][0])**2
                            + (point[i][1] - cand[j][1])**2) for i in rp for j in rc)
    m += lpSum(y) <= p
    for i in rp:
        m += lpSum(x[i]) == 1
        for j in rc:
            m += x[i][j] <= y[j]
    if m.solve() != 1: return None
    return [int(value(lpDot(rc, x[i]))) for i in rp]

def quad_assign(quant, dist):
    """
    2次割当問題
        全探索
    入力
        quant: 対象間の輸送量
        dist: 割当先間の距離
    出力
        対象ごとの割当先番号リスト
    """
    from itertools import permutations
    n = len(quant)
    bst, mn, r = None, 1e100, range(n)
    for d in permutations(r):
        s = sum(quant[i][j] * dist[d[i]][d[j]] for i in r for j in r if j != i)
        if s < mn:
            mn = s
            bst = d
    return bst

def gap(cst, req, cap):
    """
    一般化割当問題
        費用最小の割当を解く
    入力
        cst: エージェントごと、ジョブごとの費用のテーブル
        req: エージェントごと、ジョブごとの要求量のテーブル
        cap: エージェントの容量のリスト
    出力
        ジョブごとのエージェント番号リスト
    """
    from pulp import LpProblem, LpBinary, lpDot, lpSum, value
    na, nj = len(cst), len(cst[0])
    m = LpProblem()
    v = [[addvar(cat=LpBinary) for j in range(nj)] for i in range(na)]
    m += lpSum(lpDot(cst[i], v[i]) for i in range(na))
    for i in range(na):
        m += lpDot(req[i], v[i]) <= cap[i]
    for j in range(nj):
        m += lpSum(v[i][j] for i in range(na)) == 1
    if m.solve() != 1: return None
    return [int(value(lpDot(range(na), [v[i][j] for i in range(na)]))) for j in range(nj)]




