from Project2.Tokenizer.Toker import Toker
from Project2.SemiExpression.SemiExpression import SemiExp
from Project2.ScopeStack.ScopeStack import ScopeStack
from Project2.Interfaces import IRule
from Project2.Interfaces import IAction
from Project2.Interfaces import ITokCollection
from Project2.Parser.Parser import Parser

class ASTNode(object):
    type_ = ""
    name_ = ""
    startLineCount  = 0
    endLineCount = 0
    children_ = []

    def __init__(self):
        self.type_ = ""
        self.name = ""
        self.startLineCount = 0
        self.endLineCount = 0
        self.children_ = []
        

    def show(self):
        temp = ""
        temp = temp + "("
        temp = temp + self.type_
        temp = temp + ", "
        temp = temp + self.name
        temp = temp + ", "
        temp = temp + str(self.startLineCount)
        temp = temp + ", "
        temp = temp + str(self.endLineCount)
        temp = temp + ")"
        return temp

    def addChild(self,t):
        self.children_.append(t)



class Repository:
    stack = None
    p_Toker = None
    pRoot = None

    def __init__(self,pToker):
        self.p_Toker = pToker
        self.stack = ScopeStack()
        self.pRoot = None
        self.initializeRoot()

    def scopeStack(self):
        return self.stack

    def Toker(self):
        return p_Toker

    def lineCount(self):
        return int(self.p_Toker.currentLineCount())

    def TreeRoot(self):
        return self.pRoot

    def initializeRoot(self):
        elem = ASTNode()
        elem.type_ = "Global Namespace"
        elem.name = "Global Namespace"
        elem.startLineCount = 0
        elem.endLineCount = 0
        self.scopeStack().push(elem)
        self.pRoot = elem

    def Delete(self,pItem):
        del pItem.children_[:]

class BeginningOfScope(IRule):
    def doTest(self,pTc):
        if(pTc.find("{") < pTc.length()):
            IRule.doActions(self,pTc)
            return True
        return True

class HandlePush(IAction):
    p_Repos = None
    controlSignalName_ = ""
    
    def __init__(self,pRepos):
        self.p_Repos = pRepos
        self.controlSignalName_ = ""

    def doAction(self,pTc):
        elem = ASTNode()
        elem.type_ = "unknown"
        elem.name = "anonymous"
        elem.startLineCount = self.p_Repos.lineCount()
        elem.endLineCount = 0
        self.p_Repos.scopeStack().top().addChild(elem)
        self.p_Repos.scopeStack().push(elem)
        
class HandlePushInitializers(IAction):
    p_Repos = None
    def __init__(self,pRepos):
        self.p_Repos = pRepos

    def doAction(self,pTc):
        tc = pTc
        elem = self.p_Repos.scopeStack().pop()
        if(tc[tc.length()-1] == "{" and tc.find("{") - tc.find("=") == 1 and not(tc.find("(") < tc.find("="))):
            name = (pTc)[pTc.find("=") - 1]
            elem.type_ = "Initializer"
            elem.name = name
            elem.startLineCount = self.p_Repos.lineCount()
        self.p_Repos.scopeStack().push(elem)

class HandlePushFunction(IAction):
    p_Repos = None
    controlSignalName_ = ""

    def __init__(self,pRepos):
        self.p_Repos = pRepos
        self.controlSignalName_ = ""

    def isSpecialKeyWord(self,tok):
        keys = ["for","while","switch","if","catch"]
        for i in range (0,5):
            if tok == keys[i]:
                self.controlSignalName_ = keys[i]
                return True
        return False
    
    def doAction(self,pTc):
        tc = pTc
        len_ = tc.find("(")
        elem = self.p_Repos.scopeStack().pop()
        if (tc[tc.length() - 1] == "{" and len_ < tc.length() and not(self.isSpecialKeyWord(tc[len_ - 1]))):
          name = (pTc)[pTc.find("(") - 1]
          elem.type_ = "function"
          if(tc.find("(") - tc.find("]") == 1):
              name = "lambda"
          elem.name = name
          elem.startLineCount = self.p_Repos.lineCount()
        self.p_Repos.scopeStack().push(elem)

class HandlePushControlS(IAction):
    p_Repos = None
    controlSignalName_ = ""

    def __init__(self,pRepos):
        self.p_Repos = pRepos
        self.controlSignalName_ = ""

    def isSpecialKeyWord(self,tok):
        keys1 = ["for","while","switch","if","catch"]
        for i in range (0,5):
            if tok == keys1[i]:
                self.controlSignalName_ = keys1[i]
                return True
        return False

    def isDataStructOrTry(self,pTc):
        keys2 = ["class","struct","try","namespace","do","else"]
        for i in range(0,6):
            if(pTc.find(keys2[i]) < pTc.length()):
                self.controlSignalName_ = keys2[i]
                return True
        return False

    def doAction(self,pTc):
        tc= pTc
        len_ = tc.find("(")
        elem = self.p_Repos.scopeStack().pop()
        if(tc[tc.length() - 1]  == "{" and len_ < tc.length() and self.isSpecialKeyWord(tc[len_ - 1])):
            elem.type_ = self.controlSignalName_
            elem.name = self.controlSignalName_
            elem.startLineCount = self.p_Repos.lineCount()
        elif (tc[tc.length() - 1] == "{" and self.isDataStructOrTry(pTc)):
            name = self.controlSignalName_
            elem.type_ = self.controlSignalName_
            if (self.controlSignalName_ != "try" and self.controlSignalName_ != "do" and self.controlSignalName_ != "else"):
                name = (pTc)[pTc.find(self.controlSignalName_)+1]
                elem.name = name
                elem.startLineCount = self.p_Repos.lineCount()
        self.p_Repos.scopeStack().push(elem)

class EndOfScope(IRule):
    def doTest(self,pTc):
        if(pTc.find("}") < pTc.length()):
            IRule.doActions(self,pTc)
            return True
        return True

class HandlePop(IAction):
    p_Repos = None
    def __init__(self,pRepos):
        self.p_Repos = pRepos

    def doAction(self,pTc):
        if (self.p_Repos.scopeStack().size() == 0):
            return
        elem = self.p_Repos.scopeStack().pop()
        elem.endLineCount = self.p_Repos.lineCount()


def main():
    print(" Testing ActionAndRules class")
    print("==============================")
    fileSpec = open(r"C:\Users\lenovo\Desktop\OOD-sneha\OOD Projects\PR2\Parser\TreeWalkDemo.txt")
    _pIn = fileSpec.read()
    toker1= Toker()
    isattached = toker1.attach(_pIn)
    semi = SemiExp(toker1)
    """while semi.get(True):
        print ("\n  -- semiExpression --")
        print (semi.show(False))
    if semi.length() > 0 :
        print ("\n  -- semiExpression --")
        print (semi.show(False))
        print ("\n\n")"""
    parser = Parser(semi)
    pRepo = Repository(toker1)
    pBeginningOfScope = BeginningOfScope()
    pHandlePush = HandlePush(pRepo)
    pBeginningOfScope.addAction(pHandlePush)

    pHandlePushControlS = HandlePushControlS(pRepo)
    pBeginningOfScope.addAction(pHandlePushControlS)

    pHandlePushFunction = HandlePushFunction(pRepo)
    pBeginningOfScope.addAction(pHandlePushFunction)

    pHandlePushInitializers = HandlePushInitializers(pRepo)
    pBeginningOfScope.addAction(pHandlePushInitializers)
    parser.addRule(pBeginningOfScope)

    pEndOfScope = EndOfScope()
    pHandlePop = HandlePop(pRepo)
    pEndOfScope.addAction(pHandlePop)
    parser.addRule(pEndOfScope)

    while semi.get():
        parser.parse()
    len_ = pRepo.scopeStack().size()
    for i in range(0,len_):
        print(pRepo.scopeStack().pop().show())
      

        
#if __name__ == "__main__": main()
        
    
            
            

    
        
    
