class element(object):
    type_ = ""
    name = ""
    startLineCount = 0
    endLineCount = 0
    _children = []

    def __init__(self):
        self.type_ = ""
        self.name = ""
        self.startLineCount = 0
        self.endLineCount = 0
        self._children = []

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
    
    
class ScopeStack:
    stack = []

    def __init__(self):
        self.stack = []
    
    def push(self,item):
        self.stack.append(item)

    def size(self):
        return len(self.stack)

    def begin(self):
        return self.stack[0]
    
    def end(self):
        return self.stack[-1]

    def pop(self):
        item = self.stack[-1]
        del self.stack[-1]
        return item

    def top(self):
        return self.stack[-1]

    def showStack(self,stack_,indent):
        if indent is None:
            indent = True
        if(len(stack_.stack) == 0):
            print ("ScopeStack is empty")
            return
        iter_ = 0
        while (iter_ < len (stack_.stack)):
            strIndent = 2 * len(stack_.stack)
            strIndent = ' ' * strIndent
            if (not indent):
                strIndent = ""
            temp = ""
            temp = temp + "("
            temp = temp + stack_.stack[iter_].type_
            temp = temp + ", "
            temp = temp + stack_.stack[iter_].name
            temp = temp + ", "
            temp = temp + str(stack_.stack[iter_].startLineCount)
            temp = temp + ", "
            temp = temp + str(stack_.stack[iter_].endLineCount)
            temp = temp + ")"
            print(strIndent + temp)
            iter_ = iter_ + 1

      
def TreeWalk(pItem):
    print(' '*(2*TreeWalk.indentlevel)+ pItem.show())
    TreeWalk.indentlevel = TreeWalk.indentlevel + 1
    iter_ = 0
    while (iter_ < len (pItem._children)):
        TreeWalk(pItem._children[iter_])
        iter_ = iter_ + 1
    TreeWalk.indentlevel = TreeWalk.indentlevel - 1

TreeWalk.indentlevel = 0 

def main():
    print("Testing Scope Stack")
    print("=====================")
    print("pushing items onto ScopeStack instance after adding startLineCount")
    print("--------------------------------------------------------------------")
    testStack = ScopeStack()
    pItem = element()
    pItem.type_ = "function"
    pItem.name = "fun1"
    pItem.startLineCount = 33
    testStack.push(pItem)


    pItem = element()
    pItem.type_ = "if"
    pItem.name = ""
    pItem.startLineCount = 38
    (testStack.top()._children).append(pItem)
    testStack.push(pItem)

    pItem = element()
    pItem.type_ = "for"
    pItem.name = ""
    pItem.startLineCount = 40
    (testStack.top()._children).append(pItem)
    testStack.push(pItem)

    testStack.showStack(testStack,False)

    print("Popping two items off ScopeStack after adding endLineCount")
    print("------------------------------------------------------------")

    testStack.top().endLineCount = 50
    print(testStack.pop().show())
    testStack.top().endLineCount = 55
    print(testStack.pop().show())

    print("Pushing another item onto ScopeStack after adding startLineElement")
    print("--------------------------------------------------------------------")
    pItem = element()
    pItem.type_ = "while"
    pItem.name = ""
    pItem.startLineCount = 60
    (testStack.top()._children).append(pItem)
    testStack.push(pItem)

    print("Stack now contains:")
    print("---------------------")
    testStack.showStack(testStack,False)

    print("Popping last elements off stack after adding endLineCount")
    print("-----------------------------------------------------------")
    testStack.top().endLineCount = 70
    pTop = testStack.pop()
    print(pTop.show())
    testStack.top().endLineCount = 75
    pTop = testStack.pop()
    print(pTop.show())

    print("Walking simulated AST tree:")
    print("-----------------------------")
    TreeWalk(pTop)


    
#if __name__ == "__main__": main()


    
