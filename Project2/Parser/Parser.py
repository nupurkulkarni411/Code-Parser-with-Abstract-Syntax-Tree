from Project2.Interfaces import ITokCollection,IAction

class Parser:
    pTokColl = None
    rules = []
    def __init__(self,pTokCollection):
        self.pTokColl = pTokCollection
        self.rules = []

    def addRule(self,pRule):
        self.rules.append(pRule)

    def next(self):
        succeeded = self.pTokColl.get()
        if not succeeded:
            return False
        return True

    def parse(self):
        succeeded = False
        for i in range (0,len(self.rules)):
            if self.rules[i].doTest(self.pTokColl):
                succeeded = True
        return succeeded
        
