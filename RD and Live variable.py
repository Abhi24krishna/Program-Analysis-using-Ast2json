class A():
    def __init__(self,V,c,edges,gen,kill):
        self.V=V
        self.c=0
        self.edges=edges
        self.gen=gen
        self.kill=kill
    #function for operator
    def operator(self,op):
    
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
    def operation(self,ops):
    
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
            
    def exp(self,value):
        s=""
        p=""
        if len(value['args'])>0:
            for i in value['args']:
                if i['_type']=='Name':
                    p+=i['id']                    
                    self.gen[self.c].append(i['id'])
                elif i['_type']=='Call':
                    p+=i['func']['id']+'('
                    for j in i['args']:
                        p+=j['id']
                        self.gen[self.c].append(j['id'])
                        p+=','
                    p+=')'
                elif i['_type']=='Constant':
                    p+=str(i['value'])
                elif i['_type']=='BinOp':
                    v1,v2=0,0
                    for k in i['left']:
                        if k=='value':
                            v1=1
                        if k=='id':
                            v2=1
                    if v1:
                        p+=str(i['left']['value'])
                    if v2:
                        p+=i['left']['id']
                        self.gen[self.c].append(i['left']['id'])
                    p+=str(obj.operator(i['op']))
                    v1,v2=0,0
                    for k in i['right']:
                        if k=='value':
                            v1=1
                        if k=='id':
                            v2=1
                    if v1:
                        p+=str(i['right']['value'])
                    if v2:
                        p+=i['right']['id']
                        self.gen[self.c].append(i['right']['id'])
                p+=','
        if value['_type']=='Call':
            s+=value['func']['id']+'('+p[0:-1]+')'
        if self.c in self.V:
            self.V[self.c]+=s+"\n"
        else:
            self.V[self.c]=s+"\n"

    #function for AugAssign
    def AugAssign(self,targets,op,value):
        #print(p)
        s=""
        if value['_type']=='Constant':
            s=str(value['value'])
        elif value['_type']=='Name':
            s=str(value['id'])
            self.gen[self.c].append(value['id'])
        elif value['_type']=='Call':
            p=""
            if len(value['args'])>0:
                for i in value['args']:
                    if i['_type']=='Name':
                        p+=i['id']
                        self.gen[self.c].append(i['id'])
                    elif i['_type']=='Call':
                        p+=i['func']['id']+'()'
                    elif i['_type']=='Constant':
                        p+=str(i['value'])
                    elif i['_type']=='BinOp':
                        v1,v2=0,0
                        for k in i['left']:
                            if k=='value':
                                v1=1
                            if k=='id':
                                v2=1
                        if v1:
                            p+=str(i['left']['value'])
                        if v2:
                            p+=i['left']['id']
                            self.gen[self.c].append(i['left']['id'])
                        p+=str(obj.operator(i['op']))
                        v1,v2=0,0
                        for k in i['right']:
                            if k=='value':
                                v1=1
                            if k=='id':
                                v2=1
                        if v1:
                            p+=str(i['right']['value'])
                        if v2:
                            p+=i['right']['id']
                            self.gen[self.c].append(i['right']['id'])
                    p+=','
            s=value['func']['id']+'('+p[0:-1]+')'
        elif value['_type']=='Compare':
            w,x=0,0
            for k in value['left']:
                if k=='value':
                    w=1
                if k=='id':
                    x=1
            l=str()
            n,m=0,0
            for i in value['comparators']:
                for j in i:
                    if j=='value':
                        n=1
                    if j=='id':
                        m=1
            if n:
                l=value['comparators'][0]['id']
                self.gen[self.c].append(value['comparators'][0]['id'])
            if m:
                l=value['comparators'][0]['value']
            if w:
                s=str(value['left']['value'])+obj.operation(value['ops'])+str(l)
            if x:
                s=str(value['left']['id'])+obj.operation(value['ops'])+str(l)
                self.gen[self.c].append(value['left']['id'])
            if targets==0:
                return str(s)
        elif value['_type']=='BinOp':
            w,x,v,p,t,y=0,0,0,0,0,0
            m=""
            n=""
            for k in value['left']:
                if k=='value':
                    w=1
                if k=='id':
                    x=1
                    self.gen[self.c].append(value['left']['id'])
                if k=='func':
                    y=1
                    self.gen[self.c].append(value['left']['func']['id'])
            if y:
                for i in value['left']['args']:
                    if i['_type']=='Name':
                        m+=i['id']
                        self.gen[self.c].append(i['id'])
                    elif i['_type']=='Call':
                        m+=i['func']['id']+'()'
                    elif i['_type']=='Constant':
                        m+=str(i['value'])
                    elif i['_type']=='BinOp':
                        v1,v2=0,0
                        for k in i['left']:
                            if k=='value':
                                v1=1
                            if k=='id':
                                v2=1
                        if v1:
                            m+=str(i['left']['value'])
                        if v2:
                            m+=i['left']['id']
                            self.gen[self.c].append(i['left']['id'])
                        m+=str(obj.operator(i['op']))
                        v1,v2=0,0
                        for k in i['right']:
                            if k=='value':
                                v1=1
                            if k=='id':
                                v2=1
                        if v1:
                            m+=str(i['right']['value'])
                        if v2:
                            m+=i['right']['id']
                            self.gen[self.c].append(i['right']['id'])
                    m+=','
                    
            for k in value['right']:
                if k=='value':
                    v=1
                if k=='id':
                    p=1
                    self.gen[self.c].append(value['right']['id'])
                if k=='func':
                    t=1
                    self.gen[self.c].append(value['right']['func']['id'])
            if t:
                for i in value['right']['args']:
                    if i['_type']=='Name':
                        n+=i['id']
                        self.gen[self.c].append(i['id'])
                    elif i['_type']=='Call':
                        n+=i['func']['id']+'()'
                    elif i['_type']=='Constant':
                        n+=str(i['value'])
                    elif i['_type']=='BinOp':
                        v1,v2=0,0
                        for k in i['left']:
                            if k=='value':
                                v1=1
                            if k=='id':
                                v2=1
                        if v1:
                            n+=str(i['left']['value'])
                        if v2:
                            n+=i['left']['id']
                            self.gen[self.c].append(i['left']['id'])
                        n+=str(obj.operator(i['op']))
                        v1,v2=0,0
                        for k in i['right']:
                            if k=='value':
                                v1=1
                            if k=='id':
                                v2=1
                        if v1:
                            n+=str(i['right']['value'])
                        if v2:
                            n+=i['right']['id']
                            self.gen[self.c].append(i['right']['id'])
                    n+=','
            
            if v and w:
                s=str(value['left']['value'])+obj.operator(value['op'])+str(value['right']['value'])
            if x and v:
                s=str(value['left']['id'])+obj.operator(value['op'])+str(value['right']['value'])
            if p and x:
                s=str(value['left']['id'])+obj.operator(value['op'])+str(value['right']['id'])
            if p and w:
                s=str(value['left']['value'])+obj.operator(value['op'])+str(value['right']['id'])
            if w and t:
                s=str(value['left']['value'])+obj.operator(value['op'])+str(value['right']['func']['id'])+'('+n[0:-1]+')'
            if v and y:
                s=str(value['left']['func']['id'])+'('+m[0:-1]+')'+obj.operator(value['op'])+str(value['right']['id'])
            if x and t:
                s=str(value['left']['id'])+obj.operator(value['op'])+str(value['right']['func']['id'])+'('+n[0:-1]+')'
            if y and t:
                s=str(value['left']['func']['id'])+'('+m[0:-1]+')'+obj.operator(value['op'])+str(value['right']['func']['id'])+'('+n[0:-1]+')'
            if y and p:
                s=str(value['left']['func']['id'])+'('+m[0:-1]+')'+obj.operator(value['op'])+str(value['right']['id'])
                
        #print("Assignment Statement: "+targets['id']+str(p)+"="+s)
        if self.c in self.V:
            self.V[self.c]+=targets['id']+str(op)+"="+s+"\n"
        else:
            self.V[self.c]=targets['id']+str(op)+"="+s+"\n"
        self.kill[self.c].append(targets['id'])

    #function for Assignment 
    def Assignment(self,targets,value):
        s=""
        if value['_type']=='Constant':
            s=str(value['value'])
        elif value['_type']=='Call':
            p=""
            if len(value['args'])>0:
                for i in value['args']:
                    if i['_type']=='Name':
                        p+=i['id']
                        self.gen[self.c].append(i['id'])
                    elif i['_type']=='Call':
                        p+=i['func']['id']+'()'
                    elif i['_type']=='Constant':
                        p+=str(i['value'])
                    elif i['_type']=='BinOp':
                        v1,v2=0,0
                        for k in i['left']:
                            if k=='value':
                                v1=1
                            if k=='id':
                                v2=1
                        if v1:
                            p+=str(i['left']['value'])
                        if v2:
                            p+=i['left']['id']
                            self.gen[self.c].append(i['left']['id'])
                        p+=str(obj.operator(i['op']))
                        v1,v2=0,0
                        for k in i['right']:
                            if k=='value':
                                v1=1
                            if k=='id':
                                v2=1
                        if v1:
                            p+=str(i['right']['value'])
                        if v2:
                            p+=i['right']['id']
                            self.gen[self.c].append(i['right']['id'])
                    p+=','
            s=value['func']['id']+'('+p[0:-1]+')'
        elif value['_type']=='Compare':
            w,x=0,0
            for k in value['left']:
                if k=='value':
                    w=1
                if k=='id':
                    x=1
            l=str()
            n,m=0,0
            for i in value['comparators']:
                for j in i:
                    if j=='value':
                        n=1
                    if j=='id':
                        m=1
            if m:
                l=value['comparators'][0]['id']
                self.gen[self.c].append(value['comparators'][0]['id'])
            if n:
                l=value['comparators'][0]['value']
            if w:
                s=str(value['left']['value'])+obj.operation(value['ops'])+str(l)
            if x:
                s=str(value['left']['id'])+obj.operation(value['ops'])+str(l)
                self.gen[self.c].append(value['left']['id'])
            if targets==0:
                return str(s)
            
        elif value['_type']=='BinOp':
            w,x,v,p,t,y=0,0,0,0,0,0
            m=""
            n=""
            for k in value['left']:
                if k=='value':
                    w=1
                if k=='id':
                    x=1
                    self.gen[self.c].append(value['left']['id'])
                if k=='func':
                    y=1
                    self.gen[self.c].append(value['left']['func']['id'])
            if y:
                for i in value['left']['args']:
                    if i['_type']=='Name':
                        m+=i['id']
                        self.gen[self.c].append(i['id'])
                    elif i['_type']=='Call':
                        m+=i['func']['id']+'()'
                    elif i['_type']=='Constant':
                        m+=str(i['value'])
                    elif i['_type']=='BinOp':
                        v1,v2=0,0
                        for k in i['left']:
                            if k=='value':
                                v1=1
                            if k=='id':
                                v2=1
                        if v1:
                            m+=str(i['left']['value'])
                        if v2:
                            m+=i['left']['id']
                            self.gen[self.c].append(i['left']['id'])
                        m+=str(obj.operator(i['op']))
                        v1,v2=0,0
                        for k in i['right']:
                            if k=='value':
                                v1=1
                            if k=='id':
                                v2=1
                        if v1:
                            m+=str(i['right']['value'])
                        if v2:
                            m+=i['right']['id']
                            self.gen[self.c].append(i['right']['id'])
                    m+=','
            for k in value['right']:
                if k=='value':
                    v=1
                if k=='id':
                    p=1
                    self.gen[self.c].append(value['right']['id'])
                if k=='func':
                    t=1
                    self.gen[self.c].append(value['right']['func']['id'])
            
            if t:
                for i in value['right']['args']:
                    if i['_type']=='Name':
                        n+=i['id']
                        self.gen[self.c].append(i['id'])
                    elif i['_type']=='Call':
                        n+=i['func']['id']+'()'
                    elif i['_type']=='Constant':
                        n+=str(i['value'])
                    elif i['_type']=='BinOp':
                        v1,v2=0,0
                        for k in i['left']:
                            if k=='value':
                                v1=1
                            if k=='id':
                                v2=1
                        if v1:
                            n+=str(i['left']['value'])
                        if v2:
                            n+=i['left']['id']
                            self.gen[self.c].append(i['left']['id'])
                        n+=str(obj.operator(i['op']))
                        v1,v2=0,0
                        for k in i['right']:
                            if k=='value':
                                v1=1
                            if k=='id':
                                v2=1
                        if v1:
                            n+=str(i['right']['value'])
                        if v2:
                            n+=i['right']['id']
                            self.gen[self.c].append(i['right']['id'])
                    n+=','
            
            if v and w:
                s=str(value['left']['value'])+obj.operator(value['op'])+str(value['right']['value'])
            if x and v:
                s=str(value['left']['id'])+obj.operator(value['op'])+str(value['right']['value'])
            if p and x:
                s=str(value['left']['id'])+obj.operator(value['op'])+str(value['right']['id'])
            if p and w:
                s=str(value['left']['value'])+obj.operator(value['op'])+str(value['right']['id'])
            if w and t:
                s=str(value['left']['value'])+obj.operator(value['op'])+str(value['right']['func']['id'])+'('+n[0:-1]+')'
            if v and y:
                s=str(value['left']['func']['id'])+'('+m[0:-1]+')'+obj.operator(value['op'])+str(value['right']['id'])
            if x and t:
                s=str(value['left']['id'])+obj.operator(value['op'])+str(value['right']['func']['id'])+'('+n[0:-1]+')'
            if y and t:
                s=str(value['left']['func']['id'])+'('+m[0:-1]+')'+obj.operator(value['op'])+str(value['right']['func']['id'])+'('+n[0:-1]+')'
            if y and p:
                s=str(value['left']['func']['id'])+'('+m[0:-1]+')'+obj.operator(value['op'])+str(value['right']['id'])
                
            
        elif value['_type']=='Name':
            s=value['id']
            self.gen[self.c].append(value['id'])
        if targets==0:
            return str(s)
            
        for target in targets:
            #print("Assignment Statement: "+target['id']+" = "+s)
            if self.c in self.V:
                self.V[self.c]+=target['id']+"="+s+"\n"
            else:
                self.V[self.c]=target['id']+"="+s+"\n"
            self.kill[self.c].append(target['id'])
            
    #function for while loop 
    def whileLoop(self,body,test):
        self.c+=1
        self.edges[self.c-1].append(self.c)  
        l=0
        for i in test:
            if i=='ops':
                l=1
                ops=obj.operation(test['ops'])
        if l:
            s=""
            for comp in test['comparators']:
                if comp['_type']=='Constant':
                    s+=str(comp['value'])
                elif comp['_type']=='Name':
                    s+=comp['id'] 
                    self.gen[self.c].append(comp['id'])
                elif comp['_type']=='Call':
                    p=""
                    if len(comp['args'])>0:
                        for i in comp['args']:
                            if i['_type']=='Name':
                                p+=i['id']
                                self.gen[self.c].append(i['id'])
                            elif i['_type']=='Call':
                                p+=i['func']['id']+'()'
                            elif i['_type']=='Constant':
                                p+=str(i['value'])
                            elif i['_type']=='BinOp':
                                v1,v2=0,0
                                for k in i['left']:
                                    if k=='value':
                                        v1=1
                                    if k=='id':
                                        v2=1
                                if v1:
                                    p+=str(i['left']['value'])
                                if v2:
                                    p+=i['left']['id']
                                    self.gen[self.c].append(i['left']['id'])
                                p+=str(obj.operator(i['op']))
                                v1,v2=0,0
                                for k in i['right']:
                                    if k=='value':
                                        v1=1
                                    if k=='id':
                                        v2=1
                                if v1:
                                    p+=str(i['right']['value'])
                                if v2:
                                    p+=i['right']['id']
                                    self.gen[self.c].append(i['right']['id'])
                            p+=','
                    s+=comp['func']['id']+'('+p[0:-1]+')'
            #print("Branch condition: "+test['left']['id']+ops+s)
            self.V[self.c]='while '+test['left']['id']+ops+s+"\n"
            self.gen[self.c].append(test['left']['id'])
        else:
            self.V[self.c]='branch['+test['id']+']'+"\n"
            self.gen[self.c].append(test['id'])
        p=self.c
        q=self.c
        if len(body)>0:
            self.c+=1
            self.edges[self.c-1].append(self.c)
            self.edges[self.c].append(p)
            g=0
            for i in body:
                if i['_type']=='While':
                    if not g:
                        self.c-=1 
                    else:
                        self.edges[self.c-1].append(self.c) 
                    obj.whileLoop(i['body'],i['test'])
                elif i['_type']=='Assign':
                    g=1
                    obj.Assignment(i['targets'],i['value'])
                elif i['_type']=='AugAssign':
                    g=1
                    s=obj.operator(i['op'])
                    obj.AugAssign(i['target'],s,i['value'])
                elif i['_type']=='If':
                    q=self.c
                    if not g:
                        self.c-=1 
                    else:
                        self.edges[self.c].append(self.c+1) 
                    obj.condition(i['body'],i['orelse'],i['test'])
                    self.edges[self.c].append(p)
                    self.edges[q+2].append(p)
                elif i['_type']=='Expr':
                    obj.exp(i['value'])
                elif i['_type']=='Call':
                    s=""
                    if len(value['args'])>0:
                        for j in value['args']:
                            if i['_type']=='Name':
                                s+=j['id']
                                self.gen[self.c].append(j['id'])
                            elif j['_type']=='Call':
                                s+=j['func']['id']+'()'
                            elif j['_type']=='Constant':
                                s+=str(j['value'])
                            elif j['_type']=='BinOp':
                                v1,v2=0,0
                                for k in j['left']:
                                    if k=='value':
                                        v1=1
                                    if k=='id':
                                        v2=1
                                if v1:
                                    s+=str(i['left']['value'])
                                if v2:
                                    s+=i['left']['id']
                                    self.gen[self.c].append(i['left']['id'])
                                s+=str(obj.operator(i['op']))
                                v1,v2=0,0
                                for k in j['right']:
                                    if k=='value':
                                        v1=1
                                    if k=='id':
                                        v2=1
                                if v1:
                                    s+=str(i['right']['value'])
                                if v2:
                                    s+=i['right']['id']
                                    self.gen[self.c].append(i['right']['id'])
                            s+=','
                        s1=value['func']['id']+'('+s[0:-1]+')'
                    if self.c in self.V:
                        self.V[self.c]+=s1+"\n"
                    else:
                        self.V[self.c]=s1+"\n"
        return p
        
    #function for condition(if else)
    def condition(self,body,orelse,test):
        #print(type(body))
        self.c+=1
        q=self.c
        if self.c==1:
            self.edges[self.c-1].append(self.c)
        l=0
        for i in test:
            if i=='ops':
                l=1
                ops=obj.operation(test['ops'])
        if l:
            s=""
            for comp in test['comparators']:
                if comp['_type']=='Constant':
                    s+=str(comp['value'])
                elif comp['_type']=='Name':
                    s+=comp['id'] 
                    self.gen[self.c].append(comp['id'])
                elif comp['_type']=='Call':
                    p=""
                    if len(comp['args'])>0:
                        for i in comp['args']:
                            if i['_type']=='Name':
                                p+=i['id']
                                self.gen[self.c].append(i['id'])
                            elif i['_type']=='Call':
                                p+=i['func']['id']+'()'
                            elif i['_type']=='Constant':
                                p+=str(i['value'])
                            elif i['_type']=='BinOp':
                                v1,v2=0,0
                                for k in i['left']:
                                    if k=='value':
                                        v1=1
                                    if k=='id':
                                        v2=1
                                if v1:
                                    p+=str(i['left']['value'])
                                if v2:
                                    p+=i['left']['id']
                                    self.gen[self.c].append(i['left']['id'])
                                p+=str(obj.operator(i['op']))
                                v1,v2=0,0
                                for k in i['right']:
                                    if k=='value':
                                        v1=1
                                    if k=='id':
                                        v2=1
                                if v1:
                                    p+=str(i['right']['value'])
                                if v2:
                                    p+=i['right']['id']
                                    self.gen[self.c].append(i['right']['id'])
                            p+=','
                    s+=comp['func']['id']+'('+p[0:-1]+')'
            #print("Branch condition: "+test['left']['id']+ops+s)
            self.V[self.c]='if '+test['left']['id']+ops+s+"\n"
            self.gen[self.c].append(test['left']['id'])
        else:
            self.V[self.c]='branch['+test['id']+']'+"\n"
            self.gen[self.c].append(test['id'])
        p=self.c
        m=0
        n=-1
        if len(body)>0:
            self.c+=1
            self.edges[self.c-1].append(self.c)
            g=0
            for i in body:
                if i['_type']=='If':
                    if not g:
                        self.c-=1
                    else:
                        self.edges[self.c].append(self.c+1)
                    obj.condition(i['body'],i['orelse'],i['test'])
                elif i['_type']=='While':
                    if not g:
                        self.c-=1
                    else:
                        self.edges[self.c].append(self.c+1)
                    obj.whileLoop(i['body'],i['test'])
                    n=self.c-1
                elif i['_type']=='Assign':
                    g=1
                    obj.Assignment(i['targets'],i['value'])
                elif i['_type']=='AugAssign':
                    g=1
                    s=obj.operator(i['op'])
                    obj.AugAssign(i['target'],s,i['value'])
                elif i['_type']=='Expr':
                    obj.exp(i['value'])
        if len(orelse)>0:
            m=1
            self.c+=1
            self.edges[p].append(self.c)
            #if self.c+1 not in self.edges[self.c]:
             #   self.edges[self.c].append(self.c+1)
            f=0
            for j in orelse:
                if j['_type']=='If':
                    if not f:
                        self.c-=1
                    else:
                        print(self.c)
                        self.edges[c].append(self.c+1)
                    obj.condition(j['body'],j['orelse'],j['test'])
                    #print(self.V)
                elif j['_type']=='While':
                    f=1
                    obj.whileLoop(j['body'],j['test'])
                elif j['_type']=='Assign':
                    f=1
                    obj.Assignment(j['targets'],j['value'])
                elif j['_type']=='AugAssign':
                    f=1
                    s=obj.operator(j['op'])
                    obj.AugAssign(j['target'],s,j['value'])
                elif j['_type']=='Expr':
                    obj.exp(j['value'])
        if n!=-1 and self.c+1 not in self.edges[n]:
            self.edges[n].append(self.c+1)
        if not m:
            return q
        else:
            return -1
    
#Main function
if __name__=="__main__":
    import json
    from graphviz import Digraph
    with open('sample.json', 'r') as openfile:
    	ast=json.load(openfile)
    data=ast['body']
    V=dict()
    c=0
    edges=[[] for i in range(30)]
    gen=[[] for i in range(30)]
    kill=[[] for i in range(30)]
    obj=A(V,c,edges,gen,kill)
    f=0
    for i in data:
        if i['_type']=='Assign':
            if f:
                obj.c+=1
                for j in range(obj.c):
                    if len(edges[j])==0:
                        obj.edges[j].append(obj.c)
                f=0
            obj.Assignment(i['targets'],i['value'])
        elif i['_type']=='AugAssign':
            if f:
                obj.c+=1
                for j in range(obj.c):
                    if len(edges[j])==0:
                        obj.edges[j].append(obj.c)
                f=0
            s=obj.operator(i['op'])
            obj.AugAssign(i['target'],s,i['value'])
        elif i['_type']=='While':
            f=0
            k=obj.whileLoop(i['body'],i['test'])
            obj.c+=1
            obj.edges[k].append(obj.c)
            #obj.edges[k].append(obj.c+1)
            #print(k,obj.c)
        elif i['_type']=='Expr':
            if f:
                obj.c+=1
                for j in range(obj.c):
                    if len(edges[j])==0:
                        obj.edges[j].append(obj.c)
                f=0
            obj.exp(i['value'])
        elif i['_type']=='If':
            f=1
            q=obj.condition(i['body'],i['orelse'],i['test'])
            if q!=-1 and obj.c+1 not in obj.edges[q]:
                obj.edges[q].append(obj.c+1)
            
    obj.edges=[list(set(i)) for i in obj.edges]
    
    for i in range(len(obj.gen)):
        p=set(obj.gen[i])
        obj.gen[i]=list(p)
    for i in range(len(obj.kill)):
        p=set(obj.kill[i])
        obj.kill[i]=list(p)
    OUT=[[] for i in range(30)]
    IN=[[] for i in range(30)] 
    change=True
    while(change):
        change=False
        for i in range(obj.c,-1,-1):
            OLDIN=IN[i]
            OLDOUT=OUT[i]
            p=list()
            for j in obj.edges[i]:
                #print(j)
                if len(IN[j])>0:
                    p.extend(IN[j])
            OUT[i]=list(set(p))
            p=list(set(set(OUT[i])-set(kill[i])|set(gen[i])))
            IN[i]=p
            if OLDIN!=IN[i] or OLDOUT!=OUT[i]:
                change=True
    D=dict()
    m=0
    for i in obj.V:
        p=V[i].split("\n")
        loc_gen=set()
        for j in range(len(p)-2,-1,-1):
            res=p[j].find('=')
            if res!=-1:
                q=p[j][0:res]
                if q not in OUT[m] and q not in loc_gen:
                    continue
                else:
                    if m not in D:
                        D[m]=p[j]+"\n"
                    else:
                        D[m]+=p[j]+"\n"
            else:
                if m not in D:
                    D[m]=p[j]+"\n"
                else:
                    D[m]+=p[j]+"\n"
            for k in gen[m]:
                if p[j].find(k)!=-1:
                    loc_gen.add(k)
            if res!=-1 and q in loc_gen:
                loc_gen.remove(q)
        m+=1
    for i in D:
        p=D[i].split("\n")
        p=p[::-1]
        D[i]='\n'.join(p)

    dot = Digraph(comment='CFG')
    m='A'
    for i in D:
        dot.node(m,D[i])   
        m=chr(ord(m)+1)
    m='A'
    #print(obj.c)
    for i in range(len(D)):
        p=set(edges[i])
        edges[i]=list(p)
        for j in range(len(edges[i])):
            dot.edge(m,chr(edges[i][j]+65))
        m=chr(ord(m)+1)
    dot.render('output', view=True)
  
    
