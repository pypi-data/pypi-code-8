# Copyright (c) 2015 Tony Garnock-Jones <tonyg@leastfixedpoint.com>
# Copyright (c) 2015 Sean B. Palmer <inamidst.com>
# Licensed under the 2-Clause Simplified BSD License

def longest_common_subsequence(xs, ys):
    # Uses the Ukkonen-Myers algorithm
    t = len(xs) + len(ys)
    front = [0] * (2 * t + 1)
    candidates = [None] * (2 * t + 1)
    for d in range(t + 1):
        for k in range(-d, d+1, 2):
            if k == -d or (k != d and front[t + k - 1] < front[t + k + 1]):
                index = t + k + 1
                x = front[index]
            else:
                index = t + k - 1
                x = front[index] + 1
            y = x - k
            chain = candidates[index]
            while x < len(xs) and y < len(ys) and xs[x] == ys[y]:
                chain = ((x, y), chain)
                x += 1
                y += 1
            if x >= len(xs) and y >= len(ys):
                result = []
                while chain:
                    result.append(chain[0])
                    chain = chain[1]
                result.reverse()
                return result
            front[t + k] = x
            candidates[t + k] = chain

def diff(xs, ys):
    i = -1
    j = -1
    matches = longest_common_subsequence(xs, ys)
    matches.append((len(xs), len(ys)))
    result = []
    for (mi, mj) in matches:
        if mi - i > 1 or mj - j > 1:
            result.append((i + 1, xs[i + 1:mi], j + 1, ys[j + 1:mj]))
        i = mi
        j = mj
    return result

def patch(a, p, reverse=False):
    pat = {}
    for (ai, astr, bi, bstr) in p:
        if reverse is True:
            ai, astr, bi, bstr = bi, bstr, ai, astr
        if ai in pat:
           raise ValueError("Invalid patch")
        pat[ai] = (len(astr), bstr)

    i = 0
    parts = []
    while i < (len(a) + 1):
        skip, replacement = pat.get(i, (1, a[i:i+1]))
        parts.append(replacement)
        i += skip
        if skip == 0:
            del pat[i]
    return "".join(parts)

def example():
    a = "The red brown fox jumped over the rolling log"
    b = "The brown spotted fox leaped over the rolling log"
    print(patch(b, diff(a, b), True))
    print(patch(a, diff(a, b)))
    print(diff(a, b))

if __name__ == "__main__":
    example()
