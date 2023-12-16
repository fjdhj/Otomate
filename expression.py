from __future__ import annotations

from pile import pile

class expression:
    debug = False
    def __init__(self, isFactor:bool|None, isStar: bool|None, state: int|None, content, stateList:list[str]=None, eventList:list[str]=None) -> None:
        self.isFactor: bool|None=isFactor
        self.isStar: bool|None=isStar
        self.state: int|None=state #Indice de l'état
        self.content: list|int|expression=content

        self.stateList: list = stateList
        self.eventList: list = eventList


    def parentheses(self):
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
                    currentState:int = self.state if self.state != None else numberOfState+1

                    #if we don't have a currentState, we need to check if it's not after
                    while(currentState == numberOfState+1 and j< len(self.content) and (type(self.content[j]) != expression or self.content[j].isFactor) ):
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
                                            start, end = (0, buffer[0]-1) if step == -1 else (buffer[0], len(currentFacto[2]) - 1)
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
                        j = i+1

                        if i == 0 and type(self.content[0]) == int:
                            currentState = self.state if self.state != None else len(listState)-1
                        else:
                            currentState = self.content[i].state if self.content[i].state != None else len(listState)-1
                        
                        toAdd = []

                        while currentState == len(listState)-1 and j < len(self.content) and self.content[j].isFactor:
                            if self.content[j].state != None:
                                currentState = self.content[j].state
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

    #Returns au many object element are in self
    #Returns the number of index of obj, self check
    def contain(self, obj:list[int|expression]|expression, step=1, start:int=None) -> (int, int):
        if obj == None:
            return 0

        if type(obj) == expression:
            obj = obj.content
        
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
                    return 0
                
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


    @staticmethod
    def unparenthesis(lst:list[int|expression]):
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

            #Case it's empty
            elif len(lst[i].content) == 0:
                lst.pop(i)

            #Case unused parenthesis without factor
            elif len(lst[i].content) == 1 and type(lst[i].content[0]) == expression and lst[i].content[0].isFactor != True:
                expression._expression__debugClassMessage("arf", lst[i], lst[i].content[0])
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

        while nbValue < len(self.content) and type(self.content[nbValue]) == int:
            result += str(eventList[self.content[nbValue]])+" " if self.content[nbValue] != -1 else str('\u03b5 ')
            nbValue+=1
        
        #Use to remove the last unsed space
        result = result[:len(result)-1]

        while nbValue < len(self.content):
            if self.content[nbValue].isFactor == False:
                needPar = True

            temp += self.content[nbValue].__str__(eventList, stateList)
            nbValue += 1

        if self.isStar == True and not(needPar and self.isFactor):
            result  = "(" + result + ")*"

        if needPar and self.isFactor:
            result  = "(" + result + temp + ")"

            if self.isStar == True:
                result += "*"

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
    #Remove a range of a list and return the value, end is also remove
    def __rangePop(list:list, start:int, end:int) -> list:
        expression._expression__debugClassMessage("Calling __rangePop with :", list, start, end)
        return [list.pop(start) for i in range(start, end+1)]

    """
    Return lenth of associated expression in a expression objet
    Step define if we read from th left or the right
    For example : ab + cd(g+h) + rt
        - with index = 3 (+ rt) returns 0 (+ rt)
        - with index = 0 (a) returns 1 (ab)
    """
    @staticmethod
    def __getAssociatedExpression(tab:list[int|expression], index:int, step=1):
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

    def affichage(self: expression):
        print(self)

    @staticmethod
    def __debugClassMessage(*values:object, sep: Optional[str] =" ", end: Optional[str] = "\n" ):
        if expression.debug:
            print(*values, sep=sep, end=end)

    @staticmethod
    def setDebugEnable(enable:bool):
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