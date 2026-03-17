import hashlib, random, math
import numpy as np
 
class CountMinSketch:
    def __init__(self, w=1000, d=5):
        self.w=w; self.d=d
        self.table=np.zeros((d,w),dtype=np.int64)
        self.hash_fns=[(random.randint(1,2**31),random.randint(0,2**31)) for _ in range(d)]
 
    def _hash(self, item, i):
        a,b=self.hash_fns[i]
   return (a*hash(item)+b) % self.w
 
    def update(self, item, count=1):
        for i in range(self.d): self.table[i][self._hash(item,i)]+=count
 
    def query(self, item):
        return min(self.table[i][self._hash(item,i)] for i in range(self.d))
 
class MorrisCounter:
    def __init__(self): self.x=0
    def increment(self):
        if random.random() < 1/(2**self.x): self.x+=1
    def estimate(self): return 2**self.x - 1
 
class FlajoletMartin:
    def __init__(self, n_hash=10): self.n=n_hash; self.max_zeros=[0]*n_hash
    def _trailing_zeros(self,v):
        if v==0: return 32
        return len(bin(v))-len(bin(v).rstrip('0'))
    def add(self, item):
        for i in range(self.n):
            h=hash((item,i))&0xFFFFFFFF
            self.max_zeros[i]=max(self.max_zeros[i],self._trailing_zeros(h))
    def estimate(self): return 2**np.median(self.max_zeros)
 
cms=CountMinSketch()
stream=['apple','banana','apple','cherry','apple','banana']*1000
for w in stream: cms.update(w)
print(f"CountMin 'apple'  estimate: {cms.query('apple')}  (true: {stream.count('apple')})")
print(f"CountMin 'banana' estimate: {cms.query('banana')} (true: {stream.count('banana')})")
