import json
with open('sample.json', 'r') as openfile:
    ast=json.load(openfile)
#print(type(ast))
data=ast['body']

A,L,C=tuple(),tuple(),tuple()

#function for operator
def operator(op):
    
    if op['_type']=='Sub':
        return "-"
    elif op['_type']=='Add':
        return "+"
    elif op['_type']=='Mult':
        return "*"
    elif op['_type']=='Div':
        return "/"
    elif op['_type']=='Mod':
        return "%"
    elif op['_type']=='Pow':
        return "**"
    elif op['_type']=='BitOr':
        return "|"
    elif op['_type']=='BitAnd':
        return "&"
    elif op['_type']=='BitXor':
        return "^"
    elif op['_type']=='LShift':
        return "<<"
    elif op['_type']=='RShift':
        return ">>"
    elif op['_type']=='FloorDiv':
        return "//"

#function for operation 
def operation(ops):
    
    for op in ops:
        if op['_type']=='Gt':
            return ">"
        elif op['_type']=='Lt':
            return "<"
        elif op['_type']=='LtE':
            return "<="
        elif op['_type']=='GtE':
            return ">="
        elif op['_type']=='Eq':
            return "=="
        elif op['_type']=='NotEq':
            return "!="

#function for AugAssign
def AugAssign(targets,p,value):
    s=""
    if value['_type']=='Constant':
        s=str(value['value'])
    elif value['_type']=='Name':
        s=str(value['id'])
    print("Assignment Statement: "+targets['id']+str(p)+"="+s)

#function for Assignment 
def Assignment(targets,value):
    s=""
    if value['_type']=='Constant':
        s=str(value['value'])
        
    elif value['_type']=='BinOp':
        w,x,v,p=0,0,0,0
        for k in value['right']:
            if k=='value':
                v=1
            if k=='id':
                p=1
        for k in value['left']:
            if k=='value':
                w=1
            if k=='id':
                x=1
        if v and w:
            s=str(value['left']['value'])+operator(value['op'])+str(value['right']['value'])
        if x and v:
            s=str(value['left']['id'])+operator(value['op'])+str(value['right']['value'])
        if p and x:
            s=str(value['left']['id'])+operator(value['op'])+str(value['right']['id'])
        if p and w:
            s=str(value['left']['value'])+operator(value['op'])+str(value['right']['id'])
    if targets==0:
        return str(s)
            
    for target in targets:
        print("Assignment Statement: "+target['id']+" = "+s)

#function for while loop 
def whileLoop(body,test):
    #print(type(body))
    for i in body:
        if i['_type']=='While':
            whileLoop(i['body'],i['test'])
        elif i['_type']=='Assign':
            Assignment(i['targets'],i['value'])
        elif i['_type']=='For':
            forLoop(i['body'],i['iter'],i['target'])
        elif i['_type']=='AugAssign':
            s=operator(i['op'])
            AugAssign(i['target'],s,i['value'])
        elif i['_type']=='Exp':
            return
    ops=operation(test['ops'])
    s=""
    for comp in test['comparators']:
        if comp['_type']=='Constant':
            s+=str(comp['value'])
        elif comp['_type']=='Name':
            s+=comp['id']
        
        print("Loop Condition: "+test['left']['id']+ops+s)
    #print(type(test))

#function for for loop
def forLoop(body,iterable,target):
    #print(type(body))
    for i in body:
        if i['_type']=='For':
            forLoop(i['body'],i['iter'],i['target'])
        elif i['_type']=='Assign':
            Assignment(i['targets'],i['value'])
        elif i['_type']=='AugAssign':
            s=operator(i['op'])
            AugAssign(i['target'],s,i['value'])
        elif i['_type']=='While':
            whileLoop(i['body'],i['test'])
        elif i['_type']=='Exp':
            return
    #print(type(iterable))
    s=""
    for j in iterable['args']:
        if j['_type']=='Constant':
            s+=str(j['value'])
        elif j['_type']=='Name':
            s+=j['id']
        elif j['_type']=='BinOp':
            s+=str(Assignment(0,j))
        s+=","
    print("Loop condition: "+str(target['id'])+" in "+str(iterable['func']['id'])+"("+s[0:-1]+")")      
    #print(type(target))

#function for condition(if else)
def condition(body,orelse,test):
    #print(type(body))
    for i in body:
        if i['_type']=='If':
            condition(i['body'],i['orelse'],i['test'])
        elif i['_type']=='For':
            forLoop(i['body'],i['iter'],i['target'])
        elif i['_type']=='While':
            whileLoop(i['body'],i['test'])
        elif i['_type']=='Assign':
            Assignment(i['targets'],i['value'])
        elif i['_type']=='AugAssign':
            s=operator(i['op'])
            AugAssign(i['target'],s,i['value'])
        elif i['_type']=='Exp':
            return
    if len(orelse)>0:
        for j in orelse:
            if j['_type']=='If':
                condition(j['body'],j['orelse'],j['test'])
            elif j['_type']=='For':
                forLoop(j['body'],j['iter'],j['target'])
            elif j['_type']=='While':
                whileLoop(j['body'],j['test'])
            elif j['_type']=='Assign':
                Assignment(j['targets'],j['value'])
            elif j['_type']=='AugAssign':
                s=operator(j['op'])
                AugAssign(j['target'],s,j['value'])
            elif j['_type']=='Exp':
                return
        
            
    ops=operation(test['ops'])
    s=""
    for comp in test['comparators']:
        if comp['_type']=='Constant':
            s+=str(comp['value'])
        elif comp['_type']=='Name':
            s+=comp['id'] 
    print("Branch condition: "+test['left']['id']+ops+s)
    
#Main function
for i in data:
    if i['_type']=='Assign':
        Assignment(i['targets'],i['value'])
    elif i['_type']=='AugAssign':
            s=operator(i['op'])
            AugAssign(i['target'],s,i['value'])
    elif i['_type']=='For':
        forLoop(i['body'],i['iter'],i['target'])
    elif i['_type']=='While':
        whileLoop(i['body'],i['test'])
    elif i['_type']=="If":
        condition(i['body'],i['orelse'],i['test'])
