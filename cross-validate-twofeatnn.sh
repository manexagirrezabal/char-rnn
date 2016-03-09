#usage ./cross--validate-twofeatnn.sh
inputdata="/home/magirrezaba008/Dropbox/poetryCorpora/dl2featltrcorpus/10foldCV/"
actuald=`pwd`

rm tmp/* -rf

for i in 1 2 3 4 5 6 7 8 9 10
do
  rm data/tinyshakespeare/*
#  ./mapPatts.sh ${inputdata}/newcorpus-train-${i}-of-10.twofeatnn.crf > tmp/newcorpus-train-${i}-of-10.twofeatnn.crf.mapped
  ln -s ${inputdata}/newcorpus-train-${i}-of-10.txt ${actuald}/data/tinyshakespeare/input.txt
  resultsdir="tmp/cv"$i
  th train.lua -print_every 40 -eval_val_every 100 -checkpoint_dir $resultsdir -losslog $resultsdir/out.txt
done

mv tmp/ "DLsyll2featltrresults"
mkdir tmp
