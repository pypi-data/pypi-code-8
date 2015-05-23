from string import ascii_lowercase


class itemid(object):

    def __init__(self, chars=None):
        if not chars:
            chars = "0123456789" + ascii_lowercase
        else:
            assert len(set(chars)) == len(chars), "Please remove duplicate character(s)"

        self.chars_map = dict(zip([c for c in chars], [i for i in xrange(len(chars))]))
        self.chars_map_reversed = dict(zip([i for i in xrange(len(chars))], [c for c in chars]))
        self.radix = len(chars)

    def shorten(self, value):
        if value < self.radix:
            return self.chars_map_reversed[value]

        output = []
        output = self._calc(value, output)
        output = [self.chars_map_reversed[i] for i in output][::-1]
        return ''.join(output)


    def unshorten(self, value):
        power = len(value) - 1
        total = 0
        for c in value:
            total += self.chars_map[c] * (self.radix**power)
            power -= 1
        return total

    def _calc(self, num, output):
        remainder = num % self.radix
        result = num / self.radix
        if result < self.radix:
            output.append(remainder)
            output.append(result)
        else:
            output.append(remainder)
            self._calc(result, output)
        return output
