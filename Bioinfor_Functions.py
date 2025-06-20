def RevComp(string):
    
    revcomp = []
    for i in range(len(string)):
        if string[len(string) - 1 - i] == 'A':
            revcomp.append('T')
        elif string[len(string) - 1 - i] == 'T':
            revcomp.append('A')
        elif string[len(string) - 1 - i] == 'G':
            revcomp.append('C')
        else:
            revcomp.append('G')
            
    revcomp = ''.join(list(revcomp))   
    return revcomp
#--------------------------------------------------
def Hamming(s1,s2):
    count = 0
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            count = count + 1
    return count

def HamCount(string, pat, k):
    count = 0
    for i in range(len(string) - len(pat) + 1):
        if Hamming(string[i : i + len(pat)], pat) <= k:
            count = count + 1

    return count
#----------------------------------------------------------------------------- 

def SymToNum(sym):
    if sym == 'A':
        return 0
    if sym == 'C':
        return 1
    if sym == 'G':
        return 2
    else:
        return 3

def NumToSym(num):
    
    if num == 0:
        return 'A'
    if num == 1:
        return 'C'
    if num == 2:
        return 'G'
    else:
        return 'T'

def PatToNum(pat):

    if len(pat) == 0:
        return 0
    
    sym = pat[len(pat) - 1]
    pat = pat[0 : len(pat) - 1]

    return 4*PatToNum(pat) + SymToNum(sym)
    
def NumToPat(index, k):
    import math as mt
    
    if k == 1:
        return NumToSym(index)
        
    PreInd = int(mt.floor(index/4))
    Remain = int(mt.fmod(index,4))
    
    PrePat = NumToPat(PreInd, k - 1)
    sym = NumToSym(Remain)
    
    return PrePat + sym    
    
       
#------------------------------------------------------------------------------    
def CompFreq(text, k):
    
    FreqArr = [ 0 for i in range(4**k)]
    
    for i in range(len(text) - k + 1):
        pat = text[i : i + k]
        j = PatToNum(pat)
        FreqArr[j] = FreqArr[j] + 1
        
    return FreqArr
        
    
def FreqWord(text, k):
    FreqPat = []
    FreqArr = CompFreq(text, k)
    maxcount = max(FreqArr)
    
    for i in range(4**k):
        if FreqArr[i] == maxcount:
            FreqPat.append(NumToPat(i, k))
    
    return FreqPat
   
#---------------------------------------------------------------------------   
def Neighbor1(s):
    delta = ['A','G','T','C']

    neigh = []
    for i in range(len(s)):
        neigh.append(s)
        for j in range(len(s)):
            sym = s[j]
            for N in delta:
                if N != sym:
                    dum = list(s)
                    dum[j] = N
                    dum = ''.join(dum)
                    neigh.append(dum)
        
    neigh = list(set(neigh))
    return neigh 

def Neighbors(pat, d):
    
    delta = ['A','C', 'G', 'T']    
    
    if d == 0:
        return pat
    if d == 1:
        return Neighbor1(pat)
    if len(pat) == 1:
        return delta
        
    NHood = []
    SufPat = pat[1 : len(pat)]
    SufNHood = Neighbors(SufPat, d)
    
    for string in SufNHood:
        if Hamming(SufPat, string) < d:
            for N in delta:
                NHood.append(N + string)
            else:
                NHood.append(pat[0] + string)
                
    NHood = list(set(NHood))
    return NHood
                
#---------------------------------------------------------------------------------

def FreqPatMisMat(text, k, d):
    
    FreqPat = []
    Close = [0 for i in range(4**k)]
    FreqArr = [0 for i in range(4**k)]
    
    for i in range(len(text) - k + 1):
        neigh = Neighbors(text[i : i + k], d)
        for pat in neigh:
            j = PatToNum(pat)
            Close[j] = 1
            
    for i in range(4**k):
        if Close[i] == 1:
            pattern = NumToPat(i, k)
            FreqArr[i] = HamCount(text, pattern, d)
            
    M = max(FreqArr)
    
    for i in range(4**k):
        if FreqArr[i] == M:
            string = NumToPat(i, k)
            FreqPat.append(string)
        
    return FreqPat
    

def FreqWordSort(text,k,d):
    FreqPat = []
    Neigh = list()
    
    for i in range(len(text) - k + 1):
        Neigh.append(Neighbors(text[i : i + k], d))
        
    NeighArr = []
    for i in range(len(Neigh)):
        for pat in Neigh[i]:
            NeighArr.append(pat)
    
    indices = []
    count = []
    for i in range(len(NeighArr)):
        pat = NeighArr[i]
        indices.append(PatToNum(pat))
        count.append(1)
    
    SortInd = sorted(indices)
    
    for i in range(len(NeighArr) - 1):
        if SortInd[i] == SortInd[i + 1]:
            count[i + 1] = count[i] + 1
            
    M = max(count)
    
    for i in range(len(NeighArr)):
        if count[i] == M:
            pat = NumToPat(SortInd[i], k)
            FreqPat.append(pat)
            
    return FreqPat
        
        
def FreqPatRevComp(text, k, d):
    
    FreqPat = []
    Close = [0 for i in range(4**k)]
    FreqArr = [0 for i in range(4**k)]
    
    for i in range(len(text) - k + 1):
        neigh = Neighbors(text[i : i + k], d)
        for pat in neigh:
            j = PatToNum(pat)
            Close[j] = 1
            
    for i in range(4**k):
        if Close[i] == 1:
            pattern = NumToPat(i, k)
            FreqArr[i] = HamCount(text, pattern, d) + HamCount(text,RevComp(pattern), d)
            
    M = max(FreqArr)
    
    for i in range(4**k):
        if FreqArr[i] == M:
            string = NumToPat(i, k)
            FreqPat.append(string)
        
    return FreqPat     

#--------------------------------------------------------------------------

def ClumpFind(text, k, L, t):

    Clump =[0 for i in range(4**k)]
    FreqPat = []
    
    for i in range(len(text) - L + 1):
        pat = text[i : i + L]
        FreqArr = CompFreq(pat, k)
        for j in range(4**k):
            if FreqArr[j] >= t:
                Clump[j] = 1
                
    for i in range(4**k):
        if Clump[i] == 1:
            pattern = NumToPat(i, k)
            FreqPat.append(pattern)
            
    return FreqPat
    
def BetterClumpFind(text, k, L, t):
    
    Clump = [0 for i in range(4**k)]
    FreqPat = []    
    
    FreqArr = CompFreq(text, k)
    for i in range(4**k):
        if FreqArr[i] >= t:
            Clump[i] = 1
        
    for i in range(1, len(text) - L):
        pat1 = text[i - 1 : i - 1 + k]
        j = PatToNum(pat1)
        FreqArr[j] = FreqArr[j] - 1
        if FreqArr[j] < t:
            Clump[j] = 0
        pat2 = text[i + L - k: i + L]
        j = PatToNum(pat2)
        FreqArr[j] = FreqArr[j] + 1
        if FreqArr[j] >= t:
            Clump[j] = 1
            
        for i in range(4**k):
            if Clump[i] == 1:
                pattern = NumToPat(i, k)
                FreqPat.append(pattern)
        
        return FreqPat
            