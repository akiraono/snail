#!/usr/bin/python
import sys

class Feminine:
    def stem(self):
        return 'parent'

class Feminine23(Feminine):
    def stemx(self):
        return 'abc'

def main():
    fem = Feminine23()
    print(fem.stem())
    

if __name__ == '__main__':
    main()
