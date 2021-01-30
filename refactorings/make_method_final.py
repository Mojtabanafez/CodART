"""
The scripts implements different refactoring operations
"""
__version__ = '0.2.0'
__author__ = 'mojtaba_nafez'

import networkx as nx
from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter
from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
import visualization.graph_visualization

output = None
class MakeMethodFinalRefactoringListener(JavaParserLabeledListener):
    def __init__(self, parse_tree, common_token_stream: CommonTokenStream = None,
                 class_identifier: str = None, method_identifier: str = None):
        """
        :param common_token_stream:
        """
        self.parse_tree = parse_tree
        self.enter_class = False
        self.token_stream = common_token_stream
        self.class_identifier = class_identifier
        self.method_identifier = method_identifier
        if common_token_stream is not None:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)
        else:
            raise TypeError('common_token_stream is None')
        self.method_output_type = 0
        self.method_input_types = []
        self.Is_method = False
        self.Is_method_name = None

    def enterClassDeclaration(self, ctx:JavaParserLabeled.ClassDeclarationContext):
        if ctx.IDENTIFIER().getText() == self.class_identifier:
            self.enter_class = True
            print("enterNormalClassDeclaration------------------------------------------------------------------" + ctx.IDENTIFIER().getText())
    def exitClassDeclaration(self, ctx:JavaParserLabeled.ClassDeclarationContext):
        if not self.enter_class:
            return
        print("exitNormalClassDeclaration------------------------------------------------------------------" + ctx.IDENTIFIER().getText())
        self.enter_class = False

    def enterMethodDeclaration(self, ctx:JavaParserLabeled.MethodDeclarationContext):
        if (not self.enter_class) or self.method_identifier!=ctx.IDENTIFIER().getText():
            return
        print("enterMethodDeclaration-----------------------------------"+ ctx.IDENTIFIER().getText())
        self.Is_method = True
        self.Is_method_name = ctx.IDENTIFIER().getText()

    def exitMethodDeclaration(self, ctx:JavaParserLabeled.MethodDeclarationContext):
        if (not self.enter_class) or self.method_identifier != ctx.IDENTIFIER().getText():
            return
        self.method_output_type = ctx.typeTypeOrVoid().getText()

    def exitFormalParameter(self, ctx:JavaParserLabeled.FormalParameterContext):
        if self.enter_class :
            self.method_input_types.append(ctx.typeType().getText())

    def exitClassBodyDeclaration2(self, ctx:JavaParserLabeled.ClassBodyDeclaration2Context):
        if (not self.Is_method) or ((not self.enter_class) or self.method_identifier != self.Is_method_name):
            self.Is_method = False
            self.Is_method_name = None
            self.method_output_type = 0
            self.method_input_types = []
            return
        self.isInherit()
        global output;
        if output == None:
            print("changed Successfully")
            if ctx.modifier():
                modifier = ctx.modifier()
                for i in range(len(modifier)):
                    if modifier[i].getText() == "final":
                        print("exitMethodDeclaration-----------------------------------" + str(self.Is_method_name))
                        return
                self.token_stream_rewriter.insertAfter(ctx.start.tokenIndex, " final ")
            else:
                self.token_stream_rewriter.insertBeforeIndex(ctx.start.tokenIndex, "final ")
        else:
            print(output)
        print("exitMethodDeclaration-----------------------------------" + str(self.Is_method_name))
        self.Is_method = False
        self.Is_method_name = None
        self.method_output_type = 0
        self.method_input_types = []

    def isInherit(self):
        my_listener = SearchForOverWrite(parse_tree=self.parse_tree,  common_token_stream=self.token_stream, class_identifier=self.class_identifier,
                                         method_identifier=self.method_identifier, classes=[self.class_identifier])
        my_listener.method_input_types = self.method_input_types
        my_listener.method_output_type = self.method_output_type
        walker = ParseTreeWalker()
        walker.walk(t=self.parse_tree, listener=my_listener)














class SearchForOverWrite(JavaParserLabeledListener):
    def __init__(self, parse_tree, common_token_stream: CommonTokenStream = None,
                 class_identifier: str = None, method_identifier: str = None, classes=[]):

        self.classes = classes
        self.parse_tree = parse_tree
        self.enter_class = False
        self.token_stream = common_token_stream
        self.class_identifier = class_identifier
        self.method_identifier = method_identifier
        if common_token_stream is not None:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)
        else:
            raise TypeError('common_token_stream is None')
        self.method_output_type = ""
        self.method_input_types = []
        self.input_types = []



    def enterClassDeclaration(self, ctx:JavaParserLabeled.ClassDeclarationContext):
        if ctx.typeType():
            if ctx.typeType().getText() == self.classes[0]:
                self.enter_class = True
                self.classes.append(ctx.IDENTIFIER().getText())

    def exitClassDeclaration(self, ctx:JavaParserLabeled.ClassDeclarationContext):
        if not self.enter_class:
            return
        self.enter_class = False
    def enterMethodDeclaration(self, ctx:JavaParserLabeled.MethodDeclarationContext):
        if (not self.enter_class) or self.method_identifier!=ctx.IDENTIFIER().getText():
            return
        print("enterMethodDeclaration----InExtended:--------" + ctx.IDENTIFIER().getText())

    def exitFormalParameter(self, ctx:JavaParserLabeled.FormalParameterContext):
        if self.enter_class :
            self.input_types.append(ctx.typeType().getText())

    def exitMethodDeclaration(self, ctx:JavaParserLabeled.MethodDeclarationContext):
        if (not self.enter_class) or self.method_identifier != ctx.IDENTIFIER().getText():
            self.input_types=[]
            return
        output_type = ctx.typeTypeOrVoid().getText()

        if output_type != self.method_output_type:
            self.input_types=[]
            return

        if len(self.input_types)!=len(self.method_input_types):
            return
        for i in range(len(self.input_types)):
            if self.input_types[i] != self.method_input_types[i]:
                return
        global output
        output = {"error" : ("sorry this method can not be final,\n because it's OverWrite in subclass "+self.classes[len(self.classes)-1])}
        self.input_types=[]
        print("exitMethodDeclaration-----InExtended:--------" + ctx.IDENTIFIER().getText())

    def isInherit(self):
        my_listener = SearchForOverWrite(parse_tree=self.parse_tree, common_token_stream=self.token_stream,
                                         class_identifier=self.classes[0],
                                         method_identifier=self.method_identifier, classes=[self.class_identifier])
        my_listener.method_input_types = self.method_input_types
        my_listener.method_output_type = self.method_output_type
        walker = ParseTreeWalker()
        walker.walk(t=self.parse_tree, listener=my_listener)




    def exitCompilationUnit(self, ctx:JavaParserLabeled.CompilationUnitContext):
        global output
        if output:
            return
        self.classes.pop(0)
        if len(self.classes)>0:
            self.isInherit()




