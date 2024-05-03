
from collections import defaultdict
import matplotlib.pyplot as plt
import csv


class Apriori(object):
    def __init__(self, minSupp, minConf):
        """ Parameters setting
        """
        self.minSupp = minSupp  # min support (used for mining frequent sets)
        self.minConf = minConf  # min confidence (used for mining association rules)
        self.itemCountDict = defaultdict(int)  # Initialize itemCountDict here
        self.transLength = 0

    def fit(self, filePath):
        """ Run the apriori algorithm, return the frequent *-term sets. 
        """
        # Initialize some variables to hold the tmp result
        transListSet  = self.getTransListSet(filePath)   # get transactions (list that contain sets)
        itemSet       = self.getOneItemSet(transListSet) # get 1-item set
        itemCountDict = defaultdict(int)         # key=candiate k-item(k=1/2/...), value=count
        freqSet       = dict()                   # a dict store all frequent *-items set
        
        self.transLength = len(transListSet)     # number of transactions
        self.itemSet     = itemSet
        
        """ Run the apriori algorithm, return the frequent *-term sets. 
        """
        ...
        mostFreqItem = self.getMostFrequentItem(transListSet)
        # Get the frequent 1-term set
        freqOneTermSet = self.getItemsWithMinSupp(transListSet, itemSet, 
                                             itemCountDict, self.minSupp)

        # Main loop
        k = 1
        currFreqTermSet = freqOneTermSet
        while currFreqTermSet != set():
            freqSet[k] = currFreqTermSet  # save the result
            k += 1
            currCandiItemSet = self.getJoinedItemSet(currFreqTermSet, k) # get new candiate k-terms set joining step
            currFreqTermSet  = self.getItemsWithMinSupp(transListSet, currCandiItemSet, 
                                                   itemCountDict, self.minSupp) # frequent k-terms set pruning step
            
            
        #
        self.itemCountDict = itemCountDict # 所有候选项以及出现的次数(不仅仅是频繁项),用来计算置信度啊
        self.freqSet       = freqSet       # Only frequent items(a dict: freqSet[1] indicate frequent 1-term set )
        return itemCountDict, freqSet

    def getSpecRules(self):
        rules = {}
        for k, itemSet in self.freqSet.items():
            for item in itemSet:
                for rhs in item:
                    if len(item) > 1:
                        lhs = item - {rhs}
                        support_lhs = self.getSupport(lhs)
                        if support_lhs != 0:  # Pengecekan agar pembagi tidak nol
                            conf = self.getSupport(item) / support_lhs
                            if conf >= self.minConf:
                                rules[(lhs, rhs)] = conf
        return rules
        
    def getMostFrequentItem(self, transListSet):
        """ Get the most frequent item from freq 1-term set """
        mostFreqItem = None
        maxFreq = 0
        for item, freq in self.itemCountDict.items():
            if len(item) == 1 and freq > maxFreq:
                mostFreqItem = item
                maxFreq = freq
        return mostFreqItem
    
    def getSupport(self, item):
        """ Get the support of item """
        return self.itemCountDict[item] / self.transLength
        
        
    def getJoinedItemSet(self, termSet, k):
        """ Generate new k-terms candiate itemset"""
        return set([term1.union(term2) for term1 in termSet for term2 in termSet 
                    if len(term1.union(term2))==k])
    
        
    def getOneItemSet(self, transListSet):
        """ Get unique 1-item set in `set` format 
        """
        itemSet = set()
        for line in transListSet:
            for item in line:
                itemSet.add(frozenset([item]))
        return itemSet
        
    
    def getTransListSet(self, filePath):
        """ Get transactions in list format 
        """
        transListSet = []
        with open(filePath, 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=',')
            for line in reader:
                transListSet.append(set(line))                
        return transListSet
    
    def getItemsWithMinSupp(self, transListSet, itemSet, freqSet, minSupp):
        """ Get frequent item set using min support
        """
        itemSet_  = set()
        localSet_ = defaultdict(int)
        for item in itemSet:
            freqSet[item]   += sum([1 for trans in transListSet if item.issubset(trans)])
            localSet_[item] += sum([1 for trans in transListSet if item.issubset(trans)])
        
        # Only conserve frequent item-set 
        n = len(transListSet)
        for item, cnt in localSet_.items():
            if item != frozenset({''}):  # Menambahkan pengecekan agar tidak memasukkan string kosong
                itemSet_.add(item) if float(cnt)/n >= minSupp else None
        
        return itemSet_
        
    
def create_bar_chart(data):
    # Sort data by value in descending order and get the top 5 items
    sorted_data = dict(sorted(data.items(), key=lambda x: x[1], reverse=True)[:3])
    
    plt.figure(figsize=(10, 6))
    plt.bar(sorted_data.keys(), sorted_data.values(), color='#efcc00')
    plt.xlabel('Books')
    plt.ylabel('Frequency')
    plt.title('Peminjaman Buku Perpustakaan Universitas Sriwijaya')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Return the figure
    return plt

                