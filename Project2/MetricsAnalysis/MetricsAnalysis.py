from Project2.Parser.Parser import Parser
from Project2.Parser.ConfigureParser import ConfigParseToConsole
from Project2.ASTree.AST import ASTTree

class AnalysisNode:
    name = ""
    size = 0
    complexity = 0

    def __init__(self):
        self.name = ""
        self.size = 0
        self.complexity = 0

    def setComplexity(self,complexity_):
        self.complexity = complexity_

    def setSize(self,size_):
        self.size = size_

    def setName(self,name_):
        self.name = name_

    def show(self):
        temp = ""
        temp = temp + "("
        temp = temp + "Function "
        temp = temp + self.name
        temp = temp + ", "
        temp = temp + "Size = "
        temp = temp + str(self.size)
        temp = temp + ", "
        temp = temp + "Complexity = "
        temp = temp + str(self.complexity)
        temp = temp + ")"
        return temp

class MetricsAnalysis:
    configure = None
    pParser = None
    pRoot_ = None
    pTree_ = ASTTree(pRoot_)
    collection_ = []

    def __init__(self):
        self.configure = ConfigParseToConsole()
        self.pParser = None
        self.pRoot_ = None
        self.pTree_ = ASTTree(self.pRoot_)
        self.collection_ = []

    def isParserBuilt(self):
        succeeded = False
        if self.pParser is not None:
            succeeded = True
        return succeeded

    def printTree(self):
        self.pTree_.DisplayTree(self.pRoot_)

    def buildAST(self):
        if (self.pParser):
            try:
                while (self.pParser.next()):
                    self.pParser.parse()
            except ValueError:
                print("oops error occured")
            self.pRoot_ = self.configure.TreeRoot()

    def Attach(self,name,isFile):
        self.pParser = self.configure.Build()
        isattached = False
        if(self.pParser):
            isattached = self.configure.Attach(name,True)
        return isattached

    def BuildAnalysisData(self,pItem_):
        if(pItem_.type_ == "function"):
            node = AnalysisNode()
            node.setName(pItem_.name)
            node.setSize(self.pTree_.CalculateSize(pItem_))
            node.setComplexity(self.pTree_.CalculateComplexity(pItem_))
            self.collection_.append(node)
        iter_ = 0
        while (iter_ < len(pItem_.children_)):
            self.BuildAnalysisData(pItem_.children_[iter_])
            iter_ = iter_ + 1

    def AnalyseFunctionComplexity(self):
        self.BuildAnalysisData(self.pRoot_)

    def DisplayAnalysis(self):
        print("I am here")
        i = 0
        iter_ = 0
        while (iter_ < len(self.collection_)):
            print(self.collection_[i].show())
            iter_ = iter_ + 1
            i = i + 1


def main():
    createTree = MetricsAnalysis()
    fileSpec = open(r"C:\Users\lenovo\Desktop\OOD-sneha\OOD Projects\PR2\Parser\Parser.cpp")
    createTree.Attach(fileSpec,True)
    createTree.isParserBuilt()
    createTree.buildAST()
    createTree.AnalyseFunctionComplexity()
    createTree.DisplayAnalysis()
    

if __name__ == "__main__": main()
        
        
