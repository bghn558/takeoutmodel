import numpy as np
import matplotlib
import random
import matplotlib.pyplot as plt

def distance(x,y):
    return np.sqrt(np.sum(np.square(x-y)))
class Graph:
    def factorial(n):
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
    def __init__(self,m):
        self.m=m                      #图中的商店群个数
        self.v={}                    #边的长度信息
        self.e=Graph.factorial(m)/Graph.factorial(m-2)/2
        self.M=[]                #m的位置信息
        self.d=40               #最大距离
        self.l=5                #最小间距
        self.t=6                   #时间段数
        self.S=[]                 #送餐员开始数量分布
        self.R=[]                 #每次的收益
        self.TQ={}         #订单信息集合
        self.TC={}           #订单始终点集合
        self.TR={}          #订单收益集合
        self.TS=[]             #每一期分布
    def vertex_generator(self):                     #d为范围最大值 l 为最小值
        M=[]
        i=1
        V={}
        while i<self.m:
           a=np.array([np.random.rand()*self.d,np.random.rand()*self.d])
           M.append(a)
           for j in range(len(M)-1):
               if distance(M[len(M)-1],M[j])>self.d or distance(M[len(M)-1],M[j])<self.l:
                   M.pop()
           i=len(M)
        self.M=M
        for j in range(len(M)):
            V[j+1]=M[j]
        self.v=V
        return M

    def edge_lenth(self):       #边的长度
        M=self.M
        l=len(M)
        lenth={}
        for i in range(l):
            for j in range(i+1,l):
                d=distance(M[i],M[j])
                lenth[i+1, j+1] = d
        self.v=lenth
        return lenth
    def show(self):   #max为地图最大尺度
        plt.xlim((0,self.d))
        plt.ylim((0,self.d))
        l = len(self.M)
        x = []
        y = []
        for i in range(l):
            xi = np.array(self.M[i])[0]
            x.append(xi)
            yi = np.array(self.M[i])[1]
            y.append(yi)
        plt.scatter(x,y,color='r',s=80)
        for i in range(l):
            xii = [1, 2]
            yii = [1, 2]
            xii[0] = x[i]
            yii[0] = y[i]
            for j in range(i + 1, l):
                xii[1] = x[j]
                yii[1] = y[j]
                plt.plot(xii, yii, color='y')
        plt.show()
    def get_vertexcouple(self):
        L1 = []
        L3 = []
        L = []
        for i in range(1, self.m + 1):
            L1.append(i)
        L4 = L1.copy()

        for j in range(1, self.m + 1):
            L1.remove(j)
            L2 = random.sample(L1, np.random.randint(1,self.m - 1))           #需求随机
            for k in range(len(L2)):
                b = L2[k]
                L3.append(j)
                L3.append(b)
                L.append(L3)
                L3 = []
            L1 = L4.copy()
            #  print(L1)
            #  print(L2)
        #print(L)
        return L
    def request(self):  #模拟订单  t为时间数
        TQ={}
        TC={}
        TR={}
        for t in range(self.t):
            Q = []
            q = []
            D=[]
            a = self.get_vertexcouple()
            for i in range(len(a)):
                b = a[i]
                if b[0] < b[1]:
                    c = (b[0], b[1])
                else:
                    c = (b[1], b[0])
                e = self.v[c]
                d = self.d / e + np.random.randint(1, 10)/self.l
                q.append(b)  # 添加起点终点
                q.append(e)
                q.append(d)
                D.append(d)
                Q.append(q)
                q = []
            TQ[str(t)]=Q
            TC[t]=a
            TR[t]=D
        self.TQ=TQ
        self.TC=TC
        self.TR=TR
        return TQ
    def validrequest(self):             #产生有效的需求
        TQ=self.TQ.copy()
        TS=[]                                    #每一期的状态分布
        ZS=self.S.copy()
        TS.append(self.S)
        TVQ={}
        OR = []
        for i in range(self.t):
            Q=TQ[str(i)]             #第i期的订单集合
            VQ={}               #一期的每一个地点的进出集合
            TR=[]             #每个地区的收益
            L=[]             #每一期的有效订单位置信息以起点顺序
            for j in range(1,self.m+1):           #每个餐厅群
                S = []
                NNS=[]
                for k in range(len(Q)):
                    if Q[k][0][0]==j:
                        S.append(Q[k])             #S为起始点相同的需求
                NS=sorted(S,key=lambda x:x[2])      #NS为按照收益排序的起始点相同的需求
                for n in NS:
                    NNS.append(n[2])
                if ZS[j-1] < len(S):
                    for p in range(len(S) - ZS[j - 1]):
                        NNS[p] *= -1
                    del NS[0:len(S)-ZS[j-1]]                #NS更新为删除未能满足人数要求的订单的有效需求
                VQ[j]=NS
                R = []
                for l in range(len(NNS)):
                    R.append(NNS[l])                        #每期每个地点每个订单收益减去不能完成的损失
                for q in range(len(NS)):
                    L.append(NS[q][0])
                TR.append(sum(R))                           #每期每个地点的收益
            SR=sum(TR)                                   #一期的总收益
            OR.append(SR)
            NL = sorted(L, key=lambda x: x[1])          #以终点排序的订单位置信息
            SD={}              #每个点进出信息集合
            for n in range(1,self.m+1):
                ns = 0                 #起点为n的数目，需要减去
                nd=0                 #终点为n的数目，需要加上
                for m in range(len(L)):
                    if L[m][0]==n:
                        ns-=1
                    if L[m][1]==n:
                        nd+=1
                sd=[ns,nd]              #每个点的进出数
                SD[n]=sd
                ZS[n-1]=ZS[n-1]+ns+nd
            S=ZS.copy()                    #一定要复制，因为sel.S一直储存在同一个内存中防止更新之前的值
            TS.append(S)
            TVQ[i]=VQ
        self.TS=TS
        self.R=sum(OR)
       # print(self.R)
        return TVQ

    def get_revenue(self):
        return self.R-sum(self.S)*self.t
       # print(self.R)
'''''
import json
G=Graph(10)
G.vertex_generator()
G.edge_lenth()
G.request()
dis=[]
for n in G.M:
    a=list(n)
    dis.append(a)
geo=[]
for key in G.v:
    sub = []
    sub.append(list(key))
    sub.append(G.v[key])
    geo.append(sub)
data=[dis, geo, G.TQ]
with open('data','w') as file:
    json.dump(data,file)
'''''
#G=Graph(10)
#G.S=[5,5,5,5,5,5,5,5,5,5]
#G.vertex_generator()
#G.edge_lenth()
#G.request()
#print(G.TQ)
#G.validrequest()


#print(G.request())
#print(G.validrequest())
#G.validrequest()
#print(G.get_revenue())
#print(G.validrequest())
#print(G.get_revenue())
#G.S=[6,6,6,6,6,6,6,6,6,6]
#.validrequest()
#print(G.get_revenue())
























