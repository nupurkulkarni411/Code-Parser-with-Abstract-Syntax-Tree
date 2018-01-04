#import string

"""class Context:
    token = ""
    _pIn = None
    _sSpecialChar = ['{','}','[',']','(',')','<','>',':','=','+','-','*','\n','.']
    _specialCharP = ["<<",">>","+=","-=","*=","!=","::","==","++","/="]
    prevChar = None
    currChar = None
    _returncomments = True
    _lineCount = 0
    _pState = None
    _pEatWhitespace = None
    _pEatCComment = None
    _pEatCppComment = None
    _pEatSpecialTokens = None
    _pEatPunctuator = None
    _pEatAlphanum = None
    _pEatQuotedString = None
    EOF = False
    _pInlen = 0
    filepointer = 0
    first_ctor = True

    def __init__(self):
        if(Context.first_ctor):
            Context.first_ctor = False
            Context._lineCount = 1
            Context.filepointer = 0
            Context.EOF = False
            Context._pInlen = 0
            Context._returncomments = False
            Context._pEatWhitespace = EatWhitespace()
            Context._pEatCComment = EatCComment()
            Context._pEatCppComment = EatCppComment()
            Context._pEatSpecialTokens = EatSpecialTokens()
            Context._pEatPunctuator = EatPunctuator()
            Context._pEatAlphanum = EatAlphanum()
            Context._pEatQuotedString = EatQuotedString()
            Context._pState = Context._pEatWhitespace

class ConsumeState:
    token = ""
    _pIn = None
    _sSpecialChar = ['{','}','[',']','(',')','<','>',':','=','+','-','*','\n','.']
    _specialCharP = ["<<",">>","+=","-=","*=","!=","::","==","++","/="]
    prevChar = None
    currChar = None
    _returncomments = True
    _lineCount = 0
    _pState = None
    _pEatWhitespace = None
    _pEatCComment = None
    _pEatCppComment = None
    _pEatSpecialTokens = None
    _pEatPunctuator = None
    _pEatAlphanum = None
    _pEatQuotedString = None
    EOF = False
    _pInlen = 0
    filepointer = 0
    first_ctor = True
    _pContext = None

    def __init__(self):
        if(ConsumeState.first_ctor):
            ConsumeState.first_ctor = False
            ConsumeState._returncomments = True
            ConsumeState.filepointer = 0
            ConsumeState.EOF = False
            ConsumeState._pInlen = 0
            ConsumeState._pEatWhitespace = EatWhitespace()
            ConsumeState._pEatCComment = EatCComment()
            ConsumeState._pEatCppComment = EatCppComment()
            ConsumeState._pEatSpecialTokens = EatSpecialTokens()
            ConsumeState._pEatPunctuator = EatPunctuator()
            ConsumeState._pEatAlphanum = EatAlphanum()
            ConsumeState._pEatQuotedString = EatQuotedString()
            ConsumeState._pState = ConsumeState._pEatWhitespace
            ConsumeState._lineCount = 1

    def setContext(self,pContext):
        ConsumeState._pContext = pContext
        print(ConsumeState._pContext)

    def set_pInlen(self,_pIn):
        self._pContext._pInlen = len(_pIn)

    def setSpecialSingleChars(self,ssc):
        self._pContext._sSpecialChar.clear()
        for i in range (0,len(ssc)-1,2):
            if ssc[i] != ',':
                temp = ""
                temp = temp + ssc[i]
                self._pContext._sSpecialChar.append(temp)

    def setSpecialCharPairs(self,scp):
        self._pContext._specialCharP.clear()
        for i in range(0,len(scp)-1):
            if scp[i] != ',':
                temp = ""
                temp = temp + scp[i]
                i = i + 1
                temp = temp + scp[i]
                self._pContext._specialCharP.append(temp)        
     
    def returnComments(self,returnComments):
        self._pContext._returncomments = returnComments

    def getTok(self):
        return self._pContext.token
    
    def hasTok(self):
        return len(self._pContext.token) > 0
    
    def reset(self):
        self._pContext.filepointer  = 0
        self._pContext._pIn = None
            
    def checkSpecialSingleChar(self):
        for i in range(0,len(self._pContext._sSpecialChar)):
            if(self._pContext._sSpecialChar[i] == self._pContext.currChar):
                return True
        return False

    def checkSpecialDoubleChar(self):
        if self._pContext.filepointer == self._pContext._pInlen - 1:
            return False
        chNext = self._pContext._pIn[ConsumeState._pContext.filepointer+1]
        chPair = self._pContext.currChar + chNext
        for i in range(0,len(self._pContext._specialCharP)):
            if(self._pContext._specialCharP[i] == chPair):
                return True
        return False

    def attach (self,_pIn):
        self._pContext._pIn = _pIn
        self.set_pInlen(_pIn)

    def canRead(self):
        if self._pContext.filepointer == self._pContext._pInlen:
            return False
        else:
            return True
   
    def consumeChars(self):
        self._pContext._pState.eatChars()
        self._pContext._pState = self.nextState()

    def nextState(self):
        if self._pContext._pIn is None:
            self._pContext.filepointer = self._pContext.filepointer + 1
            self._pContext.EOF = True
            return None
        if self._pContext.filepointer == self._pContext._pInlen - 1:
            chNext = None
        else:
            chNext = self._pContext._pIn[self._pContext.filepointer + 1]
        if chNext is None:
            self._pContext._pIn = None
        if ((self._pContext.currChar == ' ' or self._pContext.currChar == '\t') and self._pContext.currChar != '\n'):
            return self._pContext._pEatWhitespace
        if (self._pContext.currChar == '/' and chNext == '*'):
            return self._pContext._pEatCComment
        if (self._pContext.currChar == '/' and chNext == '/'):
            return self._pContext._pEatCppComment
        if (self._pContext.currChar == '\n' or self.checkSpecialSingleChar(self) or self.checkSpecialDoubleChar(self)):
            return self._pContext._pEatSpecialTokens
        if (self._pContext.currChar == '"' or self._pContext.currChar == '\''):
            return self._pContext._pEatQuotedString
        if (self._pContext.currChar.isalnum() or self._pContext.currChar == '_'):
            return self._pContext._pEatAlphanum
        if (self.ispunct(self,self._pContext.currChar)):
            return self._pContext._pEatPunctuator
        if self._pContext._pIn is None:
            self._pContext.EOF = True
            return self._pContext._pEatWhitespace
        else:
            print ("Invalid Type Error")


    def ispunct(self,char):
        if(char in string.punctuation):
            return True
        return False

    def setContext(self,pContext):
        self._pContext = pContext

    def currentLineCount(self):
        return self._pContext._lineCount

    def getChar(self):
        self._pContext.prevChar = self._pContext.currChar
        if self._pContext.currChar == '\n':
            self._pContext._lineCount = self._pContext._lineCount + 1
        return self._pContext._pIn[self._pContext.filepointer]


class EatWhitespace(ConsumeState):
    def __init__(self):
        ConsumeState.__init__(self)
    
    def eatChars(self):
        #print ("state:eatWhitespace")
        print(ConsumeState._pContext)
        ConsumeState._pContext.token = ""
        while True:
            if ConsumeState._pContext._pIn is None or ConsumeState._pContext.filepointer == ConsumeState._pContext._pInlen - 1:
                ConsumeState._pContext._pIn = None
                return
            ConsumeState._pContext.currChar = ConsumeState.getChar()
            if ((ConsumeState._pContext.currChar != ' ' and ConsumeState._pContext.currChar != '\t') or ConsumeState._pContext.currChar == '\n'):
                return
            else:
                ConsumeState._pContext.filepointer = ConsumeState._pContext.filepointer + 1


class EatCComment(ConsumeState):
    def __init__(self):
        ConsumeState.__init__(self)
            
    def eatChars(self):
        #print("state:eatCComment")
        ConsumeState._pContext.token = ""
        while True:
            if(ConsumeState._pContext._returncomments):
                ConsumeState._pContext.token = ConsumeState._pContext.token + ConsumeState._pContext.currChar
            if(not ConsumeState._pContext._pIn):
                return
            ConsumeState._pContext.filepointer = ConsumeState._pContext.filepointer + 1
            ConsumeState._pContext.currChar = ConsumeState.getChar()
            if ConsumeState._pContext.currChar == '*' and ConsumeState._pContext._pIn[ConsumeState._pContext.filepointer + 1] == '/':
                break
        if(ConsumeState._pContext._returncomments):
            ConsumeState._pContext.token = ConsumeState._pContext.token + ConsumeState._pContext.currChar
        ConsumeState._pContext.filepointer = ConsumeState._pContext.filepointer + 1
        ConsumeState._pContext.currChar = CosumeState.getChar()
        if(ConsumeState._pContext._returncomments):
            ConsumeState._pContext.token = ConsumeState._pContext.token + ConsumeState._pContext.currChar
        if ConsumeState._pContext._pIn is None or ConsumeState._pContext.filepointer == ConsumeState._pContext._pInlen - 1:
            ConsumeState._pContext._pIn = None
            return
        ConsumeState._pContext.filepointer = ConsumeState._pContext.filepointer + 1
        ConsumeState._pContext.currChar = ConsumeState.getChar()
        ConsumeState._pContext.filepointer = ConsumeState._pContext.filepointer - 1
        

class EatCppComment(ConsumeState):
    def __init__(self):
        ConsumeState.__init__(self)
        
    def eatChars(self):
        #print ("state:eatCppComment")
        ConsumeState._pContext.token = ""
        while True:
            if(ConsumeState._pContext._returncomments):
                ConsumeState._pContext.token = ConsumeState._pContext.token + ConsumeState._pContext.currChar
            if ConsumeState._pContext._pIn is None or ConsumeState._pContext.filepointer == ConsumeState._pContext._pInlen - 1:
                ConsumeState._pContext._pIn = None
                return
            ConsumeState._pContext.filepointer = ConsumeState._pContext.filepointer + 1
            ConsumeState._pContext.currChar = ConsumeState.getChar()
            if (ConsumeState.currChar == '\n'):
                return

    

class EatSpecialTokens(ConsumeState):
    def __init__(self):
        ConsumeState.__init__(self)

    def eatChars(self):
        #print ("state:eatSpecialTokens")
        ConsumeState._pContext.token = ""
        if(ConsumeState.checkSpecialDoubleChar(self)):
            ConsumeState._pContext.token = ConsumeState._pContext.token + ConsumeState._pContext.currChar
            ConsumeState._pContext.filepointer = ConsumeState._pContext.filepointer + 1
            ConsumeState._pContext.currChar = ConsumeState.getChar()
            ConsumeState._pContext.token = ConsumeState._pContext.token + ConsumeState._pContext.currChar
        else:
            ConsumeState._pContext.token = ConsumeState._pContext.token + ConsumeState._pContext.currChar
        if ConsumeState._pContext._pIn is None or ConsumeState._pContext.filepointer == ConsumeState._pContext._pInlen - 1:
            ConsumeState._pContext._pIn = None
            return
        ConsumeState._pContext.filepointer = ConsumeState._pContext.filepointer + 1
        ConsumeState._pContext.currChar = ConsumeState.getChar()


class EatQuotedString(ConsumeState):
    def __init__(self):
        ConsumeState.__init__(self)

    def eatChars(self):
        #print ("state:eatQuotedString")
        quotation = ConsumeState._pContext.currChar
        ConsumeState._pContext.token = ""
        while True:
            chNext = ConsumeState._pContext._pIn[ConsumeState._pContext.filepointer+1]
            if (ConsumeState._pContext.currChar == '\\' and (chNext == quotation or chNext == '\\')):
                ConsumeState._pContext.token = ConsumeState._pContext.token + ConsumeState._pContext.currChar
                ConsumeState._pContext.filepointer = ConsumeState._pContext.filepointer + 1
                ConsumeState._pContext.currChar = ConsumeState.getChar()
                ConsumeState._pContext.token = ConsumeState._pContext.token + ConsumeState._pContext.currChar
                ConsumeState._pContext.filepointer = ConsumeState._pContext.filepointer + 1
                ConsumeState._pContext.currChar = ConsumeState.getChar()
            else:
                ConsumeState._pContext.token = ConsumeState._pContext.token + ConsumeState._pContext.currChar
                if (not ConsumeState._pContext._pIn):
                    return
                ConsumeState._pContext.filepointer = ConsumeState._pContext.filepointer + 1
                ConsumeState._pContext.currChar = ConsumeState._pContext.getChar()
            if (ConsumeState._pContext.currChar == quotation):
                ConsumeState._pContext.token = ConsumeState._pContext.token + ConsumeState._pContext.currChar
                break
        if ConsumeState._pContext._pIn is None or ConsumeState._pContext.filepointer == ConsumeState._pContext._pInlen - 1:
            ConsumeState._pContext._pIn = None
            return
        ConsumeState._pContext.filepointer = ConsumeState._pContext.filepointer + 1
        ConsumeState._pContext.currChar = ConsumeState.getChar()

class EatPunctuator(ConsumeState):
    def __init__(self):
        ConsumeState.__init__(self)
        
    def eatChars(self):
        #print ("state:eatPunctuator")
        ConsumeState._pContext.token = ""
        while True:
            ConsumeState._pContext.token = ConsumeState._pContext.token + ConsumeState._pContext.currChar
            if ConsumeState._pContext._pIn is None or ConsumeState._pContext.filepointer == ConsumeState._pContext._pInlen - 1:
                ConsumeState._pContext._pIn = None
                return
            ConsumeState._pContext.filepointer = ConsumeState._pContext.filepointer + 1
            ConsumeState._pContext.currChar = ConsumeState.getChar()
            if (not ConsumeState.ispunct(self,ConsumeState._pContext.currChar) or ConsumeState.checkSpecialSingleChar(self) or ConsumeState.checkSpecialDoubleChar(self) or ConsumeState._pContext.currChar == '"' or ConsumeState._pContext.currChar == '\''):
                return 

class EatAlphanum(ConsumeState):
    def __init__(self):
        ConsumeState.__init__(self)

    def eatChars(self):
        #print ("state:eatAlphanumeric")
        ConsumeState._pContext.token = ""
        while True:
            ConsumeState._pContext.token = ConsumeState._pContext.token + ConsumeState._pContext.currChar
            if ConsumeState._pContext._pIn is None or ConsumeState._pContext.filepointer == ConsumeState._pContext._pInlen - 1:
                ConsumeState._pContext._pIn = None
                return
            ConsumeState._pContext.filepointer = ConsumeState._pContext.filepointer + 1
            ConsumeState._pContext.currChar = ConsumeState.getChar()
            if (not ConsumeState._pContext.currChar.isalnum()):
                break"""


import string

class ConsumeState:
    token = ""
    _pIn = None
    prevChar = None
    currChar = None
    _returncomments = True
    _sSpecialChar = ['{','}','[',']','(',')','<','>',':','=','+','-','*','\n','.']
    _specialCharP = ["<<",">>","+=","-=","*=","!=","::","==","++","/="]
    first_ctor = True
    filepointer = 0
    _pState = None
    _pEatWhitespace = None
    _pEatCComment = None
    _pEatCppComment = None
    _pEatSpecialTokens = None
    _pEatPunctuator = None
    _pEatAlphanum = None
    _pEatQuotedString = None
    EOF = False
    _pInlen = 0
    _lineCount = 0

    def getChar(self):
        ConsumeState.prevChar = ConsumeState.currChar
        if ConsumeState.currChar == '\n':
            ConsumeState._lineCount = ConsumeState._lineCount + 1
        return ConsumeState._pIn[ConsumeState.filepointer]

    def currentLineCount(self):
        return ConsumeState._lineCount 

    def set_pInlen(self,_pIn):
        ConsumeState._pInlen = len(_pIn)

    def setSpecialSingleChars(self,ssc):
        self._sSpecialChar.clear()
        for i in range (0,len(ssc)-1,2):
            if ssc[i] != ',':
                temp = ""
                temp = temp + ssc[i]
                self._sSpecialChar.append(temp)

    def setSpecialCharPairs(self,scp):
        self._specialCharP.clear()
        for i in range(0,len(scp)-1):
            if scp[i] != ',':
                temp = ""
                temp = temp + scp[i]
                i = i + 1
                temp = temp + scp[i]
                self._specialCharP.append(temp)
        
    def __init__(self):
        if(ConsumeState.first_ctor):
            ConsumeState.first_ctor = False
            ConsumeState._returncomments = True
            ConsumeState.filepointer = 0
            ConsumeState.EOF = False
            ConsumeState._pInlen = 0
            ConsumeState._pEatWhitespace = EatWhitespace()
            ConsumeState._pEatCComment = EatCComment()
            ConsumeState._pEatCppComment = EatCppComment()
            ConsumeState._pEatSpecialTokens = EatSpecialTokens()
            ConsumeState._pEatPunctuator = EatPunctuator()
            ConsumeState._pEatAlphanum = EatAlphanum()
            ConsumeState._pEatQuotedString = EatQuotedString()
            ConsumeState._pState = ConsumeState._pEatWhitespace
            ConsumeState._lineCount = 1
            
    def returnComments(self,returnComments):
        self._returncomments = returnComments

    def getTok(self):
        return self.token
    
    def hasTok(self):
        return len(self.token) > 0
    
    def reset(self):
        ConsumeState.first_ctor = True
        ConsumeState.filepointer  = 0
        ConsumeState._pIn = None
            
    def checkSpecialSingleChar(self):
        for i in range(0,len(ConsumeState._sSpecialChar)):
            if(ConsumeState._sSpecialChar[i] == ConsumeState.currChar):
                return True
        return False

    def checkSpecialDoubleChar(self):
        if ConsumeState.filepointer == ConsumeState._pInlen - 1:
            return False
        chNext = ConsumeState._pIn[ConsumeState.filepointer+1]
        chPair = ConsumeState.currChar + chNext
        for i in range(0,len(ConsumeState._specialCharP)):
            if(ConsumeState._specialCharP[i] == chPair):
                return True
        return False

    def attach (self,_pIn):
        ConsumeState._pIn = _pIn
        self.set_pInlen(_pIn)

    def canRead(self):
        if ConsumeState.filepointer == ConsumeState._pInlen:
            return False
        else:
            return True
   
    def consumeChars(self):
        ConsumeState._pState.eatChars()
        ConsumeState._pState = self.nextState()

    def nextState(self):
        if ConsumeState._pIn is None:
            ConsumeState.filepointer = ConsumeState.filepointer + 1
            ConsumeState.EOF = True
            return None
        if ConsumeState.filepointer == ConsumeState._pInlen - 1:
            chNext = None
        else:
            chNext = ConsumeState._pIn[ConsumeState.filepointer + 1]
        if chNext is None:
            ConsumeState._pIn = None
        if ((ConsumeState.currChar == ' ' or ConsumeState.currChar == '\t') and ConsumeState.currChar != '\n'):
            return ConsumeState._pEatWhitespace
        if (ConsumeState.currChar == '/' and chNext == '*'):
            return ConsumeState._pEatCComment
        if (ConsumeState.currChar == '/' and chNext == '/'):
            return ConsumeState._pEatCppComment
        if (ConsumeState.currChar == '\n' or ConsumeState.checkSpecialSingleChar(self) or ConsumeState.checkSpecialDoubleChar(self)):
            return ConsumeState._pEatSpecialTokens
        if (ConsumeState.currChar == '"' or ConsumeState.currChar == '\''):
            return ConsumeState._pEatQuotedString
        if (ConsumeState.currChar.isalnum() or ConsumeState.currChar == '_'):
            return ConsumeState._pEatAlphanum
        if (ConsumeState.ispunct(self,ConsumeState.currChar)):
            return ConsumeState._pEatPunctuator
        if ConsumeState._pIn is None:
            ConsumeState.EOF = True
            return ConsumeState._pEatWhitespace
        else:
            print ("Invalid Type Error")

    def reset(self):
        ConsumeState.first_ctor = True
        
            
    def ispunct(self,char):
        if(char in string.punctuation):
            return True
        return False


class EatWhitespace(ConsumeState):
    def __init__(self):
        ConsumeState.__init__(self)
    def eatChars(self):
        #print ("state:eatWhitespace")
        ConsumeState.token = ""
        while True:
            if ConsumeState._pIn is None or ConsumeState.filepointer == ConsumeState._pInlen - 1:
                ConsumeState._pIn = None
                return
            ConsumeState.currChar = ConsumeState.getChar(self)
            if ((ConsumeState.currChar != ' ' and ConsumeState.currChar != '\t') or ConsumeState.currChar == '\n'):
                return
            else:
                ConsumeState.filepointer = ConsumeState.filepointer + 1


class EatCComment(ConsumeState):
    def __init__(self):
        ConsumeState.__init__(self)
            
    def eatChars(self):
        #print("state:eatCComment")
        ConsumeState.token = ""
        while True:
            if(ConsumeState._returncomments):
                ConsumeState.token = ConsumeState.token + ConsumeState.currChar
            if(not ConsumeState._pIn):
                return
            ConsumeState.filepointer = ConsumeState.filepointer + 1
            ConsumeState.currChar = ConsumeState.getChar(self)
            if ConsumeState.currChar == '*' and ConsumeState._pIn[ConsumeState.filepointer + 1] == '/':
                break
        if(ConsumeState._returncomments):
            ConsumeState.token = ConsumeState.token + ConsumeState.currChar
        ConsumeState.filepointer = ConsumeState.filepointer + 1
        ConsumeState.currChar = ConsumeState.getChar(self)
        if(ConsumeState._returncomments):
            ConsumeState.token = ConsumeState.token + ConsumeState.currChar
        if ConsumeState._pIn is None or ConsumeState.filepointer == ConsumeState._pInlen - 1:
            ConsumeState._pIn = None
            return
        ConsumeState.filepointer = ConsumeState.filepointer + 1
        ConsumeState.currChar = ConsumeState.getChar(self)
        ConsumeState.filepointer = ConsumeState.filepointer - 1
        

class EatCppComment(ConsumeState):
    def __init__(self):
        ConsumeState.__init__(self)

    def eatChars(self):
        #print ("state:eatCppComment")
        ConsumeState.token = ""
        while True:
            if(ConsumeState._returncomments):
                ConsumeState.token = ConsumeState.token + ConsumeState.currChar
            if ConsumeState._pIn is None or ConsumeState.filepointer == ConsumeState._pInlen - 1:
                ConsumeState._pIn = None
                return
            ConsumeState.filepointer = ConsumeState.filepointer + 1
            ConsumeState.currChar = ConsumeState.getChar(self)
            if (ConsumeState.currChar == '\n'):
                return

    

class EatSpecialTokens(ConsumeState):
    def __init__(self):
        ConsumeState.__init__(self)

    def eatChars(self):
        #print ("state:eatSpecialTokens")
        ConsumeState.token = ""
        if(ConsumeState.checkSpecialDoubleChar(self)):
            ConsumeState.token = ConsumeState.token + ConsumeState.currChar
            ConsumeState.filepointer = ConsumeState.filepointer + 1
            ConsumeState.currChar = ConsumeState.getChar(self)
            ConsumeState.token = ConsumeState.token + ConsumeState.currChar
        else:
            ConsumeState.token = ConsumeState.token + ConsumeState.currChar
        if ConsumeState._pIn is None or ConsumeState.filepointer == ConsumeState._pInlen - 1:
            ConsumeState._pIn = None
            return
        ConsumeState.filepointer = ConsumeState.filepointer + 1
        ConsumeState.currChar = ConsumeState.getChar(self)


class EatQuotedString(ConsumeState):
    def __init__(self):
        ConsumeState.__init__(self)

    def eatChars(self):
        #print ("state:eatQuotedString")
        quotation = ConsumeState.currChar
        ConsumeState.token = ""
        while True:
            chNext = ConsumeState._pIn[ConsumeState.filepointer+1]
            if (ConsumeState.currChar == '\\' and (chNext == quotation or chNext == '\\')):
                ConsumeState.token = ConsumeState.token + ConsumeState.currChar
                ConsumeState.filepointer = ConsumeState.filepointer + 1
                ConsumeState.currChar = ConsumeState.getChar(self)
                ConsumeState.token = ConsumeState.token + ConsumeState.currChar
                ConsumeState.filepointer = ConsumeState.filepointer + 1
                ConsumeState.currChar = ConsumeState.getChar(self)
            else:
                ConsumeState.token = ConsumeState.token + ConsumeState.currChar
                if (not ConsumeState._pIn):
                    return
                ConsumeState.filepointer = ConsumeState.filepointer + 1
                ConsumeState.currChar = ConsumeState.getChar(self)
            if (ConsumeState.currChar == quotation):
                ConsumeState.token = ConsumeState.token + ConsumeState.currChar
                break
        if ConsumeState._pIn is None or ConsumeState.filepointer == ConsumeState._pInlen - 1:
            ConsumeState._pIn = None
            return
        ConsumeState.filepointer = ConsumeState.filepointer + 1
        ConsumeState.currChar = ConsumeState.getChar(self)

class EatPunctuator(ConsumeState):
    def __init__(self):
        ConsumeState.__init__(self)

    def eatChars(self):
        #print ("state:eatPunctuator")
        ConsumeState.token = ""
        while True:
            ConsumeState.token = ConsumeState.token + ConsumeState.currChar
            if ConsumeState._pIn is None or ConsumeState.filepointer == ConsumeState._pInlen - 1:
                ConsumeState._pIn = None
                return
            ConsumeState.filepointer = ConsumeState.filepointer + 1
            ConsumeState.currChar = ConsumeState.getChar(self)
            if (not ConsumeState.ispunct(self,ConsumeState.currChar) or ConsumeState.checkSpecialSingleChar(self) or ConsumeState.checkSpecialDoubleChar(self) or ConsumeState.currChar == '"' or ConsumeState.currChar == '\''):
                return 

class EatAlphanum(ConsumeState):
    def __init__(self):
        ConsumeState.__init__(self)

    def eatChars(self):
        #print ("state:eatAlphanumeric")
        ConsumeState.token = ""
        while True:
            ConsumeState.token = ConsumeState.token + ConsumeState.currChar
            if ConsumeState._pIn is None or ConsumeState.filepointer == ConsumeState._pInlen - 1:
                ConsumeState._pIn = None
                return
            ConsumeState.filepointer = ConsumeState.filepointer + 1
            ConsumeState.currChar = ConsumeState.getChar(self)
            if (not ConsumeState.currChar.isalnum()):
                break
    
            
            
    
                
    


    
            
            
    
                
    
