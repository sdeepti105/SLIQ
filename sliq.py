#!/usr/bin/env python
# coding: utf-8

# In[5]:


import math
infi=math.inf
import pydot
import pandas as pd
path='book.xlsx'
#header=list(pd.read_excel(path))
header=[ 'Humidity','Temperature','Pressure','Wind Speed','Dew Point','Class']
label_frame=pd.read_excel(path,usecols=[len(header)-1])
label_list=label_frame.values.tolist()
final_node=label_frame.values.tolist()
def unique(list):
    return set(list)
def class_count(list):
    count={}
    for i in range(len(list)):
        pivot=list[i][0]
        if pivot not in count:
            count[pivot]=0
        count[pivot]+=1
    return count
def partition(list,val):
    length=len(list)
    L=[]
    R=[]
    i=0
    while i<length:
        if list[i][1]<val:
            L.append(list[i][0])
            i=i+1
        else:
            R.append(list[i][0])
            i=i+1
    return L,R
def ginni(list):
    length=len(list)
    out=[]
    for i in range(length):
        out.append(label_list[list[i]])
    counts=class_count(out)
    impurity=1
    for label in counts:
        prob=counts[label]/length
        impurity=impurity-(prob**2)
    return impurity

def best_split(list):
    gmin=1
    length=len(list)
    val=0
    for i in range(length-1):
        UP=[]
        DO=[]
        for j in range(length-1):
            if j<=i:
                UP.append(list[j][0])
            else:
                DO.append(list[j][0])
        gini_up=ginni(UP)
        gini_down=ginni(DO)
        #print("UP")
        #print(UP)
        #print("Dpwn")
        #print(DO)
        result=(len(UP)/len(list))*gini_up+(len(DO)/len(list))*gini_down
        if result<=gmin:
            gmin=result
            val=(list[i][1]+list[i+1][1])/2
    return val

def getvalue(index,value):
    result=[[] for k in range(len(index))]
    for i in range(len(index)):
        result[i]=[index[i],value.iloc[index[i],0]]
    result=sorted(result,key=lambda x:x[1])
    return result
    
def label(list,key):
    length=len(list)
    for i in range(length):
        final_node[list[i]]=key
split=[infi]*(2**(len(header))-1)

def splitting(path,header,list,c,k): #no of attribute, k lebel of node
    if c<len(header)-1:
        #print("klkl")
        col=pd.read_excel(path,usecols=[c])
        list_1=getvalue(list,col)
        #print(list_1)
        left,right=partition(list_1,best_split(list_1))
        split[k-1]=best_split(list_1)
        label(left,2*k)
        label(right,2*k+1)
        if ginni(left)>0:
            splitting(path,header,left,c+1,2*k)
        if ginni(right)>0:
            splitting(path,header,right,c+1,2*k+1)
    return
          
class node:
    def __init__(self,val,index,x=None):
        self.v=val
        self.i=index
        self.l=x
def makelist(list):
    nodes=[]
    count=0
    j=0
    for i in range(math.floor(len(list)/2)):
        N=node(list[i],i+1,header[count])
        nodes.append(N)
        if j<=i:
            count=count+1
            j=2**(count+1)
    for i in range(math.floor(len(list)/2),len(list)):
        N=node(list[i],i+1)
        nodes.append(N)
    return nodes
def label_nodes(A,list):
    u=unique(A)
    result=[]
    for i in range(len(u)):
        ar=[]
        m=0
        counts={}
        leaf=u.pop()
        j=[index for index,value in enumerate(A) if value==leaf]
        for k in range(len(j)):
            ar.append(label_list[j[k]])
        counts=class_count(ar)
        for key in counts:
            if m<=counts[key]:
                m==counts[key]
                c=key
        result.append([leaf,c])
    for  i in range(len(result)):
        p=result[i][0]
        list[p-1].l=result[i][1]
    return result
def Savegraph(list): #list of nodes
    graph = pydot.Dot(graph_type='graph')
    for i in range(math.floor(len(list)/2)):
        if list[i].v!=infi:
            if list[2*i+1].l!=None:
                if list[2*i+1].v!=infi:
                    edge = pydot.Edge(str(list[i].i)+"--->"+str(list[i].l)+"--->"+str(list[i].v),str(list[2*i+1].i)+"--->"+str(list[2*i+1].l)+"--->"+str(list[2*i+1].v))
                    graph.add_edge(edge)
                else:
                    edge = pydot.Edge(str(list[i].i)+"--->"+str(list[i].l)+"--->"+str(list[i].v),str(list[2*i+1].i)+"--->"+str(list[2*i+1].l))
                    graph.add_edge(edge)
            if list[2*i+2].l!=None: 
                if list[2*i+2].v!=infi:
                    edge = pydot.Edge(str(list[i].i)+"--->"+str(list[i].l)+"--->"+str(list[i].v),str(list[2*i+2].i)+"--->"+str(list[2*i+2].l)+"--->"+str(list[2*i+2].v))
                    graph.add_edge(edge)
                else:
                    edge = pydot.Edge(str(list[i].i)+"--->"+str(list[i].l)+"--->"+str(list[i].v),str(list[2*i+2].i)+"--->"+str(list[2*i+2].l))
                    graph.add_edge(edge)
        graph.write_png('sliq.png')

