from checkTokenizer.Tokenizer import EatWhitespace
from checkTokenizer.Tokenizer import ConsumeState

class Toker:
    _pConsumer = None
    def __init__(self):
        self._pConsumer = EatWhitespace()
        
    def attach(self,_pIn):
        print (_pIn)
        if(_pIn):
            self._pConsumer.attach(_pIn)
            return True
        return False


    def getTok(self):
        while True:
            if(not self._pConsumer.canRead()):
                return ""
            self._pConsumer.consumeChars()
            if(self._pConsumer.hasTok()):
                break
        return self._pConsumer.getTok()

    def reset(self):
        self._pConsumer.reset()

    def EOFreached(self):
        if(ConsumeState.EOF == True):
            return True
        else:
            return False

    def setSpecialSingleChars(self,ssc):
        self._pConsumer.setSpecialSingleChars(ssc)

    def setSpecialCharPairs(self,scp):
        self._pConsumer.setSpecialCharPairs(scp)

    def returnComments(self,doReturnComments):
        self._pConsumer.returnComments(doReturnComments)

    def currentLineCount(self):
        return self._pConsumer.currentLineCount()
        
            
