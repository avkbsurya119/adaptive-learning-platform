import random

class RecommadationHeap:
    def __init__(self,maxSize=20):
        self.a=[None]*maxSize
        self.n=0
        self.a[0]=99999
    def insert(self,resource):
        self.n+=1
        self.a[self.n]=resource
        self.restore_up(self.n)
    def restore_up(self,i):
        k=self.a[i]
        iparent=i//2
        while iparent>=1 and self.a[iparent][1]>k[1]:
            self.a[i]=self.a[iparent]
            i=iparent
            iparent=i//2
        self.a[i]=k
    def delete_root(self):
        if self.n==0:
            raise Exception("Heap is empty")
        minValue=self.a[1]
        self.a[1]=self.a[self.n]
        self.n-=1
        self.restore_down(1)
        return minValue
    def restore_down(self,i):
        k=self.a[i]
        lchild=2*i
        rchild=lchild+1
        while rchild<=self.n:
            if k[1]<=self.a[lchild][1] and k[1]<=self.a[rchild][1]:
                self.a[i]=k
                return
            elif self.a[lchild][1]<self.a[rchild][1]:
                self.a[i]=self.a[lchild]
                i=lchild
            else:
                self.a[i]=self.a[rchild]
                i=rchild
            lchild=2*i
            rchild=lchild+1    
        if lchild==self.n and k[1]>self.a[lchild][1]:
            self.a[i]=self.a[lchild]
            i=lchild
        self.a[i]=k
    def display(self):
        if self.n==0:
            print("Heap is empty") 
            return
        print("Heap size =",self.n)
        for i in range(1,self.n+1):
            print(self.a[i],end=' ')
        print()
    def insert_recommendation(self, module, progress, recommendation_threshold):
        # Recommend based on progress against a random threshold
        if progress < recommendation_threshold:
            self.insert((module, progress))
        else:
            # Add more sequences as recommendations to progress further
            self.insert((module, progress + random.randint(1, 5)))