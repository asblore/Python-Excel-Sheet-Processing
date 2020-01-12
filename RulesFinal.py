import pandas as pd
import warnings

def getvcv(rule):
    """
    getvcv() takes a rule of the form {var1 cond1(val1){var2 cond2(val2)}{var3 cond3(val3)}...}
    and returns a list of strings ['var1 cond1(val1)','var2 cond2(val2)','var3 cond3(val3)'...]
    """
    stack=[]
    lst=[]
    i=0
    l=len(rule)
    while i<l:
        if rule[i]=='{':
            i+=1
            s=''
            while True:
                if rule[i]=='{' and len(stack)!=0:   #'{' lies inside ()
                    s+=rule[i]
                    i+=1
                elif rule[i]=='}' and len(stack)!=0: #'}' lies inside ()
                    s+=rule[i]
                    i+=1
                elif rule[i]=='{' and len(stack)==0: #'{' lies outside ()
                    break
                elif rule[i]=='}' and len(stack)==0: #'}' lies outside ()
                    break
                if rule[i]=='(':
                    stack.append(rule[i])
                if rule[i]==')':
                    stack.pop()
                s+=rule[i]
                i+=1
            lst+=[s]
        else:
            i+=1
    return lst

def extract(s):
    """
    extract() takes a string s of the form var cond(val)
    and returns a tuple (var,cond,val)
    """
    s=s.split()   #s=[var,cond(val)]
    var=s[0]
    cond=''
    val=''        #cond and val need to be extracted from s[1]=cond(val)

    i=0
    l=len(s[1])

    while s[1][i]!='(':
        cond+=s[1][i]
        i+=1

    i+=1

    while i<l-1:
        val+=s[1][i]
        i+=1
        
    return (var,cond,val)

def convert1(s): 
    '''
    convert1() takes a string s of the form val1,val2,val3...,valn and
    returns a list [val1,val2,val3...,valn]
    '''
    i=0
    l=len(s)
    stack=[]
    lst=[]
    s1=''
    while i<l:
        if s[i]=='(' or s[i]=='[' or s[i]=='{':
            stack.append(s[i])
            s1+=s[i]
            i+=1
        elif s[i]==')' or s[i]==']' or s[i]=='}':
            stack.pop()
            s1+=s[i]
            i+=1
        elif s[i]==',':
            if len(stack)==0:
                lst+=[s1]
                s1=''
                i+=1
            else:
                s1+=s[i]
                i+=1
        else:
            s1+=s[i]
            i+=1
    if s1!='':
        lst+=[s1]
    return lst

def convert2(s):
    '''
    convert2() takes a string s of the form key1:val1,key2:val2,...keyn:valn and
    returns a list [key1,val1,key2...,valn]
    '''
    i=0
    l=len(s)
    stack=[]
    lst=[]
    s1=''
    while i<l:
        if s[i]=='(' or s[i]=='[' or s[i]=='{':
            stack.append(s[i])
            s1+=s[i]
            i+=1
        elif s[i]==')' or s[i]==']' or s[i]=='}':
            stack.pop()
            s1+=s[i]
            i+=1
        elif s[i]==',':
            if len(stack)==0:
                lst+=[s1]
                s1=''
                i+=1
            else:
                s1+=s[i]
                i+=1
        elif s[i]==':':
            if len(stack)==0:
                lst+=[s1]
                s1=''
                i+=1
            else:
                s1+=s[i]
                i+=1
        else:
            s1+=s[i]
            i+=1
    if s1!='':
        lst+=[s1]
    return lst

def type_listuple(s):
    '''
    type_listuple() takes a string s of the form val1,val2...,valn
    and prints the type of val1,val2...,valn
    '''
    if s=='':
        return s
    lst=convert1(s)
    s=''
    for v in lst:
        s+=find_type(v)
    return s

def type_dict(s):
    '''
    type_dict() takes a string s of the form key1:val1,key2:val2...,keyn:valn
    and prints the type of key1,val1...,keyn,valn
    '''
    if s=='':
        return s
    lst=convert2(s)
    s=''
    for v in lst:
        s+=find_type(v)
    return s

def find_type(val):
    '''
    find_type() takes a string s and prints its type  
    type can be integer,floating point,string,list,tuple or dictionary
    '''
    if val.isdigit():
        return 'integer '
    elif val.find('.')!=-1:
        p=val.find('.')
        if val[:p].isdigit() and val[p+1:].isdigit():
            return 'float '
        else:
            return 'string '
    elif val[0]=='[' and val[len(val)-1]==']':
        return 'list '+type_listuple(val[1:len(val)-1])
    elif val[0]=='(' and val[len(val)-1]==')':
        return 'tuple '+type_listuple(val[1:len(val)-1])
    elif val[0]=='{' and val[len(val)-1]=='}':
        return 'dictionary '+type_dict(val[1:len(val)-1])
    else:
        return 'string '

def checkValidity(rule,lst):
    '''
    checkValidity() takes a rule in the form of a string rule="{var1:val1,var2:val2...}"
    and tests its validity using the standard rule which is a list lst=[(var1,cond1,val1)...]
    drule is a dictionary of the form {var1:val1,var2:val2,...} built using rule
    dlst is a dictionary of the form {var1:[cond1,val1],var2:[cond2,val2]...} built using lst
    '''
    drule={}                   
    l=convert2(rule[1:len(rule)-1])
    i=0
    while i<len(l)-1:
        drule[l[i]]=l[i+1]
        i+=2

    if len(drule.keys())!=len(lst):
        return -1
    else:
        dlst={}
        for v in lst:
            dlst[v[0]]=[v[1],v[2]]
    
        for k in drule.keys():
            if k not in dlst.keys():
                return 0
            cond=dlst[k][0]
            val=dlst[k][1]
            test_val=drule[k]
            if cond=='is':
                if test_val!=val:
                    return 0
            elif cond=='from_to' or cond=='not_from_to':
                t=find_type(test_val)
                if t!='integer ' and t!='float ':
                    return 0
                l=val[1:len(val)-1].split(',')
                a=float(l[0])
                b=float(l[1])
                num=float(test_val)
                r=num<a or num>b
                if r==1 and cond=='from_to':
                    return 0
                if r==0 and cond=='not_from_to':
                    return 0
            elif cond=='between' or cond=='not_between':
                t=find_type(test_val)
                if t!='integer ' and t!='float ':
                    return 0
                l=val[1:len(val)-1].split(',')
                a=float(l[0])
                b=float(l[1])
                num=float(test_val)
                r=num<=a or num>=b
                if r==1 and cond=='between':
                    return 0
                if r==0 and cond=='not_between':
                    return 0
            elif cond=='greater_equal' or cond=='less':
                t=find_type(test_val)
                if t!='integer ' and t!='float ':
                    return 0
                r=float(test_val)<float(val)
                if r==1 and cond=='greater_equal':
                    return 0
                if r==0 and cond=='less':
                    return 0
            elif cond=='less_equal' or cond=='greater':
                t=find_type(test_val)
                if t!='integer ' and t!='float ':
                    return 0
                r=float(test_val)>float(val)
                if r==1 and cond=='less_equal':
                    return 0
                if r==0 and cond=='greater':
                    return 0
            elif cond=='among' or cond=='not_among':
                l=convert1(val[1:len(val)-1])
                r=test_val not in l
                if r==1 and cond=='among':
                    return 0
                if r==0 and cond=='not_among':
                    return 0
        return 1

def inputrule(res):
    '''
    Manually input rule values for testing validity
    '''
    rname=input("Enter rule name:")
    rule=input("Enter rule (like a dictionary):")
    if rname not in res.keys():
        print("Rule name not found")
    else:
        lst=res[rname]
        ret=checkValidity(rule,lst)
        if ret==1:
            print("Rule is valid")
        elif ret==0:
            print("Rule is invalid")
        else:
            print("Rule not applicable")

def inputrule2(res):
    '''
    Rules to be tested for validity are read from file
    and results written into file
    '''
    df1=pd.read_excel("C:\\Users\\Abhishek\\Documents\\IISc Internship\\Rules\\rules1.xlsx",sheet_name='Sheet2')
    l1=[]
    l2=[]
    l3=[]
    for i in df1.index:
        rname=df1['Rule Name'][i]
        rule=df1['Check'][i]
        l1+=[rname]
        l2+=[rule]
        if rname not in res.keys():
            l3+=["Rule name not found"]
        else:
            lst=res[rname]
            ret=checkValidity(rule,lst)
            if ret==1:
                l3+=["Valid"]
            elif ret==0:
                l3+=["Not valid"]
            else:
                l3+=["Not applicable"]
    df2=pd.DataFrame({'Rule Name':l1,'Check':l2,'Validity':l3})
    df2=df2.set_index('Rule Name')
    writer = pd.ExcelWriter("C:\\Users\\Abhishek\\Documents\\IISc Internship\\Rules\\rules2.xlsx", engine='xlsxwriter')  
    df2.to_excel(writer,'Sheet1')
    writer.save()
    
def display_rules(res):
    for t in sorted(res.keys()):
        print(t)
        for v in res[t]:
            print(v[0],v[1],v[2],"\ttype of "+v[0]+" is "+find_type(v[2]).split()[0])
        print()

def display_types(res):
    for t in res.values():
        for v in t:
            print(v[2])
            print(find_type(v[2]))
            print()

def get_res(df):
    res={}
    for i in df.index:
       rule_name=df['Rule Name'][i]
       rule=df['Rule'][i]
       lst=getvcv(rule)                 #lst is a list of strings of the form 'var cond(val)'
       vcv=[]                           #vcv is a list of tuples of the form (var,cond,val)
       for s in lst:
           vcv+=[extract(s)]
       res[rule_name]=vcv
    return res
        
def main():
    '''
    res is a dictionary of the form {rule_name:vcv}
    vcv is a list of tuples of the form (var,cond,val)
    Thus res associates a rule_name with list of possible variables,conditions and values
    '''
    df=pd.read_excel("C:\\Users\\Abhishek\\Documents\\IISc Internship\\Rules\\rules1.xlsx",sheet_name='Sheet1')
    res=get_res(df)
    print(res)
    #display_rules(res)
    #display_types(res)
    #inputrule2(res)
    #inputrule(res)
main()
