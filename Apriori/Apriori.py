



class Apriori(object):
    def __init__(self,itemSet,minSupport):
        self.minsupport = minSupport
        self.itemSet = itemSet
        self.candidate = {}

    # 首先要对输入的set里的每一个元素有序化,以便进行后续的连接
    def _setOrder(self):
        message = []
        for item in self.itemSet:
            item.sort()
            message.append(item)
        self.itemSet = message
    # 确定候选一项集
    def _candidate_1(self):
        for item in self.itemSet:
          for element in item:
              self.candidate[element]=0
        for item in self.itemSet:
          for element in item:
              self.candidate[element] = self.candidate[element]+1


    #剪枝函数
    def _cut(self):
        for element in list(self.candidate):
            if self.candidate[element] < self.minsupport:
                del self.candidate[element]


    # 将筛选后的k-1项集合
    # 将一个list作为一个key
    # 比对每一个key内的元素,前k-1位都相同的进行叠加.
    def _candidate_k(self):
        newcandidateList = {}
        newcandidateSet = []
        candidateSet = list(self.candidate.keys())#key的list集合
        candidateSet.sort()
        for i in range(len(candidateSet)):
            for j in range(i+1,len(candidateSet)):
                # 比较candidateSet[i]和candidateSet[j]的内k-1个值的大小
                if list(candidateSet[i])[:-1] == list(candidateSet[j])[:-1]:
                    newcandidate=list(candidateSet[i])
                    newcandidate.extend(list(candidateSet[j])[-1])
                    newcandidateSet.append(newcandidate)

        if newcandidateSet:
            for candidate in newcandidateSet:
                for item in self.itemSet:
                    keynum = 0
                    for candidatee in candidate:
                        if candidatee in item:
                            keynum = keynum+1
                    if keynum == len(candidate):
                        m = ''.join(candidate)
                        newcandidateList[m] = 0
            for candidate in newcandidateSet:
                for item in self.itemSet:
                    keynum = 0
                    for candidatee in candidate:
                        if candidatee in item:
                            keynum = keynum+1
                    if keynum == len(candidate):
                        m = ''.join(candidate)
                        newcandidateList[m] = newcandidateList[m]+1
            self.candidate = newcandidateList

    def getFinalCandidate(self):
        self._setOrder()
        self._candidate_1()
        self._cut()
        candidate = self.candidate
        self._candidate_k()
        while candidate != self.candidate:
            candidate = self.candidate
            self._cut()
            self._candidate_k()
        return  candidate



Alist = [['1','3','4'],['2','3','5'],['1','2','3','5'],['2','5']]
A = Apriori(Alist,3)
print(A.getFinalCandidate())
