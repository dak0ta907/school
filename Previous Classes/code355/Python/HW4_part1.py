#Garrett Rudisill
#CptS 355 HW4 part 1
#WSU ID 11461816
#PostScript interpreter part 1 in python 3.6
#tested on both linux and windows

#opstack portion
opstack = []

def opPop():
    #pop a item off stack if its not empty
    if len(opstack) > 0:
        return opstack.pop()
    else:
        print("Op stack is empty")

def opPush(val):
    #push things to the stack
    #functions error check, so we dont need to check whats pushed
    opstack.append(val)

#dictionary stack
#-----------------------
dictstack = []

def dictPop():
    #pop from dictionary if there is an item inside
    if len(dictstack) > 0:
        return dictstack.pop()
    else:
        print("Dict stack is empty")

def dictPush(d):
    #append to dictstack
    dictstack.append(d)

def define(name,val):
    if name[0] =='/':#check for / character symbolizing a var def
        name = name[1:]#rem /
        if dictstack == []:#if dictionary stack empty
            d = {}
            d[name] = val
            dictstack.append(d) #append new dict with val to dictstack
        else:
            (dictstack[-1])[name]=val #update if not empty
    else:
        print("variable not defined")

#check this
def lookup(name):
    operable_dict = reversed(dictstack) #if more than one dict, ensure from top of stack to bottom
    for d in operable_dict:
        if name in d:
            return d[name]
    else:
        print("Name is not defined")

#we gon shoot at ops
#-----
#add
#sub 
#mul
#div
#mod
def add():
    try:
        op1 = opPop()
        op2 = opPop()
        #type checking
        if isinstance(op1,(int,float)) and isinstance(op2,(int,float)):
            opstack.append(op1+op2)
        else:
            print("Invalid inputs")
    except:
        print("not enough args")

def sub():
    try:
        op1 = opPop()
        op2 = opPop()
        #type checking
        if isinstance(op1,(int,float)) and isinstance(op2,(int,float)):
            opstack.append(op2-op1)
        else:
            print("Invalid inputs")
    except:
        print("not enough args")

def mul():
    try:
        op1 = opPop()
        op2 = opPop()
        #type checking
        if isinstance(op1,(int,float)) and isinstance(op2,(int,float)):
            opstack.append(op2*op1)
        else:
            print("Invalid inputs")
    except:
        print("not enough args")

def div():
    try:
        op1 = opPop()
        op2 = opPop()
        if op2 == 0:
            print("div by 0 error")
            return
        elif op1 == 0 and op2 == 0:
            print("div by 0 error")
            return
        elif op1 == 0:
            opstack.append(0)
            return
        else:
            pass
        #type checking
        if isinstance(op1,(int,float)) and isinstance(op2,(int,float)):
                opstack.append(op2/op1)
        else:
            print("invalid inputs")
    except:
        print("not enough args")

def mod():
    try:
        op1 = opPop()
        op2 = opPop()
        #type checking
        #mods are probably int only?
        if isinstance(op1,int) and isinstance(op2,int):
            opstack.append(op2%op1)
        else:
            print("invalid ops")
    except:
        print("not enough args")


#array ops
#---------
#length
#get

def length():
    temp = opPop()
    if isinstance(temp, list): #check for array before len call
        opPush(len(temp))
    else:
        print("type error")

def get():
    ar_ind = opPop()
    arr = opPop()
    if isinstance(arr, list):
        try:
            opPush(arr[ar_ind])
        except:
            print("out of index error")
    else:
        print("type error - not array")

    
#stack manip ops
#--------
#dup, exch, pop, roll , copy, clear, stack

def dup():
    op1 = opPop()
    opstack.append(op1)
    opstack.append(op1)
    #works, could be more efficient, but I dont really care

def exch():
    op1 = opPop()
    op2 = opPop()
    if op1 == None or op2 == None:
        print("cant exchange some with none")
        return
    opstack.append(op1)
    opstack.append(op2)
    #ol' reddit switcheroo

def pop():
    _ = opPop()
    #trash a op

def clear():
    opstack.clear()
    #nuclear launch @ stack detected

def copy():
    try:#how many items to copy
        numItems = int(opPop()) #cast to an int if possible
    except:
        print("Item is null/unsucessfully converted to int")
        return
    if numItems > len(opstack) or numItems < 0:
        print("negative items or attempting to copy nonexistent items")
        return
    else:
        #operation execution
        i = 0
        temp = []
        operableStack = list(reversed(opstack))
        #reversed for easy linear traversal
        while i < numItems: #iterate for i number of items
            #get num items
            temp.append(operableStack[i])
            i+=1            
        for val in temp:#appened all the values that need to be copied
            opstack.append(val)
        

    

def roll():
    if len(opstack) <=2 : #stack 2 short
        print("not enough args, cant roll")
        return
    rolls = opPop() # num of rolls
    items = opPop() # num of items to be rolled
    if not isinstance(rolls,int) or not isinstance(items,int): #datatype check
        print("invalid args")
        return
    elif items < 0:
        print("invalid index")
        return
    elif items <2:
        return #no change to stack
    
    else: #actually perform op
        if rolls >=0 : #roll data to bottom from top
            items = -items +1 #index correction
            for count in range(rolls):
                val = opPop()
                opstack[items:items-1]=[val]
        else:
            #roll data to top from bottom
            items = -items
            rolls = -rolls
            for count in range(rolls):
                val = opPop()
                opstack[items:items-1]=[val]

#print le stack
def stack():
    printable = reversed(opstack)
    for ent in printable:
        print(ent)

#dick manip ops
#------
#psDict, begin, end, psDef
def psDict():
    if opPop() != None:
        opPush({})
    else:
        print("operation not completed")

#push a dict to dictstack
def begin():
    temp = opPop()
    if isinstance(temp, dict):
        dictPush(temp)
    else:
        print("not a dictionary")

#pop off dictstact
def end():
    if dictstack != None:
        dictPop()
    else:
        print("dict empty, nothing to pop from end")

#define stuff
def psDef():
    val = opPop()
    name = opPop()
    define(name,val)

#------- Part 1 TEST CASES--------------
def testDefine():
    define("/n1", 4)
    if lookup("n1") != 4:
        return False
    define("test",4)
    if lookup("test") == 4:
        return False
    return True

def testLookup():
    opPush("/n1")
    opPush(3)
    psDef()
    if lookup("n1") != 3:
        return False
    if lookup("n2") == 2:
        return False
    return True

#Arithmatic operator tests
def testAdd():
    opPush(1)
    opPush(2)
    add()
    if opPop() != 3:
        return False
    clear()
    add()
    opPush("test")
    opPush(-2)
    add()
    return True

def testSub():
    opPush(10)
    opPush(4.5)
    sub()
    if opPop() != 5.5:
        return False
    clear()
    sub()
    opPush("string")
    opPush(123)
    sub()
    
    return True

def testMul():
    opPush(2)
    opPush(4.5)
    mul()
    if opPop() != 9:
        return False
    clear()
    mul()
    opPush("string")
    opPush(123)
    mul()
    return True

def testDiv():
    opPush(10)
    opPush(4)
    div()
    if opPop() != 2.5:
        return False
    
    clear()
    div()
    
    opPush(0)
    opPush(10)
    div()
    
    opPush(10)
    opPush(0)
    if opPop() != 0:
        return False

    return True

def testMod():
    opPush(10)
    opPush(3)
    mod()
    if opPop() != 1:
        return False
    opPush(3.5)
    opPush(2)
    mod()

    opPush(0)
    opPush(10)
    mod()
    if opPop() != 0:
        return False

    opPush(10)
    opPush(0)
    mod()
    if opPop() != 10:
        return False

    clear()
    mod()

    opPush("string")
    opPush(123)
    mod()
    return True

#Array operator tests
def testLength():
    opPush([1,2,3,4,5])
    length()
    if opPop() != 5:
        return False
    opPush("strong")
    length()
    
    clear()
    length()

    opPush([])
    length()

    if opPop() != 0:
        return False
    return True

def testGet():
    opPush([1,2,3,4,5])
    opPush(4)
    get()
    if opPop() != 5:
        return False
    opPush([])
    opPush(4)
    get()

    opPush("sring")
    opPush(4)
    get()

    clear()
    get()
    return True

#stack manipulation functions
def testDup():
    opPush(10)
    dup()
    if opPop()!=opPop():
        return False
    clear()
    dup()

    opPush("string")
    dup()
    if opPop() != "string":
        return False
    return True

def testExch():
    opPush(10)
    opPush("/x")
    exch()
    if opPop()!=10 and opPop()!="/x":
        return False
    clear()
    exch()

    opPush(1)
    exch()
    return True

def testPop():
    l1 = len(opstack)
    opPush(10)
    pop()
    l2= len(opstack)
    if l1!=l2:
        return False

    clear()
    opPop()

    return True

def testRoll():
    opPush(1)
    opPush(2)
    opPush(3)
    opPush(4)
    opPush(5)
    opPush(4)
    opPush(-2)
    roll()
    if opPop()!=3 and opPop()!=2 and opPop()!=5 and opPop()!=4 and opPop()!=1:
        return False
    opPush("other stuff")
    opPush(0)
    opPush(2)
    roll()
    
    clear()
    roll()
    return True

def testCopy():
    opPush(1)
    opPush(2)
    opPush(3)
    opPush(4)
    opPush(5)
    opPush(2)
    copy()
    if opPop()!=5 and opPop()!=4 and opPop()!=5 and opPop()!=4 and opPop()!=3 and opPop()!=2:
        return False

    clear()
    copy()

    opPush(-1)
    copy()

    return True

def testClear():
    opPush(10)
    opPush("/x")
    clear()
    if len(opstack)!=0:
        return False
    return True

#dictionary stack operators
def testDict():
    opPush(1)
    psDict()
    if opPop()!={}:
        return False
    return True

def testBeginEnd():
    opPush("/x")
    opPush(3)
    psDef()
    opPush({})
    begin()
    opPush("/x")
    opPush(4)
    psDef()
    end()
    if lookup("x")!=3:
        return False
    return True

def testpsDef():
    opPush("/x")
    opPush(10)
    psDef()
    if lookup("x")!=10:
        return False
    return True

def testpsDef2():
    opPush("/x")
    opPush(10)
    psDef()
    opPush(1)
    psDict()
    begin()
    if lookup("x")!=10:
        end()
        return False
    end()
    return True


def main():
    
    testCases = [('define',testDefine),('lookup',testLookup),('add', testAdd), ('sub', testSub),('mul', testMul),('div', testDiv),  ('mod', testMod), \
                ('length', testLength),('get', testGet), ('dup', testDup), ('exch', testExch), ('pop', testPop), ('roll', testRoll), ('copy', testCopy), \
                ('clear', testClear), ('dict', testDict), ('begin', testBeginEnd), ('psDef', testpsDef), ('psDef2', testpsDef2)]
    # add you test functions to this list along with suitable names
    for tests in testCases:
        #print(tests[0] +" test = "+ str(tests[1]()))
        if tests[1] == False:
            print(str(tests[0])+" test failed")
    else:
        print("Tests passed")

def main_part1():
    testCases = [('define',testDefine),('lookup',testLookup),('add', testAdd), ('sub', testSub),('mul', testMul),('div', testDiv),  ('mod', testMod), \
                ('length', testLength),('get', testGet), ('dup', testDup), ('exch', testExch), ('pop', testPop), ('roll', testRoll), ('copy', testCopy), \
                ('clear', testClear), ('dict', testDict), ('begin', testBeginEnd), ('psDef', testpsDef), ('psDef2', testpsDef2)]
    # add you test functions to this list along with suitable names
    failedTests = [testName for (testName, testProc) in testCases if not testProc()]
    if failedTests:
        return ('Some tests failed', failedTests)
    else:
        return ('All part-1 tests OK')

if __name__ == '__main__':
    print("comment out main() to not run tests")
    print(main_part1())

    print("\n\n")
    print("comment out line 587 to stop tests")
    print("error catch cases will print out, not effect output and thus tests should pass")
    print("Error catch messages are for tests of a empty stack, or improper data input")
    print("There are also tests for div/0 errors in the div function \n")