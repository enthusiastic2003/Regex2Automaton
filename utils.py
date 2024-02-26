import abc

# this class characterizes an automaton
class FSA:
    def __init__ (self, numStates = 0, startState=None, finalStates=None, alphabetTransitions=None) :
        self.numStates = numStates
        self.startState = startState
        self.finalStates = finalStates
        self.alphabetTransitions = alphabetTransitions

class NFA(FSA):
    def simulate(self, ipStr):
        S = set(self.startState)
        newS = set()
        for i in range(len(ipStr)):
            symbol = ipStr[i]
            while len(S) > 0:
                tm = self.alphabetTransitions[symbol]
                for state in range(len(S)):
                    trs = tm[state]
                    for tr in range(len(trs)):
                        if trs[tr] == 1:
                            newS.add(tr)
            S = set(newS)
            newS = set()
        if S.intersection(self.finalStates):
            print("String Accepted")
            return True
        else:
            print("String Rejected")
            return False

    def getNFA(self):
        return self

class ETree:
    root = None
    nfa = None
    class ETNode:
        def __init__(self, val=" ", left=None, right=None):
            self.val = val
            self.left = left
            self.right = right

    def compute(self, operands, operators):
            operator = operators.pop()
            if operator == "*":
                left = operands.pop()
                operands.append(self.ETNode(val=operator, left=left))
            elif operator == "+":
                right, left = operands.pop(), operands.pop()
                operands.append(self.ETNode(val=operator, left=left, right=right))
            elif operator == ".":
                right, left = operands.pop(), operands.pop()
                operands.append(self.ETNode(val=operator, left=left, right=right))

    def parseRegex(self, regex):
        operands, operators = [], []
        for i in range(len(regex)):
            if regex[i].isalpha():
                operands.append(self.ETNode(val=regex[i]))
            elif regex[i] == '(':
                operators.append(regex[i])
            elif regex[i] == ')':
                while operators[-1] != '(':
                    self.compute(operands, operators)
                operators.pop()
            else :
                operators.append(regex[i])
        while operators:
            self.compute(operands, operators)

        if len(operators) == 0:
            self.root = operands[-1]
        else :
            print("Parsing Regex failed.")

    def getTree(self):
        return self.root

    ###################################################################
    # IMPLEMENTATION STARTS AFTER THE COMMENT
    # Implement the following functions

    # In the below functions to be implemented delete the pass statement
    # and implement the functions. You may define more functions according
    # to your need.
    ###################################################################
    # .
    def operatorDot(self, fsaX, fsaY):
        pass

    # +
    def operatorPlus(self, fsaX, fsaY):
        pass

    # *
    def operatorStar(self, fsaX):
        pass

    # a, b, c
    def alphabet(self, symbol):
        pass

    # Traverse the regular expression tree(ETree)
    # calling functions on each node and hence
    # building the automaton for the regular
    # expression at the root.
    def buildNFA(self, root):
        if root == None:
            print("Tree not available")
            exit(0)

        numStates = 0
        initialState = set()
        finalStates = set()
        transitions = {}

        # write code to populate the above datastructures for a regex tree

        self.nfa = NFA(numStates, initialState, finalStates, transitions)
        return self.nfa

    ######################################################################