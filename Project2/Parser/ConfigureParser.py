from Project2.Parser.Parser import Parser
from Project2.Tokenizer.Toker import Toker
from Project2.SemiExpression.SemiExpression import SemiExp
from Project2.ActionAndRules.ActionAndRules import ASTNode,Repository,BeginningOfScope,HandlePush,HandlePushInitializers,HandlePushFunction,HandlePushControlS,EndOfScope,HandlePop
from Project2.Interfaces import IBuilder

class ConfigParseToConsole(IBuilder):
    pIn = None
    pToker = None
    pSemi = None
    pParser = None
    pRepo = None
    pBeginningOfScope = None
    pHandlePush = None
    pHandlePushControlS = None
    pHandlePushInitializers = None
    pEndOfScope = None
    pHandlePop = None
    pRoot_ = None

    def __init__(self):
        self.pIn = None
        self.pToker = None
        self.pSemi = None
        self.pParser = None
        self.pRepo = None
        self.pBeginningOfScope = None
        self.pHandlePush = None
        self.pHandlePushControlS = None
        self.pHandlePushInitializers = None
        self.pEndOfScope = None
        self.pHandlePop = None
        self.pRoot_ = None

    def TreeRoot(self):
        return self.pRoot_

    def Attach(self,name,isFile):
        if isFile is None:
            isFile = True
        if self.pToker == 0:
            return False
        self.pIn = name.read()
        if not self.pIn:
            return False
        return self.pToker.attach(self.pIn)

    def Build(self):
        self.pToker = Toker()
        self.pToker.returnComments(False)
        self.pSemi = SemiExp(self.pToker)
        self.pParser = Parser(self.pSemi)
        self.pRepo = Repository(self.pToker)
        self.pRoot_ = self.pRepo.TreeRoot()
        self.pBeginningOfScope = BeginningOfScope()
        self.pHandlePush = HandlePush(self.pRepo)
        self.pBeginningOfScope.addAction(self.pHandlePush)
        self.pHandlePushControlS = HandlePushControlS(self.pRepo)
        self.pBeginningOfScope.addAction(self.pHandlePushControlS)
        self.pHandlePushFunction = HandlePushFunction(self.pRepo)
        self.pBeginningOfScope.addAction(self.pHandlePushFunction)
        self.pHandlePushInitializers = HandlePushInitializers(self.pRepo)
        self.pBeginningOfScope.addAction(self.pHandlePushInitializers)
        self.pParser.addRule(self.pBeginningOfScope)

        self.pEndOfScope = EndOfScope()
        self.pHandlePop = HandlePop(self.pRepo)
        self.pEndOfScope.addAction(self.pHandlePop)

        self.pParser.addRule(self.pEndOfScope)
        return self.pParser

def main():
    fileSpec = open(r"C:\Users\lenovo\Desktop\OOD-sneha\OOD Projects\PR2\Parser\Parser.cpp")
    configure = ConfigParseToConsole()
    pParser = configure.Build()
    if pParser:
        configure.Attach(fileSpec,True)
    while pParser.next():
        pParser.parse()
            
#if __name__ == "__main__": main()
        
