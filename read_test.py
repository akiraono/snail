#!/usr/bin/env python3
import sys
import sqlite3

class Cyrillic:
    def __init__(self, cyrillic):
        self.cyrillic = cyrillic
    def __str__(self):
        return self.cyrillic
    @staticmethod
    def isCyrillic(c):
        value = ord(c)
        if value >= 1040 and value <= 1103: # from a to ya
            return True
        if value == 1105 or value == 1025: # yo
            return True
        return False
    def lower(c):
        value = ord(c)
        if value >= 1040 and value <= 1071:
            value = value + 32
            #print(c,chr(value))
            return chr(value)
        elif value == 1025:
            return chr(1105)
        else:
            return c
    

class Word:
    def __init__(self,word):
        self.word = word
        self.cyrillics = []
        for i in range(len(self.word)):
            self.cyrillics.append( Cyrillic( self.word[i] ))
        #if self.isRussian(self.cyrillics):
        #    print(self.word + "\tis russian word")
        return
    def __str__(self):
        w = "".join(str(x) for x in self.cyrillics)
        if not self.isRussian(w):
            return w
        if self.isDBRegistered(self.lower(w)):
            return w
        return self.makeRed(w)
    def makeRed(self,data):
        return '\033[31m' + data + '\033[0m'
    def isRussian(self,chrs):
        for c in chrs:
            Cyrillic.lower(str(c))
            if not Cyrillic.isCyrillic(str(c)):
                return False
        return True
    def lower(self,chrs):
        result = []
        for c in chrs:
            result.append(Cyrillic.lower(str(c)))
        lowered = ''.join(result)
        #print(lowered)
        return lowered
    def isDBRegistered(self,word):
        conn = sqlite3.connect(sys.argv[1])
        cursor = conn.cursor()
        select_sql = 'select singular_nominative from noun where singular_nominative="' + word + '";'
        try:
            cursor.execute(select_sql)
            row = cursor.fetchone()
            #print(row)
        except sqlite3.Error as er:
            print(er)
        conn.close()
        if row is None:
            return False
        return True
        

class Sentence:
    def __init__(self,sentence):
        self.words = self.parseWords(sentence)
    def __str__(self):
        #print(self.words)
        s = " ".join(str(x) for x in self.words)
        #print(s)
        return s + "." # append period at end
    def removePeriod(self, sentence):
        index = sentence.find('.')
        stripped = sentence[0:index]
        return stripped
    def splitComma(self,sentence):
        return sentence.replace(","," ,")
    def parseWords(self, sentence):
        noperiod = self.removePeriod(sentence)
        split_comma = self.splitComma(noperiod)
        words = []
        chunks = split_comma.split(' ')
        #print(chunks)
        for c in chunks:
            words.append(Word(c))
        return words

class Chapter:
    def __init__(self,data):
        self.sentences = []
        while len(data)>0:
            first,data = self.split_by_period(data)
            self.sentences.append(Sentence(first))
    def split_by_period(self,data):
        index = data.find('.')
        if index >= 0:
            index += 1
            first_half = data[0:index]      # a sentence
            first_half = self.removeExtraSpace(first_half) # remove white space
            second_half = data[index:]      # result of chapter
            return first_half,second_half
        else:
            return data,''
    def getSentences(self):
        return self.sentences
    def removeExtraSpace(self,data):
        result = []
        datas = data.strip().split(' ')
        for d in datas:
            if len(d) > 0:
                result.append(d)
        return ' '.join(result)
        
        


def main():
    sentences = []
    f = open(sys.argv[2])
    for line in f:
        if len(line.rstrip()) == 0: # skip blank line
            continue
        chap = Chapter(line.rstrip())
        sentences.extend(chap.getSentences())
    f.close()
    for sentence in sentences:
        print(sentence)
    return


if __name__ == '__main__':
    main()
