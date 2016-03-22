
import sys
import re
import os
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import accuracy_score
import numpy as np
from skll.metrics import kappa

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
mapping['-']='-'
mapping['=']='='
mapping['+']='+'

def makepred (input, model):
    comm = "th samplemod.lua "+model+" -gpuid -1 -primetext \""+input.replace("\"", "\\\"")+"_\" -length 1 -verbose 0"
#    print comm.encode("utf8")
    res = os.popen(comm.encode("utf8"))
    #http://stackoverflow.com/questions/26541968/delete-every-non-utf-8-symbols-froms-string
    restxt=res.read().decode("utf8",'ignore')
    return unicode(lastchar(restxt.strip()))

def get(tup, posit, defval):
    
    if tup==None:
        return defval
    else:
        return tup[posit]

def divide (str):
#    if str != '':
#        pat= re.search("(\w+)_(.)", str)
#        if pat != None:
#            return (pat.group(1), pat.group(2))
    pat = str.split("_")
    if len(pat)>1:
        return (pat[0],pat[1])

def lastchar(st):
    return st[len(st)-1]

def stats (list1,list2):
    print "Predictions:"
    print list1
    print list(reversed(list2)) #COMPARABLE ORDER
    print

    list1fl=[class2float(i) for i in list1]
    list2fl=[class2float(i) for i in list(reversed(list2))]

    print list1fl
    print list2fl

    print
    print kappa(list1fl,list2fl) #http://skll.readthedocs.org/en/latest/_modules/skll/metrics.html
    print
    print list2


if len(sys.argv) < 3:
  print "Error"
  print "Usage: ~$ python "+sys.argv[0]+" MODEL(ltr) MODEL(rtl) [test-file(ltr)]"
  print
  print "This program gets as input two models for the char-rnn package."
  print "Each of the models has the capability of tagging a poem's stresses going from left to right or from right to left, respectively."
  print "If we include a third parameter, it must be a file in which we want to test our models. The file format should be the one for the first evaluator, left to right."
  print
  print "NO WARRANTY. IT MAY NOT WORK!!"
  print "Manex :-P"
  print
  exit(-1)


#model ="cv/lm_lstm_epoch50.00_1.5602.t7"
model1 = sys.argv[1]
model2 = sys.argv[2]
print "Working with these models:",model1, model2

#classes = set([get(el,1, "<UNK>") for line in lines for el in line])
classes = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q']
#classes = ['-','+']
classes = ['=','+']
rawinput=len(sys.argv)==3

def class2float(k):
  if k=='+'.encode("utf8"):
    return 1.0
  elif k=='='.encode("utf8"):
    return 0.0
  else:
    return -1.0

if rawinput:

    ltrpreds=[]
    rtlpreds=[]

    ltrphrase=""
    input=raw_input().decode("utf8")
    while input:
        ltrphrase = ltrphrase+input
        pred = makepred (ltrphrase, model1)
        print pred
        ltrpreds.append(pred)
        ltrphrase = ltrphrase+"_"+pred[-1]+" "
        input = raw_input().decode("utf8")
    print ltrphrase.encode("utf8")
    ltrphrase=ltrphrase.rstrip()

    rtlphrase=""
    print type(ltrphrase)
    for i in reversed(ltrphrase.split(" ")):
        print i.encode("utf8")
        rtlphrase = rtlphrase + i[:-2]
        rtlpred = makepred (rtlphrase, model2)
        print rtlpred.encode("utf8")
        rtlpreds.append(rtlpred)
        rtlphrase = rtlphrase +"_"+rtlpred[-1]+" "
    print rtlphrase.encode("utf8")

    stats(ltrpreds, rtlpreds)



else:

    f=open(sys.argv[3])
    lines = [[divide(k) for k in i.decode("utf8").rstrip().split(" ")] for i in f]
    f.close()

    y_true=[]
    y_predltr=[]
    y_predrtl=[]
    phraseltr=""
    kont=0
    import progressbar
    with progressbar.ProgressBar(max_value=len(lines)) as progress:
        for line in lines:
            for word in line:
                if word != None:
                    phraseltr = phraseltr+word[0]
#                    print phraseltr
                    pred=makepred (phraseltr, model1)
#                    print pred
#                    print pred, word[1], pred==word[1]
                    y_true.append(word[1])
                    y_predltr.append(pred)
                    if pred not in classes:
                        print "The unknown:"+pred.encode("utf8")+"-"
                    phraseltr = phraseltr+"_"+pred+" "
#                else: #When None comes, it means that there's an empty line, so let's set our seed to the empty string
#                    phraseltr = ''

            if word != None:
                phraseltr=phraseltr.rstrip()

                y_predrtllocal=[]
                phrasertl=""
                for i in reversed(phraseltr.split(" ")):
#                    print "i --> "+i.encode("utf8")
                    phrasertl = phrasertl + i[:-2]
                    rtlpred = makepred (phrasertl, model2)
#                    print rtlpred.encode("utf8")
#                    y_predrtl.append(rtlpred)
                    y_predrtllocal.insert(0,rtlpred)
                    phrasertl = phrasertl +"_"+rtlpred[-1]+" "

                y_predrtl=y_predrtl+y_predrtllocal
            #print
            #print "LENGTHS",len(y_predrtl),len(y_predltr), word
            #print 

#            print phraseltr
#            print phrasertl
#            print
#            print y_predltr
#            print y_predrtl


#            print
            kont=kont+1
            phraseltr= ''
            progress.update(kont)

#    print sorted(list(set(y_predltr).union(set(y_true))))
#    print "LABELS: "+' '.join([mapping.get(i,"<UNK>") for i in list(classes)])

#    prf1sltr = precision_recall_fscore_support(y_true, y_predltr, labels=["J","M","N","P","Q","H","I","A","B","C","D","E","F","G","K","L","O"])
    prf1sltr = precision_recall_fscore_support(y_true, y_predltr)
    prf1sltrmi = precision_recall_fscore_support(y_true, y_predltr, average='micro', pos_label=None)
    prf1sltrma = precision_recall_fscore_support(y_true, y_predltr, average='macro', pos_label=None)

#    prf1srtl = precision_recall_fscore_support(y_true, y_predrtl, labels=["J","M","N","P","Q","H","I","A","B","C","D","E","F","G","K","L","O"])
    prf1srtl = precision_recall_fscore_support(y_true, y_predrtl)
    prf1srtlmi = precision_recall_fscore_support(y_true, y_predrtl, average='micro', pos_label=None)
    prf1srtlma = precision_recall_fscore_support(y_true, y_predrtl, average='macro', pos_label=None)

    print "Left-to-Right analyzer info:"
    print prf1sltr
    print "MICRO,"+unicode(prf1sltrmi[0])+","+unicode(prf1sltrmi[1])+","+unicode(prf1sltrmi[2])
    print "MACRO,"+unicode(prf1sltrma[0])+","+unicode(prf1sltrma[1])+","+unicode(prf1sltrma[2])
    print "ACCURACY,"+unicode(accuracy_score(y_true, y_predltr))

    print "Right-to-Left analyzer info:"
    print prf1srtl
    print "MICRO,"+unicode(prf1srtlmi[0])+","+unicode(prf1srtlmi[1])+","+unicode(prf1srtlmi[2])
    print "MACRO,"+unicode(prf1srtlma[0])+","+unicode(prf1srtlma[1])+","+unicode(prf1srtlma[2])
    print "ACCURACY,"+unicode(accuracy_score(y_true, y_predrtl))

    print "Kappa statistics / Agreement among models"

    list1fl=[class2float(i) for i in y_predltr]
    list2fl=[class2float(i) for i in y_predrtl]

    #print list1fl
    #print list2fl
    print kappa (list1fl, list2fl)
    
#    print "MACRO,"+unicode(np.mean(prf1sltr[0]))+","+unicode(np.mean(prf1sltr[1]))+","+unicode(np.mean(prf1sltr[2]))

#    print 
#    print precision_recall_fscore_support(y_true, y_predltr, average='micro')




