from Project2.ActionAndRules.ActionAndRules import ASTNode

class ASTTree:
    childCount_ = 0
    pRoot_ = None
    indentLevel = 0

    def __init__(self,pRoot):
        self.pRoot_ = pRoot
        self.childCount_ = 1
        self.indentLevel = 0 

    def setChildCount(self,childCount):
        self.childCount_ = childCount

    def CalculateSize(self,pItem):
        temp = pItem.show()
        return (1 + pItem.endLineCount - pItem.startLineCount)

    def CalculateComplexity(self,pItem):
        self.childCount_ = 0
        self.countChildren(pItem)
        return self.childCount_

    def countChildren(self,pItem):
        iter_ = 0
        self.childCount_ = self.childCount_ + 1
        while (iter_ < len(pItem.children_)):
            self.countChildren(pItem.children_[iter_])
            iter_ = iter_ + 1
            

    def DisplayTree(self,pItem):
        print(' '*(2*self.indentLevel)+ pItem.show())
        self.indentLevel = self.indentLevel + 1
        iter_ = 0
        while (iter_ < len (pItem.children_)):
            self.DisplayTree(pItem.children_[iter_])
            iter_ = iter_ + 1
        self.indentLevel = self.indentLevel - 1



def main():
    pItem = ASTNode()

    pItem.type_ = "function"
    pItem.name = "fun1"
    pItem.startLineCount = 20
    pItem.endLineCount = 33

    pItem1 = ASTNode()

    pItem1.type_ = "if"
    pItem1.name = ""
    pItem1.startLineCount = 25
    pItem1.endLineCount = 32

    pItem.addChild(pItem1)

    pItem2 = ASTNode()
    pItem2.type_ = "for"
    pItem2.name = ""
    pItem1.startLineCount = 26
    pItem1.endLineCount = 30
    pItem1.addChild(pItem2)

    pTree = ASTTree(pItem)
    pTree.CalculateComplexity(pItem)
    pTree.CalculateSize(pItem)
    pTree.DisplayTree(pItem)


#if __name__ == "__main__": main()
        
        
