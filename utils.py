import abc
# this class characterizes an automaton
class FSA:
    def __init__ (self, numStates = 0, startStates=None, finalStates=None, alphabetTransitions=None) :
        self.numStates = numStates
        self.startStates = startStates
        self.finalStates = finalStates
        self.alphabetTransitions = alphabetTransitions

class NFA(FSA):
    def simulate(self, ipStr):
        S = set(self.startStates)
        newS = set()
        for i in range(len(ipStr)):
            symbol = ipStr[i]
            tm = self.alphabetTransitions[symbol]
            for state in S:
                trs = tm[state]
                for tr in range(len(trs)):
                    if trs[tr] == 1:
                        newS.add(tr)
            S = set(newS)
            newS = set()
        if len(self.finalStates) > 0 and not S.isdisjoint(self.finalStates):
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
    def resolveTransitionStates(self,treeL,treeR):
        """
        The purpose of this function is to resolve the transition states of the two trees. That is to say,
        When we are given 2 NFAs treeL, treeR, we merge the transition matrices of the two trees to form a new transition matrix.
        This is done by adding treeL.numStates to the states of treeR, so the statenumbers of treeR do not overlap with treeL, they are 
        shifted by treeL.numStates.

        Also, we set the startStates as the union of the startStates of treeL and treeR.
        And, we set the finalStates as the union of the finalStates of treeL and treeR.
        """
        treeLDict=treeL.alphabetTransitions
        treeRDict=treeR.alphabetTransitions
        newDict={'a':[],'b':[],'c':[],'e':[]}
        for sym in newDict:
            for rowi in range(len(treeLDict[sym])+len(treeRDict[sym])):
                if(rowi<len(treeLDict[sym])):
                    newRow=treeLDict[sym][rowi]+[0 for _ in range(len(treeRDict[sym]))]
                    newDict[sym].append(newRow)
                else:
                    newRow=[0 for _ in range(len(treeLDict[sym]))]+(treeRDict[sym][rowi-len(treeLDict[sym ])])
                    newDict[sym].append(newRow)
        
        newStartStates=set()
        newFinalStates=set()
        newNumStates=treeL.numStates+treeR.numStates
        newStartStates=newStartStates.union(treeL.startStates)
        newFinalStates=newFinalStates.union(treeL.finalStates)

        for state in treeR.startStates:
            newStartStates.add(state+treeL.numStates)
        
        for state in treeR.finalStates:
            newFinalStates.add(state+treeL.numStates)
              
        retFSA=FSA(newNumStates,newStartStates,newFinalStates,newDict)
        return retFSA

    # .
    def operatorDot(self, treeL,treeR):
        """
        Here, we basically make an epsilon-transition from the final states of treeL to the start states of treeR and then
        we remove the epsilon transition from the final states of treeL to the start states of treeR using the algorithm to remove epsilon transitions.
        """
        treeLStart,treeLFinal=treeL.startStates,treeL.finalStates #start and final states of treeL
        treeRStart,treeRFinal=treeR.startStates,treeR.finalStates #start and final states of treeR
        
        tempFSA=self.resolveTransitionStates(treeL,treeR) #resolve the transition states of the two trees

        markedStates=[] #Mark the states that are connected from the start states of treeR to the some other state of treeR

        for state in treeRStart:
            for sym in treeR.alphabetTransitions:
                for coli in range(len(treeR.alphabetTransitions[sym])):
                    if(treeR.alphabetTransitions[sym][state][coli]==1):#Check if the there is a transition from any one of the final states of treeR to some other state of treeR
                        markedStates.append((sym,coli)) #Add the marked states and the symbol that marks them to the markedStates list
        
        for symb,state in markedStates:
            for finals in treeLFinal:#For each final state of treeL, we add a transition from the final state of treeL to the marked states
                tempFSA.alphabetTransitions[symb][finals][state+treeL.numStates]=1
        
        tempFSA.startStates=treeLStart.copy()#By default, the start states of the new FSA are the start states of treeL

        tempFSA.finalStates=set()
        for state in treeRFinal:
            tempFSA.finalStates.add(state+treeL.numStates)#The final states of the new FSA are the final states of treeR and to each state number of treeRFinal, we add treeL.numStates to it to get the correct state number in the new FSA

        for state in treeLStart:
            if state in treeLFinal:
                for starts in treeRStart:
                    tempFSA.startStates.add(starts+treeL.numStates)#If the start states of treeL are also final states of treeL, then we add the start states of treeR to the start states of the new FSA
        
        for state in treeRFinal:
            if state in treeRStart:
                for finals in treeLFinal:
                    tempFSA.finalStates.add(finals)#If the final states of treeR are also start states of treeR, then we add the final states of treeL to the final states of the new FSA
                    
        return tempFSA

    # +
    def operatorPlus(self,treeR,treeL):
        tempFSA=self.resolveTransitionStates(treeL,treeR)#resolve the transition states of the two trees, and our resolving function basically does union of the 2 NFAs too.
        return tempFSA




    # *
    def operatorStar(self,treeLeft):
        preFinal=[]

        for state in treeLeft.finalStates:
            for sym in treeLeft.alphabetTransitions:
                for rowi,row in enumerate(treeLeft.alphabetTransitions[sym]):
                    if(row[state]==1):
                        preFinal.append((sym,rowi))#Collect all the transitions to the final states of treeLeft and store them in preFinal


        for stStates in treeLeft.startStates:
            for target in preFinal:
                treeLeft.alphabetTransitions[target[0]][target[1]][stStates]=1#Add transitions to the start states of treeLeft from the preFinal states with the same symbol as the preFinal states

        treeLeft.finalStates=treeLeft.startStates.copy() #The final states of the new FSA are the start states of the treeLeft      
        
        return treeLeft

            
    # a, b, c and e for epsilon
    def alphabet(self, symbol):
        """
        Here, we create an NFA that will accept a single character. We do this by creating a new NFA with 2 states, one start state and one final state, and marking the transition from the start state to the final state with the symbol.
        """
        if(symbol!='e'):
            newStartState=set()
            newFinalState=set()
            newNumStates=0
            newStartState.add(newNumStates)
            newFinalState.add(newNumStates+1)
            newTransitions={'a':[[0,0],[0,0]],'b':[[0,0],[0,0]],'c':[[0,0],[0,0]],'e':[[0,0],[0,0]]}
            newTransitions[symbol][newNumStates][newNumStates+1]=1
            newNumStates+=2
            newFSA=FSA(newNumStates,newStartState,newFinalState,newTransitions)
            return newFSA
        else:
            """
            if the symbol is epsilon, then we create an NFA that accepts epsilon. This is done by creating a new NFA with 1 state, and setting that state as the fi8nal and start stae.
            """
            newStartState=set()
            newFinalState=set()
            newNumStates=0
            newStartState.add(newNumStates)
            newFinalState.add(newNumStates)
            newTransitions={'a':[[0]],'b':[[0]],'c':[[0]],'e':[[0]]}
            newNumStates+=1
            newFSA=FSA(newNumStates,newStartState,newFinalState,newTransitions)
            return newFSA

        
    # Traverse the regular expression tree(ETree)
    # calling functions on each node and hence
    # building the automaton for the regular
    # expression at the root.
################################################
##CODE AND COMMENTS FROM HERE ON ARE THE AUTHORS
################################################
    #Anytime we work on a binary tree, the first thing that comes to mind is recursion. So thats what we will do.
         

    def buildNFAR(self, root):

        # write code to populate the above datastructures for a regex tree
        
        if root.val.isalpha():
          retval=self.alphabet(root.val)
        else:
            symb=root.val
            treeLeft=None
            treeRight=None
            if symb=='*':
                treeLeft=self.buildNFAR(root.left)
                retval=self.operatorStar(treeLeft)
            else:
                treeLeft=self.buildNFAR(root.left)
                treeRight=self.buildNFAR(root.right)
                if symb=='+':
                    retval=self.operatorPlus(treeLeft,treeRight)
                else:
                    retval=self.operatorDot(treeLeft,treeRight)
        self.nfa=NFA(retval.numStates,retval.startStates,retval.finalStates,retval.alphabetTransitions)
        #Print the NFA

        return self.nfa           

    def buildNFA(self,root):
        gotRet=self.buildNFAR(root)

        self.nfa=gotRet
        print("The NFA is as follows:")
        print("Number of States: ",self.nfa.numStates)
        print("Start States: ",self.nfa.startStates)
        print("Final States: ",self.nfa.finalStates)
        print("Alphabet Transitions: ",self.nfa.alphabetTransitions)

        return self.nfa
        
    ######################################################################