class ITokCollection(object):
    def get(self,clear = True):
        raise NotImplementedError("Subclass must implement abstract method")

    def length(self):
        raise NotImplementedError("Subclass must implement abstract method")

    def find(self):
        raise NotImplementedError("Subclass must implement abstract method")

    def push_back(self):
        raise NotImplementedError("Subclass must implement abstract method")

    def remove(self,tok):
        raise NotImplementedError("Subclass must implement abstract method")

    def toLower(self):
        raise NotImplementedError("Subclass must implement abstract method")

    def trimFront(self):
        raise NotImplementedError("Subclass must implement abstract method")

    def show(self,showNewLines = False):
        raise NotImplementedError("Subclass must implement abstract method")

    def isComment(self,tok):
        raise NotImplementedError("Subclass must implement abstract method")

class IBuilder:
    def Build(self):
        raise NotImplementedError("Subclass must implement abstract method")

class IAction:
    def doAction(self,pTc):
        raise NotImplementedError("Subclass must implement abstract method")

class IRule:
    actions = []

    def __init__(self):
        self.actions = []
        
    def doTest(self,pTc):
        raise NotImplementedError("Subclass must implement abstract method")
    
    def addAction(self,pAction):
        self.actions.append(pAction)

    def doActions(self,pTokColl):
        if(len(self.actions) > 0):
            for i in range(0,len(self.actions)):
                self.actions[i].doAction(pTokColl)
        

