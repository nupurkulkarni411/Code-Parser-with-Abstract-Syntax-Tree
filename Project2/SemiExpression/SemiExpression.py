from Project2.Tokenizer.Toker import Toker
from Project2.Interfaces import ITokCollection

class SemiExp(ITokCollection):
    _tokens = []
    _pToker = None

    def __init__(self,pToker):
        self._tokens = [] 
        self._pToker = pToker

    def __getitem__(self,n):
        if (n < 0 or n >= len(self._tokens)):
            raise Exception('index out of bound')
        return self._tokens[n]
    
    def merge(self,firstTok,secondTok):
        return True

    def getHelper(self,clear):
        if self._pToker is None:
            print ("No toker reference")
        if clear:
            self._tokens.clear()
        while True:
            token = self._pToker.getTok()
            if token == "":
                break
            while self.isComment(token):
                token = self._pToker.getTok()
                if token == "":
                    break
            self._tokens.append(token)
            if token == "{" or token == "}" or token == ";":
                return True
            if token == '\n' :
                l = self.find("#")
                if l < self.length():
                    return True
            if self.length() >= 2 :
                if token == ":" and (self._tokens[self.length() - 2] == "public" or self._tokens[self.length()- 2] == "private" or self._tokens[self.length() - 2] == "protected"):
                    return True
        return False

    def get(self,clear = True):
        issuccessful = self.getHelper(clear)
        if(len (self._tokens) == 0):
            return issuccessful
        if issuccessful and self._tokens[len (self._tokens) - 1] == ";":
            if self.isForLoop():
                issucessful = self.getHelper(False)
                if issuccessful:
                    issuccessful = self.getHelper(False)
                return issuccessful
        return issuccessful

    def merge(self,firstTok,secondTok):
        return True

    def push_back(self,tok):
        self._tokens.append(tok)

    def isComment(self,token):
        if len(token) > 1 :
            if token[0] == '/' and (token[1] == '/' or token[1] == '*') :
                return True
        return False

    def isForLoop(self):
        l1 = self.find("(")
        if l1 < self.length():
            l2 = self.find("for")
            if l2 < l1 :
                return True
        return False

    def length(self):
        return len (self._tokens)

    def show(self,showNewLines):
        if self.length() == 0:
            return ""
        temp = ""
        for i in range (0, len (self._tokens)) :
            if self._tokens[i] != '\n' or showNewLines:
                temp = temp + " "
                temp = temp + self._tokens[i]
        return temp

    def find(self,tok):
        i = 0
        while True:
            if i == len (self._tokens) or self._tokens[i] == tok:
                break
            else :
                i = i + 1
        return i

    def toLower(self):
        for i in range (0,self.length()):
            self._tokens[i] = self._tokens[i].lower()

    def trimFront(self):
        while self.length()>0 and (self._tokens[0] == "\n" or self._tokens[0] == " "):
            self.remove(0)


    def remove(self,tok):
        if type(tok) is str:
            i = self.find(tok)
            if i < len(self._tokens):
                del self._tokens[i]
                return True
            return False
        if type(tok) is int:
            if tok < 0 or len(self._tokens) <= tok:
                return False
            del self._tokens[tok]
            return True

    def currentLineCount(self):
        if self._pToker is None:
            return 0
        return self._pToker.currentLineCount()- 1



                
        
                    
                

    
    
