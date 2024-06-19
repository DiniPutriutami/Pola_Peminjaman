# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 10:05:45 2018

@author: zbj
"""

from optparse import OptionParser    # parse command-line parameters
from apriori import Apriori

if __name__ == '__main__':
    
    # Parsing command-line parameters
    optParser = OptionParser()
    optParser.add_option('-f', '--file', 
                         dest='filepath',
                         help='Input a csv file',
                         type='string',
                         default=None)  # input a csv file
                         
    optParser.add_option('-s', '--minsupport', 
                         dest='minsupport',
                         help='Mininum support',
                         type='float',
                         default=0.000)  # mininum support value
                         
    optParser.add_option('-c', '--minconfident', dest='minconfident',
                         help='Mininum confidence',
                         type='float',
                         default=0.000)  # mininum confidence value    
                         
    
    (options, args) = optParser.parse_args()       
        
    # Get two important parameters
    filePath = options.filepath
    minSupp  = options.minsupport
    minConf  = options.minconfident
    print("""Parameters: \n - filePath: {} \n - mininum support: {} \n - mininum confidence: {}\n""".\
          format(filePath,minSupp,minConf))

    # Run and print
    objApriori = Apriori(minSupp, minConf)
    itemCountDict, freqSet = objApriori.fit(filePath)
    transListSet = objApriori.getTransListSet(filePath)  # Definisikan transListSet di sini
    for key, value in freqSet.items():
        print('frequent {}-term set:'.format(key))
        print('-'*20)
        for itemset in value:
            support = objApriori.getSupport(itemset)
            print(list(itemset), "Support: {:.3f}".format(support))  # Cetak nilai support dengan tiga angka desimal
        print()


    # Return rules with regard of `rhs`
    rules = objApriori.getSpecRules()
    print('-'*20)
    print('rules refer to {}'.format(list(itemset)))
    for key, value in rules.items():
        antecedent = list(key[0])
        consequent = key[1]
        conf = value
        antecedent_str = ', '.join(antecedent)
        rule_str = f"[{antecedent_str}, {consequent}]"  # Format aturan asosiasi
        lift = objApriori.getLiftRatio(frozenset(antecedent), frozenset([consequent]))
        print('{} --> confidence: {:.3f}, lift: {:.3f}'.format(rule_str, conf, lift))
    print('-'*20)

    