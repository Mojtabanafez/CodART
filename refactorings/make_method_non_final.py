"""
The scripts implements different refactoring operations


"""
__version__ = '0.1.0'
__author__ = 'Morteza'

import networkx as nx

from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter
from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
import visualization.graph_visualization


class MakeMethodNonFinalRefactoringListener(JavaParserLabeledListener):
    """
    To implement the extract class refactoring
    Encapsulate field: Make a public field private and provide accessors
    a stream of tokens is sent to the listener, to build an object token_stream_rewriter
    field addresses the field of the class, tobe encapsulated.
    """

    def __init__(self, common_token_stream: CommonTokenStream = None,
                 class_identifier: str = None, method_identifier: str = None):
        """
        :param common_token_stream:
        """
        self.enter_class = False
        self.token_stream = common_token_stream
        self.class_identifier = class_identifier
        self.method_identifier = method_identifier
        if common_token_stream is not None:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)
        else:
            raise TypeError('common_token_stream is None')
        self.Is_method =False
        self.Is_method_name=None


    def enterClassDeclaration(self, ctx:JavaParserLabeled.ClassDeclarationContext):
        print("enterNormalClassDeclaration----------------------------" + ctx.IDENTIFIER().getText())
        if ctx.IDENTIFIER().getText() != self.class_identifier:
            return
        self.enter_class = True
    def exitClassDeclaration(self, ctx:JavaParserLabeled.ClassDeclarationContext):
        if not self.enter_class:
            return
        print("exitNormalClassDeclaration----------------------------" + ctx.IDENTIFIER().getText())
        self.enter_class = False



    def exitClassBodyDeclaration2(self, ctx:JavaParserLabeled.ClassBodyDeclaration2Context):
        if not self.Is_method:
            return
        if (not self.enter_class) or self.method_identifier != self.Is_method_name:
            return
        print("---------Founded! method " + self.Is_method_name + " is under changes!------")
        modifiers = ctx.modifier()
        new_code = ""
        i=1
        self.token_stream_rewriter.deleteIndex(ctx.start.tokenIndex)
        tmp =True
        for modifier in modifiers:
            if modifier.getText() != "final":
                new_code += modifier.getText()+" "
            else:
                tmp=False
            self.token_stream_rewriter.deleteIndex(ctx.start.tokenIndex+i)
            i += 1
        self.token_stream_rewriter.deleteIndex(ctx.start.tokenIndex + i)
        print(new_code)
        self.token_stream_rewriter.insertBeforeIndex(ctx.start.tokenIndex, new_code)
        if tmp:
            print("---------method " + self.Is_method_name + "  was non-final method!------")
        else:
            print("---------method " + self.Is_method_name + " changed successfully!------")
        self.Is_method = False
        self.Is_method_name = None

    def enterMethodDeclaration(self, ctx:JavaParserLabeled.MethodDeclarationContext):
        self.Is_method = True
        self.Is_method_name = ctx.IDENTIFIER().getText()

