#!/usr/bin/env python3
import sys
import sqlite3
from cyrillic import CyrillicDB

db = CyrillicDB.CyrillicDB(sys.argv[1])

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
        if db.isRegistered(self.lower(word)):
            self.registered = True
        else:
            self.registered = False
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
        if self.registered:
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
    def isRegistered(self):
        return self.registered


        

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
    def words_count(self):
        return len(self.words)
    def registered_word_count(self):
        count = 0
        for w in self.words:
            if w.isRegistered():
                count += 1
        return count


        
class Text:
    def __init__(self, filename):
        self.wholetext = ''
        self.sentences = []
        f = open(filename)
        for line in f:
            self.wholetext += line.rstrip()
            self.wholetext += ' '
            #print(self.wholetext)
        f.close()
        data = self.wholetext
        while len(data)>0:
            first,data = self.split_by_period(data)
            self.sentences.append(Sentence(first))
        return
    def addSentence(self, s):
        self.sentences.append(s)
        return
    def __str__(self):
        r = ''
        for s in self.sentences:
            r += s.__str__() + ' '
        return r
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
    def removeExtraSpace(self,data):
        result = []
        datas = data.strip().split(' ')
        for d in datas:
            if len(d) > 0:
                result.append(d)
        return ' '.join(result)
    def words_stat(self):
        count = 0
        for s in self.sentences:
            count += s.words_count()
        dbcount = 0
        for s in self.sentences:
            dbcount += s.registered_word_count()
        ratio = float(dbcount)/count * 100
        return str(dbcount) + '/' + str(count) + '(' + str(round(ratio,2)) + '%)'



def main():
    text = Text(sys.argv[2])
    print(text)
    print('DB covered words = ',text.words_stat())
    #sentences = []
    #f = open(sys.argv[2])
    # for line in f:
    #     if len(line.rstrip()) == 0: # skip blank line
    #         continue
    #     chap = Chapter(line.rstrip())
    #     sentences.extend(chap.getSentences())
    # f.close()
    # for sentence in sentences:
    #     print(sentence)
    return


if __name__ == '__main__':
    main()
