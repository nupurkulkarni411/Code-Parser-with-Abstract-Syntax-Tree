from Project2.MetricsAnalysis.MetricsAnalysis import MetricsAnalysis


def main():
    createTree = MetricsAnalysis()
    fileSpec = open(r"C:\Users\lenovo\Desktop\OOD-sneha\OOD Projects\PR2\Tokenizer\Tokenizer.cpp")
    createTree.Attach(fileSpec,True)
    createTree.isParserBuilt()
    createTree.buildAST()
    print("Displaying the tree")
    createTree.printTree()
    print("Displaying the Analysis")
    createTree.AnalyseFunctionComplexity()
    createTree.DisplayAnalysis()
    



if __name__ == "__main__": main()
