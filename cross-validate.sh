#usage ./cross-validate [w2w|s2s]
mode=$1
inputdata="/home/magirrezaba008/Dropbox/poetryCorpora/formattedCorpus/10foldCVDL"${mode}
actuald=`pwd`

rm tmp/* -rf

for i in 1 2 3 4 5 6 7 8 9 10
do
  rm data/tinyshakespeare/*
  ./mapPatts.sh ${inputdata}/newcorpus-train-${i}-of-10.DL${mode} > tmp/newcorpus-train-${i}-of-10.DL${mode}
  ln -s ${actuald}/tmp/newcorpus-train-${i}-of-10.DL${mode} ${actuald}/data/tinyshakespeare/input.txt
  resultsdir="tmp/cv"$i
  th train.lua -print_every 40 -eval_val_every 100 -checkpoint_dir $resultsdir -losslog $resultsdir/out.txt
done

mv tmp/ "DL"${mode}"results"
mkdir tmp
#Check with plotloss.py which is the minima of the validation error
#for i in 1 2 3 4 5 6 7 8 9 10
#do
#  python plotloss.py "DL"${mode}"results"/cv${i}/out.txt no
#done

#Using the checkpoint at that epoch, evaluate the system with the test set.
#First, we map the test sets:
#for i in 1 2 3 4 5 6 7 8 9 10
#do
#  ./mapPatts.sh ${inputdata}/newcorpus-test-${i}-of-10.DL${mode} > "DL"${mode}"results"/newcorpus-test-${i}-of-10.DL${mode}
#done


#for i in 1 2 3 4 5 6 7 8 9 10
#do
#  python callSampleMod.py DLw2wresults/cv${i}/lm_lstm_epoch50* DLw2wresults/newcorpus-test-${i}-of-10.DLw2w
#done

