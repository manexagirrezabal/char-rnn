
import sys
import re
import os
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import accuracy_score
import numpy as np

# +-+-+   | A         #
# +-+--   | B         #
# -+--+   | C         #
# +-+-    | D         #
# -+-+    | E         #
# -+--    | F         #
# --+-    | G         #
# +-+     | H         #
# +--     | I         #
# -+-     | J         #
# --+     | K         #
# --      | L         #
# -+      | M         #
# +-      | N         #
# ++      | O         #
# -       | P         #
# +       | Q         #
mapping={}
mapping['A']='+-+-+'
mapping['B']='+-+--'
mapping['C']='-+--+'
mapping['D']='+-+-'
mapping['E']='-+-+'
mapping['F']='-+--'
mapping['G']='--+-'
mapping['H']='+-+'
mapping['I']='+--'
mapping['J']='-+-'
mapping['K']='--+'
mapping['L']='--'
mapping['M']='-+'
mapping['N']='+-'
mapping['O']='++'
mapping['P']='-'
mapping['Q']='+'

def divide (str):
    if str != '':
        #print "DIVIDE"
        pat= re.search("(\w+)_(.)", str)
        #print "-"
        if pat != None:
#            print str
#            print (pat.group(1), pat.group(2))
            return (pat.group(1), pat.group(2))

def lastchar(st):
    return st[len(st)-1]

#model ="cv/lm_lstm_epoch50.00_1.5602.t7"
model = sys.argv[1]
def makepred (input):
    comm = "th samplemod.lua "+model+" -gpuid -1 -primetext '"+input+"_' -length 1 -verbose 0"
    #print comm
    res = os.popen(comm)
    return unicode(lastchar(res.read().strip()))

def get(tup, posit, defval):
    
    if tup==None:
        return defval
    else:
        return tup[posit]

#classes = set([get(el,1, "<UNK>") for line in lines for el in line])
classes = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q']
rawinput=False

if rawinput:

    phrase=""
    input=raw_input()
    while input:
        phrase = phrase+input
        comm = "th samplemod.lua "+model+" -gpuid -1 -primetext '"+phrase+"_' -length 1 -verbose 0"
        print comm
        pred = os.popen(comm).read().rstrip()
        print pred+mapping[pred[len(pred)-1]]
        phrase = phrase+"_"+pred[len(pred)-1]+" "
#        print phrase
#        print res.read()
        input = raw_input()


else:

    f=open(sys.argv[2])
    lines = [[divide(k) for k in i.decode("utf8").rstrip().split(" ")] for i in f]
    f.close()

    y_true=[]
    y_pred=[]
    phrase=""
    kont=0
    import progressbar
    with progressbar.ProgressBar(max_value=len(lines)) as progress:
        for line in lines:
            for word in line:
                if word != None:
                    phrase = phrase+word[0]
#                    print phrase
                    pred=makepred (phrase)
#                    print pred
#                    print pred, word[1], pred==word[1]
                    y_true.append(word[1])
                    y_pred.append(pred)
                    if pred not in classes:
                        print "The unknown:"+pred+"-"
                    phrase = phrase+"_"+pred+" "
#                else: #When None comes, it means that there's an empty line, so let's set our seed to the empty string
#                    phrase = ''
#            print
#            phrase = phrase +"\n"
            kont=kont+1
            phrase= ''
            progress.update(kont)

    print sorted(list(set(y_pred).union(set(y_true))))
    print "LABELS: "+' '.join([mapping.get(i,"<UNK>") for i in list(classes)])
#    prf1s = precision_recall_fscore_support(y_true, y_pred, labels=["J","M","N","P","Q","H","I","A","B","C","D","E","F","G","K","L","O"])
    prf1s = precision_recall_fscore_support(y_true, y_pred)
    prf1smi = precision_recall_fscore_support(y_true, y_pred, average='micro')
    prf1sma = precision_recall_fscore_support(y_true, y_pred, average='macro')
    print prf1s
    print "MICRO,"+unicode(prf1smi[0])+","+unicode(prf1smi[1])+","+unicode(prf1smi[2])
    print "MACRO,"+unicode(prf1sma[0])+","+unicode(prf1sma[1])+","+unicode(prf1sma[2])
    print "ACCURACY,"+unicode(accuracy_score(y_true, y_pred))
    
#    print "MACRO,"+unicode(np.mean(prf1s[0]))+","+unicode(np.mean(prf1s[1]))+","+unicode(np.mean(prf1s[2]))

#    print 
#    print precision_recall_fscore_support(y_true, y_pred, average='micro')
