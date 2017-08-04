#!/usr/bin/env python3
import sqlite3

class CyrillicDB:
    def __init__(self,dbname):
        self.data = {}
        self.conn = sqlite3.connect(dbname)
        self.cursor = self.conn.cursor()
        self.readData('select * from preposition;')
        self.readData('select * from noun;')
        self.readData('select * from verb;')
        self.readData('select * from adverb;')
        self.readData('select * from conjunction;')
        self.readData('select * from adjective;')
        return
    def readData(self, stmt):
        self.cursor.execute(stmt)
        list = self.cursor.fetchall()
        for row in list:
            for col in row:
                self.data[col] = 'registered'
    def isRegistered(self,word):
        if word in self.data:
            return True
        return False





if __name__ == '__main__':
    db = CyrillicDB('snailwords.db')
    print(db.isRegistered('от'))
    print(db.isRegistered('pencil'))
    


