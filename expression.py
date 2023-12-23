from __future__ import annotations

from pile import pile
import copy

class expression:
    __LEFT__ = 0
    __RIGHT__ = 1

    debug = False
    def __init__(self, isFactor:bool|None, isStar: bool|None, state: int|None, content, stateList:list[str]=None, eventList:list[str]=None) -> None:
        self.isFactor: bool|None=isFactor          # Defnine what's in front of the expression : nothing(None), +(False), *(True)
        self.isStar: bool=isStar                   # Define if it's needed to put a star
        self.state: int|None=state                 # State id
        self.content: list|int|expression=content  # List of event id and expression object

        self.stateList: list = stateList
        self.eventList: list = eventList


    def parentheses(self):
        """
        This methods puts self.content in parenthesis if needed, it's usefull when it's needed to ad a factor (state or event)
        For example :
            - ax + (b+c) -> (ax + (b+c))
            - (ax + b)(c + d) -> (ax + b)(c + d)
            - (ax + b) + (c + d) -> ((ax + b) + (c + d))
        """
        i=0
        parenthesed = True

        while(i<len(self.content) and parenthesed == True):
            if (isinstance(self.content[i], expression) and self.content[i].isFactor == False):
                parenthesed = False
            i+=1

        if(parenthesed==False):
            newExpr = expression(True, False, None, self.content)
            self.content = [newExpr]
            #return newExpr

        #return self

    def factorize(self: expression, numberOfState: int):
        """
        This function is use to factorize an expression with all his state in common factor
        numberOfState is used to create a list of size numberOfState.
        If the max index of the states is more than numberOfState, numberOfState need to be equals to this number + 1
        """
        listState:list[int|expression] = [[] for i in range(numberOfState+1)]
        currentState: int|None = None

        i:int = 0
        toAdd:list[int|expression] = []

        #We go across all the content
        while( i < len(self.content) or len(toAdd) != 0):
            expression._expression__debugClassMessage("We are in the main loop")
            #If it's not an expression object, we need to put it in expression object
            if(i < len(self.content) and type(self.content[i]) != expression):
                expression._expression__debugClassMessage("It's not an expression ! Its a", type(self.content[i]))
                #Looking for the state if we do not know which one it is
                if(currentState == None):
                    j:int = i+1
                    currentState:int = self.state if self.state != None else numberOfState

                    #if we don't have a currentState, we need to check if it's not after
                    while(currentState == numberOfState+1 and j< len(self.content) and (type(self.content[j]) != expression or self.content[j].isFactor)):
                        if(type(self.content[j]) == expression and self.content[j].state != None):
                            currentState = self.content[j].state

                        j+=1
                
                expression._expression__debugClassMessage("ImadOss117 : Debuging in int object, currentState =", currentState)
                if(len(toAdd) == 0):
                    toAdd.append(expression(None, False, None, [self.content[i]]))
                else:
                    toAdd[0].content.append(self.content[i])
            

            #If it's an expression object
            else:

                #We have an addition or no currentState
                if (i >=len(self.content) and len(toAdd) != 0) or not self.content[i].isFactor or currentState == None:
                    #If we have somthing do add at our expression befor looking for the current state
                    #The true beinning of the factorization
                    if(currentState != None):
                        stack:pile = pile()
                        stack.pileUp((listState[currentState], 0, toAdd, 1))
                        toAdd:list = []

                        #TODO faire gaffe à la longueur à mettre entre parenthèse bg
                        while not stack.isEmpty():
                           
                            currentFacto = stack.unstack()
                            expression._expression__debugClassMessage("Captain : UNSTACKING !!!")
                            expression._expression__debugClassMessage("ImadOss : Containing folowing data :" ,[currentFacto], len(currentFacto))

                            if type(currentFacto) != tuple:
                                expression._expression__debugClassMessage("Revert, THIS IS THE END")
                                expression.unparenthesis(currentFacto)

                            elif len(currentFacto[0]) == 0:
                                expression._expression__debugClassMessage("Captain : We ... We did it ?!")
                                expression._expression__debugClassMessage("Sailor : checking the content captain :", currentFacto[2])
                                currentFacto[0].extend(currentFacto[2])

                                expression.unparenthesis(currentFacto[0])
                            elif len(currentFacto[2]) == 0:
                                expression._expression__debugClassMessage("Captain : Santa ?!")
                                expression._expression__debugClassMessage("Sailor : checking the content captain :", currentFacto[2])
                                currentFacto[0].append(expression(False, None, None, [-1]))
                                expression.unparenthesis(currentFacto[0])
                            else:
                                expression._expression__debugClassMessage("Wouha ! maybe we'r gonna to make it !")
                                j = currentFacto[1]
                                jSize=len(currentFacto[2])-1
                                step = currentFacto[3]

                                factoOk = False

                                #If -1 we are at the root, if another positive number, we are in a child of the root !
                                #(depth, currentTab) = (-1, currentFacto[0]) if type(currentFacto[0][j]) != expression or currentFacto[0][j].isFactor != True else (j, currentFacto[0][j].content)
                                depth = -1
                                currentTab = currentFacto[0]

                                #If it's ok, it's suppose to stop when we are at the end of the part to add, or at the end of the limiter
                                #The child need to be a sum if we want to go in it !
                                while (not factoOk and j < len(currentTab) and j > -1) or depth != -1:
                                    buffer = (0, 0)

                                    expression._expression__debugClassMessage("Sailor : We are in the loop !", j, jSize, currentTab)
                                    if jSize < len(currentFacto[2]) and j < len(currentTab) and j > -1 : 
                                        expression._expression__debugClassMessage(currentFacto[2][jSize])
                                        expression._expression__debugClassMessage(currentFacto[2][jSize] == currentTab[j])


                                    
                                    if jSize < len(currentFacto[2]) and ( currentFacto[2][jSize] == currentTab[j] or \
                                    (type(currentFacto[2][jSize]) == expression and type(currentTab[j]) == expression and currentFacto[2][jSize].content == currentTab[j].content)) :
                                        jSize+=1
                                        expression._expression__debugClassMessage("Sailor : UPGRADING SIZE SIR")

                                    elif jSize != 0 or jSize == len(currentFacto[2]) or\
                                        (type(currentFacto[2][jSize]) == expression and (buffer := currentFacto[2][jSize].contain(currentTab, step))[0] != 0):
                                        
                                        expression._expression__debugClassMessage("Sailor : COMMON FACTOR FIND", jSize != 0, jSize+1 == len(currentFacto[2]))
                                        #We just find an common factor, we get out the part who don't match
                                        if jSize == len(currentFacto[2]):
                                            buffer = []
                                        elif buffer[0] > 0:
                                            expression._expression__debugClassMessage("Sailor : Captain, somthing strange appen, what do we need to do ?")
                                            start, end = (0, len(currentFacto[2][jSize].content)-buffer[0]-1) if step == -1 else (buffer[0], len(currentFacto[2][jSize].content) - 1)
                                            j+=(buffer[1]+1)*step
                                            expression._expression__debugClassMessage(currentFacto[2][jSize].content, start, end)
                                            buffer = expression._expression__rangePop(currentFacto[2][jSize].content, start, end)
                                            expression._expression__debugClassMessage(buffer)

                                            if len(buffer) != 0:
                                                buffer = [expression(None, False, None, buffer)]

                                        elif currentFacto[3] == 1:
                                            buffer = expression._expression__rangePop(currentFacto[2], jSize+1, len(currentFacto[2]) - 1)
                                        else:
                                            buffer = expression._expression__rangePop(currentFacto[2], 0, jSize)


                                        #if step != -1:
                                         #   j+=1
                                        j-=step

                                        #Putting the associated expression in parenthesis
                                        lenght = expression._expression__getAssociatedExpression(currentTab, j, step)
                                        expression._expression__debugClassMessage("NINI :", currentTab, lenght, j)
                                                                            

                                        if type(currentTab[j]) == expression:
                                            currentTab[j] = expression(currentTab[j].isFactor, False, None, [currentTab[j]])
                                            currentTab[j].content[0].isFactor = True

                                            if currentTab[j].isFactor == False:
                                                bufferBis = expression(True, False, None, [])
                                                if step == 1:
                                                    #Ajout à droite
                                                    currentTab[j].content.append(bufferBis)
                                                else:
                                                    #Ajout à gauche
                                                    currentTab[j].content = [bufferBis] + currentTab[j].content
                                            else:
                                                bufferBis = currentTab[j]
                                        else:
                                            currentTab[j] = expression(True, False, None, [currentTab[j]])
                                            bufferBis = currentTab[j]

                                        expression._expression__debugClassMessage("MERDE :", currentTab[j], j)

                                        #Putting in parenthesis things who are factor
                                        if(lenght != 0):
                                            bufferBis.content.extend(expression._expression__rangePop(currentTab, j, j+lenght))

                                        #TODO We need to do the same for the common factor if he is at the right (case step == -1)
                                        if step == -1  and j+1 < len(currentTab):
                                            bufferThird = expression(True, False, None, expression._expression__rangePop(currentTab, j+1, j+1+expression._expression__getAssociatedExpression(currentTab, j+1, 1)))
                                            tempBuffer = expression._expression__rangePop(currentTab, j+1, len(currentTab)-1)
                                            currentTab.append(bufferThird)
                                            currentTab.extend(tempBuffer)

                                        stack.pileUp(currentTab)
                                        expression._expression__debugClassMessage("pile up", currentTab, "at index", j)
                                        stack.pileUp(currentTab[j].content)
                                        stack.pileUp( (bufferBis.content, 0, buffer, 1) )

                                        factoOk = True
                                        #if step != -1:
                                         #   j-=1
                                        j+=step

                                        if depth != -1:
                                            expression._expression__debugClassMessage("Sailor : GOING TO THE SPECIAL SURFACE SIR, current level :", currentFacto[0])
                                            j = depth
                                            depth = -1
                                            jSize=len(currentFacto[2])-1

                                            currentTab = currentFacto[0]
                                    
                                    #We need to go deeper
                                    elif depth == -1 and type(currentTab[j]) == expression and (step == -1 or currentTab[j].isFactor != True):
                                        expression._expression__debugClassMessage("Sailor : GOING DEEPER SIR, current level :", currentTab[j].content)
                                        depth = j
                                        j = -1 if step == 1 else len(currentTab[depth].content)
                                        jSize=len(currentFacto[2])-1

                                        currentTab = currentTab[depth].content
                                    
                                    #We need to go on the surface !
                                    elif depth != -1 and (j <= 0 or j >= len(currentTab)-1):
                                        expression._expression__debugClassMessage("Sailor : GOING TO THE SURFACE SIR, current level :", currentFacto[0])
                                        j = depth
                                        depth = -1
                                        jSize=len(currentFacto[2])-1

                                        currentTab = currentFacto[0]

                                    #Oh oh ... we need to speed up the research
                                    #We need to find the next addition !
                                    else:
                                        expression._expression__debugClassMessage("Sailor : INCREASING ENGINE POWER SIR")
                                        jSize=len(currentFacto[2])-1

                                        while j+step<len(currentFacto) and j+step > -1 and (type(currentFacto[j+step]) != expression or currentFacto[j+step].isFactor != False):
                                            j+=step
                                    
                                    j+=step
                                
                                if not factoOk:
                                    if currentFacto[3] == 1 :
                                        #Captain, we need to look from the other side !
                                        stack.pileUp( (currentFacto[0], len(currentFacto[0])-1, currentFacto[2], -1) )
                                    else:
                                        #Captain, it's not possible, we can't find a common factor, we need to put it like newbi !
                                        currentFacto[0].append(expression(False, False, None, currentFacto[2]))

                    #The end of the true factorization          
                    
                    if i < len(self.content):
                        #Captain, we don't know the state, we need to find him !
                        expression._expression__debugClassMessage("Path Finding : Bip. Bip. Starting state path finding, OS version : ImadOss 3.5.78.chocolat")
                        j = i

                        if i == 0:
                            #It's a int or a product
                            currentState = self.state if self.state != None else len(listState)-1
                            lookin = self.content
                        else:
                            #It's a sum and not product because after int we have produtct of int then sum
                            currentState = self.content[i].state if self.content[i].state != None else len(listState)-1
                            lookin = self.content[i].content
                            j = 0
                        
                        toAdd = []

                        while currentState == len(listState)-1 and j < len(lookin) and (isinstance(lookin[j], int) or lookin[j].isFactor):
                            if isinstance(lookin[j], expression) and lookin[j].state != None:
                                currentState = lookin[j].state
                                lookin[j].state = None
                            j+=1
                        expression._expression__debugClassMessage("Path Finding : Finding a state with id", currentState)
                    
                if i < len(self.content):
                    self.content[i].state = None
                    toAdd.append(self.content[i])
                    expression._expression__debugClassMessage("FUCKKKKKKKKK", toAdd)
                    if len(toAdd) == 1 and toAdd[0].isFactor == False:
                        toAdd[0].isFactor = None

            i+=1

        #In theory, we have all we need to update our initial expression
        #first we well add non associated expression if it existe
        #Then the other output
        #The first need to loose his parenthesis
        self.content = []
        self.state = None

        if(len(listState[-1]) != 0):
            expression._expression__debugClassMessage("YAHOU, we have non stated event :", listState[-1])
            self.unparenthesis(currentFacto[0])
            self.content.extend(listState[-1])
        
        expression._expression__debugClassMessage("Merging data bipbip", listState)
        for i in range(len(listState)-1):
            expression._expression__debugClassMessage("Debug at i =", i, ":", listState[i])
            if(len(listState[i]) != 0):
                if(len(self.content) == 0):
                    expression.unparenthesis(listState[i])
                    
                    # If it's already a None isFactor (root type) and have a lenght of 1, 
                    # don't need to put it in content, just repace it
                    if type(listState[i][0]) == int or listState[i][0].isFactor == None:
                        self.content = listState[i]
                    else:
                        self.content.extend(listState[i])
                    

                    self.parentheses()
                    #buffer = expression(None, False, None, listState[i])
                    #buffer = buffer.parentheses()

                    #Checkin where do we need to put our state
                    #If only int -> at the parent
                    #If contain expression -> at the last one
                    if True in [type(e)==expression for e in self.content]:
                        #Contains expression only expression
                        self.content[-1].state = i
                    else:
                        expression._expression__debugClassMessage("WHYYYYYYYYYYYYYYYYYYY")
                        self.state = i
                        
                else:
                    buffer = expression(False, False, None, listState[i])
                    buffer.parentheses()

                    #Checkin where do we need to put our state
                    #If only int -> at the parent
                    #If contain expression -> at the last one
                    if True in [type(e)==expression for e in listState[i]]:
                        #Contains expression
                        buffer.content[-1].state = i
                    else:
                        buffer.state = i

                    expression._expression__debugClassMessage(self.content)
                    self.content.append(buffer)

    def contain(self, obj:list[int|expression]|expression, step=1, start:int=None) -> (int, int):
        """
        Returns how many object element are in self
        Returns the number of index of obj, self check
        """
        if obj == None:
            return 0

        if isinstance(obj, expression):
            obj = obj.content

        if isinstance(obj, int):
            obj = [obj]
        
        diff = 0 if step == 1 else len(obj)-1
        i, end = (0, len(self.content)) if step == 1 else (len(self.content)-1, -1)
        if start != None:
            i = start
            
        result = 0
        strict = False

        expression._expression__debugClassMessage(i, end, step)
        while (i < end and diff-result < len(obj) and step == 1) or (i > end and diff-result > -1 and step == -1):
            expression._expression__debugClassMessage(i, end, step, diff, result)
            expression._expression__debugClassMessage(self.content[i], "==", end=" ")
            expression._expression__debugClassMessage(obj[abs(diff-result)])
            if self.content[i] == obj[abs(diff-result)]:
                expression._expression__debugClassMessage("Sultant of swing", i)
                result += 1
                i+=step

            # obj = _(ab) for example
            elif type(obj[abs(diff-result)]) == expression and obj[abs(diff-result)].isFactor != False and obj[abs(diff-result)].isStar == False and (buff := self.contain(obj[abs(diff-result)], step, i))[0] > 0:
                result += 1
                i+= buff[0]*step
            
            #Factor
            elif type(self.content[i]) == expression and self.content[i].isFactor == True and self.content[i].isStar == False:
                buff = self.content[i].contain(obj[abs(diff-result)], step, i)

                #All obj need to be in self, so if it
                # 's not, returning 0
                if buff[0] == 0:
                    return (0, i)
                
                if buff[0] < len(obj[abs(diff-result)])-1:
                    expression._expression__debugClassMessage("Stric mod change the value")
                    return buff

                #Checking if it's not after
                i+=step
                strict = True
            
            #Sum
            elif type(self.content[i]) == expression and self.content[i].isFactor == False and self.content[i].isStar == False:
                expression._expression__debugClassMessage("It should work")
                buff = self.content[i].contain(obj[abs(diff-result)], step, i)

                #All obj need to be in self, so if it
                # 's not, returning 0
                if buff[0] == 0:
                    return 0
                
                if buff[0] < len(obj[abs(diff-result)])-1:
                    expression._expression__debugClassMessage("Stric mod change the value")
                    return buff

                #Checking if it's not after
                i+=step
                strict = True

            else:
                if strict and len(obj) != result:
                    expression._expression__debugClassMessage("Strict mode change result value")
                    result = 0

                i = i if step == 1 else len(self.content)-1-i
                expression._expression__debugClassMessage("Contain debug : returning", result, ";", i)
                return (result, i)

        if i != end:
            i-=step
        
        if strict and len(obj) != result:
                    expression._expression__debugClassMessage("Strict mode change result value")
                    result = 0

        expression._expression__debugClassMessage(i)
        i = i if step == 1 else len(self.content)-1-i
        expression._expression__debugClassMessage("Contain debug : returning global ", result, ";", i)
        return (result, i)

    def concatenate(self, expr:expression) -> int:
        """
        Return -1 if an error occure
        Return 0 otherwise
        """
        expression._expression__debugClassMessage("Calling concatenate function with :", self, expr)
        if(not isinstance(expr, expression)):
            expression._expression__debugClassMessage("WARNING concatenate function ;: call with non expression objetc")
            return -1

        if len(self.content) == 0 and expr.isFactor != True:
            expression._expression__debugClassMessage("Info concatenate function : self.content was empty")
            self.isStar = expr.isStar
            self.state = expr.state
            self.content = expr.content
        else:
            self.content.append(expression(False, False, None, [expr]))
        return 0

    def breakExpressionDown(self) -> expression:
        """
        Breakdown self into multiple expression with the isFactor == False (+ sign)
        For example _q0[ a +[ a *q0[b +[ c ] ] ] ] // a q0 + a(b + c) q0
        Will return [_q0[ a ] ; _[ b *q0[ b +[ c ] ] ]] // [a q0 ; a(b + c) q0]
        """

        current = expression(None, False, None, [])
        breakDown = []

        for e in self.content:
            if isinstance(e, int):
                current.content.append(e)
                current.isFactor = self.isFactor
                current.isStar   = self.isStar
                current.state    = self.state
            else:
                #Sum, stop the breakdown, creating a new current expression
                if e.isFactor == False:
                    if len(current.content) != 0:
                        breakDown.append(current)
                    current = expression(None, e.isStar, e.state, copy.deepcopy(e.content))

                else:
                    current.append(copy.deepcopy(e))
        
        breakDown.append(current)
        return breakDown

    def addFactor(self, value:int|expression, side:int) -> None:
        """
        Add a factor at the left or the right
        Use expression.__LEFT__ and expression.__RIGHT__ const to select the sideau
        """
        expression._expression__debugClassMessage("addFactor function debug, input =", self, value, side)
        self.parentheses()
        initSize = len(self.content)

        if len(self.content) == 0 and isinstance(value, expression) and value.isFactor != True:
            expression._expression__debugClassMessage("addFactor function info : unpackaking value because self.content was empty")
            self.state = value.state
            self.isStar = value.isStar
            self.content.extend(value.content)

        elif side == expression.__LEFT__:
            buffer = [self.content.pop(0) for i in range(initSize)]
            self.content.append(value)
            self.content.extend(buffer)

        else:
            self.content.append(value)

        expression._expression__debugClassMessage("addFactor function debug, output =", self, value, side)

    def append(self, value:int|expression) -> None:
        """
        Add value at the end of the expression
        This function take the len of self.content to unpack value if necessary
        """

        if len(self.content) == 0 and isinstance(value, expression) and value.isFactor != True:
            expression._expression__debugClassMessage("addFactor function info : unpackaking value because self.content was empty")
            self.state = value.state
            self.isStar = value.isStar
            self.content.extend(value.content)
        else:
            self.content.append(value)

    def ArdenLemma(self, state:int):
        """
        This methods tranform an expression object by using the Arden lemma on state
        It returns a heavy unfactorised expression because it will allow user to perform easely more operation on it
        """

        #Case no expression
        if len(self.content) == 0:
            expression._expression__debugClassMessage("Lemma debug : No content")
            return False

        breakDown = self.breakExpressionDown()

        #Extracting state in self.content
        i = 0
        found = False
        while i < len(breakDown) and not found:
            expression._expression__debugClassMessage("Lemma debug : content of current breakdown :", breakDown[i])
            if breakDown[i].state == state or (isinstance(breakDown[i].content[-1], expression) and breakDown[i].content[-1].state == state):
                found = True
                newExpression = breakDown.pop(i)
            i+=1

        #Can't find state, need to return False
        if not found:
            expression._expression__debugClassMessage("Lemma debug : State not found")
            return False

        #Because self.breakExpressionDown do not empty the main list, we need to do it
        self.content = []
        self.state = None
            

        newExpression.isFactor = True
        newExpression.isStar = True
        if newExpression.state == state:
            newExpression.state = None
        else:
            newExpression.content[-1].state = None

        while len(breakDown) != 0:
            currentBreak = breakDown.pop(0)
            currentBreak.isFactor = True
            if len(self.content) != 0:
                self.content.append(expression(False, False, None, [copy.deepcopy(newExpression), currentBreak]))
            else:
                self.content.extend([copy.deepcopy(newExpression), currentBreak])

        return True

    def containState(self, state, maxDepth=1) -> int|False:
        """
        Return the index in current state if  self contain this state
        return a negatif index if he is not in self.content but in a child expression 
        return True if define in self.state, and False if it was not found
        """

        if maxDepth < 0:
            return False

        if len(self.content) == 0:
            return False

        if self.state == state:
            return -1

        for i in range(len(self.content)):
            e = self.content[i]
            if isinstance(e, expression) and e.isFactor == False and (buffer := e.containState(state, maxDepth-1) != False):
                return -i if isinstance(buffer, int) else i
            elif isinstance(e, expression) and e.state == state:
                return i
        return False


    @staticmethod
    def unparenthesis(lst:list[int|expression]):
        """
        This static methods is use to remove unsed parenthesis of multiple expression
        Because of this initial usage case it's static but a classical way to call it is :
        expression.unparenthesis(expr.content) with expr an expression object

        """
        expression._expression__debugClassMessage("Unparenthesis debug :", lst)
        if lst == None or len(lst) == 0:
            return
        
        i:int = 0
        while i < len(lst):
            #Case int
            if type(lst[i]) != expression:
                if lst[i] == -1 and ( (i > 0 and type(lst[i-1]) == int ) or (i < len(lst)-1 and (type(lst[i+1]) == int or lst[i+1].isFactor == True)) ):
                    lst.pop(i)
                else:
                    i+=1
            
            #Case it's stared
            elif lst[i].isStar == True:
                i+=1

            #Case it's empty or contain -1 (empty word)
            elif len(lst[i].content) == 0 or (len(lst[i].content) == 1 and lst[i].isFactor == True and lst[i].content[0] == -1):
                lst.pop(i)

            #Case unused parenthesis without factor
            elif len(lst[i].content) == 1 and type(lst[i].content[0]) == expression and lst[i].content[0].isFactor != True:
                expression._expression__debugClassMessage("arf", lst[i], lst[i].content[0])
                lst[i].isStar = lst[i].content[0].isStar
                lst[i].state = lst[i].content[0].state
                lst[i].content = lst[i].content[0].content
                i+=1

            #Case factor in only factor
            elif lst[i].isFactor == True and not False in (buffer := [type(lst[i].content[j]) == expression and lst[i].content[j].isFactor == True for j in range(len(lst[i].content))]):
                expression._expression__debugClassMessage("PAPA NOEL", lst[i])
                state = lst[i].state
                content = lst.pop(i).content
                end = expression._expression__rangePop(lst, i, len(lst)-1)

                lst.extend(content)
                lst[-1].state = state
                lst.extend(end)
                i+= len(buffer)

            #Case an None isFactor expression without sum
            elif lst[i].isFactor == None and not False in (buffer := [type(lst[i].content[j]) == int or lst[i].content[j].isFactor == True for j in range(len(lst[i].content))]):
                expression._expression__debugClassMessage("PAPA NOEL", lst[i])
                content = lst.pop(i).content
                end = expression._expression__rangePop(lst, i, len(lst)-1)

                lst.extend(content)
                lst.extend(end)
                i+= len(buffer)

            #Case it's a sum whitout previous modif
            elif lst[i].isFactor == False:
                expression.unparenthesis(lst[i].content)
                i+=1
            
            else:
                i+=1
        
        if len(lst) == 1 and type(lst[0]) == expression and lst[0].isFactor == True and lst[0].isStar == False:
            data = lst[0].content
            lst.pop()
            lst.extend(data)

    def __str__(self, eventList:list=None, stateList:list=None) -> str:
        if eventList == None:
            eventList = self.eventList if self.eventList != None else [str(chr(c)) for c in range(ord('a'), ord('z')+1)]
        
        if stateList == None:
            stateList = self.stateList if self.stateList != None else ["q"+str(i) for i in range(0, 30)]

        result = str()
        temp = str()
        nbValue = 0
        needPar = False

        while nbValue < len(self.content) and isinstance(self.content[nbValue], int):
            result += str(eventList[self.content[nbValue]])+" " if self.content[nbValue] != -1 else str('\u03b5 ')
            nbValue+=1
        
        while nbValue < len(self.content) and self.content[nbValue].isFactor == True:
            result += self.content[nbValue].__str__(eventList, stateList)
            nbValue+=1
        
        #Use to remove the last unsed space
        if len(result) > 0 and result[-1] == " ":
            result = result[:len(result)-1]

        while nbValue < len(self.content):
            if self.content[nbValue].isFactor == False:
                needPar = True

            temp += self.content[nbValue].__str__(eventList, stateList)
            nbValue += 1

        if self.isStar == True and not(needPar and self.isFactor):
            if len(result) > 1:
                result  = "(" + result + ")* "
            else:
                result += "* "

        if needPar and self.isFactor:
            result  = "(" + result + temp + ")"

            if self.isStar == True:
                result += "* "

            if self.state != None:
                result += " " + stateList[self.state]

        else:
            if self.state != None:
                result += " " + stateList[self.state]

            result += temp
        
        if self.isFactor == False:
            result = " + " + result

        return result
        
    def __repr__(self: expression, end:str=""):
        if self.isFactor == None:
            op = "_"
        elif(self.isFactor):
            op = "*"
        else:
            op = "+"

        if self.state != None:
            st = "q"+str(self.state)
        else:
            st = ""

        if self.isStar:
            star = "^"
        else:
            star = ""
        
        result = op+st+star+"[ "
        for e in self.content:
            if(type(e) == expression):
                result += e.__repr__(end=" ")
            else:
                result += (str(e) + " ")
            
        result += "]" + end

        return result

    @staticmethod
    def __rangePop(list:list, start:int, end:int) -> list:
        """
        This is a private static methode
        Remove a range of a list and return the value, end is also remove
        """
        expression._expression__debugClassMessage("Calling __rangePop with :", list, start, end)
        return [list.pop(start) for i in range(start, end+1)]

    @staticmethod
    def __getAssociatedExpression(tab:list[int|expression], index:int, step=1):
        """
        This is a private static function
        Return lenth of associated expression in a expression objet
        Step define if we read from th left or the right
        For example : ab + cd(g+h) + rt
            - with index = 3 (+ rt) returns 0 (+ rt)
            - with index = 0 (a) returns 1 (ab)
        """
        expression._expression__debugClassMessage("__getAssociatedExpression call with", tab, index, step)
        if(step != 1 and step != -1):
            return 0
        
        if(tab == None or len(tab) == 0):
            return 0
        
        if type(tab[index]) == expression and tab[index].isFactor == False:
            return 0

        lenght = step
        while index+lenght < len(tab) and index+lenght > -1 and (type(tab[index+lenght]) != expression or tab[index+lenght].isFactor):
            lenght+=step

        return abs(lenght-step)

    @staticmethod
    def __debugClassMessage(*values:object, sep: Optional[str] =" ", end: Optional[str] = "\n" ) -> None:
        """
        This is a private stati function
        Allow class methods and function to print debug message if user need it
        Debug message can be activate/desactivate with expression.setDebugEnable(enable:bool) function
        """
        if expression.debug:
            print(*values, sep=sep, end=end)

    @staticmethod
    def setDebugEnable(enable:bool) -> None:
        """
        This function allow the user to activate/desactivate debug message of this class
        """
        expression.debug = enable


if False:
    #Test à la wanagun
    #e1 : (a + b)c * q0 + bc * q0
    #     _[ *[a; +[b] ]; *q0[c] +q0[b ; c]]
    print("e1 :")
    e1 = expression(None, False, None, [ expression(True, False, None, [0, expression(False, False, None, [1])]), expression(True, False, 0, [2]), expression(False, False, 0, [1, 2]) ])
    print("Testing expression e1 :", e1)
    e1.factorize(1)
    print("Result of factorization :", e1)
    if repr(e1) != "_[ *[ 0 +[ 1 ] ] *q0[ 2 ] ]":
        print("ALERTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT GENERAAAAAAAAAAALLLL")
    print("\n")

    #e2 : abc * q0
    # _q0[a; b; c]
    print("e2 : ")
    e2 = expression(None, False, 0, [0,1,2])
    print("Testing expression e2 :", e2)
    e2.factorize(1)
    print("Result of factorization :", e2)
    if repr(e2) != "_q0[ 0 1 2 ]":
        print("ALERTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT GENERAAAAAAAAAAALLLL")
    print("\n")

    #e3 : ab * q0 + c * q0
    print("e3 : ")
    e3 = expression(None, False, 0, [0,1, expression(False, False, 0, [2])])
    print("Testing expression e3 :", e3)
    e3.factorize(1)
    print("Result of factorization e3 :", e3)
    if repr(e3) != "_[ *q0[ 0 1 +[ 2 ] ] ]":
        print("ALERTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT GENERAAAAAAAAAAALLLL")
    print("\n")

    #e4 : ab * q0 + c * q1
    print("e4 : ")
    e4 = expression(None, False, 0, [0,1, expression(False, False, 1, [2])])
    print("Testing expression e4 :", e4)
    e4.factorize(2 )
    print("Result of factorization e4 :", e4)
    if repr(e4) != "_q0[ 0 1 +q1[ 2 ] ]":
        print("ALERTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT GENERAAAAAAAAAAALLLL")
    print("\n")

    #e5 : (a + b)^ * q0 + c * q0 -> ( (a + b)^ + c )q0 
    #        -> _[ *q0^[ 0 +[ 1 ] ] +q0[ 2 ] ]
    # result -> _[ *q0[ *^[ 0 +[ 1 ] ] +[ 2 ] ] ]
    print("e5")
    e5 = expression(None, False, None, [expression(True, True, 0, [0, expression(False, False, None, [1]) ]), expression(False, False, 0, [2]) ])
    print("Testing expression e5 :", e5)
    e5.factorize(1)
    print("Result of factorization e5 :", e5)
    if repr(e5) != "_[ *q0[ *^[ 0 +[ 1 ] ] +[ 2 ] ] ]":
        print("ALERTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT GENERAAAAAAAAAAALLLL")
    print("\n")

    #e6 : (a + b) * q0 + c * q0 -> ( (a + b + c )q0 
    #        -> _[ *q0[ 0 +[ 1 ] ] +q0[ 2 ] ]
    # result -> _[ *q0[ 0 +[ 1 ] +[ 2 ] ] ]
    print("e6")
    e6 = expression(None, False, None, [expression(True, False, 0, [0, expression(False, False, None, [1]) ]), expression(False, False, 0, [2]) ])
    print("Testing expression e5 :", e6)
    e6.factorize(1)
    print("Result of factorization e5 :", e6)
    if repr(e6) != "_[ *q0[ 0 +[ 1 ] +[ 2 ] ] ]":
        print("ALERTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT GENERAAAAAAAAAAALLLL")
    print("\n")

    #e7 : abc * q0 + ab * q0
    # -> ab(c + ε) * q0
    print("e7 : ")
    e7 = expression(None, False, 0, [0,1,2, expression(False, False, 0, [0, 1])])
    print("Testing expression e7 :", e7)
    e7.factorize(1)
    print("Result of factorization e7 :", e7)
    if repr(e7) != "_[ 0 1 *q0[ 2 +[ -1 ] ] ]":
        print("ALERTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT GENERAAAAAAAAAAALLLL")
    print("\n")