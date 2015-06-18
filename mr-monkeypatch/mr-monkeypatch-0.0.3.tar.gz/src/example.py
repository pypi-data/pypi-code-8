#!/usr/bin/python

import monkeypatch as mp


@mp.monkeypatch
class ExampleClass(object):

    def __init__(self, val=0):
        self.val = val

    @mp.route(r'square_of_([0-9]+)')
    def squared(self, num):
        num = int(num)
        return self.val + num * num

    def original(self, num):
        return num


def main():
    a = ExampleClass(5)
    print a.square_of_2()
    print a.original(2)
    print a.squared(4)

if __name__ == '__main__':
    main()
