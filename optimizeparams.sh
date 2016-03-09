echo "Optimizing parameters for dataset no. $1"
rm data/tinyshakespeare/*
rm trainfile
rm testfile
rm dpbx$1-train.nn
rm dpbx$1-train.nn.patt.nonl

for i in ~/Dropbox/poetryCorpora/trainTestSet$1/train/*.xml; do python ~/Dropbox/poetryCorpora/oldCorpusReader.py $i; done >dpbx$1-train.nn
#for i in ~/Dropbox/poetryCorpora/trainTestSet$1/test/*.xml; do python ~/Dropbox/poetryCorpora/oldCorpusReader.py $i; done >dpbx$1-test.nn
./mapPatts.sh dpbx$1-train.nn > dpbx$1-train.nn.patt.nonl
rm dpbx$1-train.nn
#./mapPatts.sh dpbx$1-test.nn > dpbx$1-test.nn.patt.nonl
#rm dpbx$1-test.nn
head -n -10 dpbx$1-train.nn.patt.nonl > trainfile
tail -n10 dpbx$1-train.nn.patt.nonl > testfile

#ln -s `pwd`/dpbx$1-train.nn.patt.nonl data/tinyshakespeare/input.txt
ln -s `pwd`/trainfile data/tinyshakespeare/input.txt
rm dpbx$1-train.nn.patt.nonl

#FOREACH PARAMETERS:
#checkpointdir="cv"
#mkdir $checkpointdir
#th train.lua -print_every 40 -eval_val_every 100 -max_epochs 20 -checkpoint_dir $checkpointdir

for model in "lstm" "gru" "rnn"
do
  for rnnsize in 64 128 256
  do
    for numlayers in 2 3 4
    do
      for dropout in 0 0.1
      do
        for seqlength in 20 30
        do
          for batchsize in 20 30
            do
              resultsdir="results/"$model"="$rnnsize"="$numlayers"="$dropout"="$seqlength"="$batchsize"/"
              command="th train.lua -print_every 40 -eval_val_every 100 -checkpoint_dir $resultsdir -losslog $resultsdir/out.txt -model $model -rnn_size $rnnsize -num_layers $numlayers -dropout $dropout -seq_length $seqlength -batch_size $batchsize"
              echo $command
              $command
#              read name
            done
        done
      done
    done
  done
done




#python callSampleMod.py cv/lm_lstm_epoch60.00_1.4352.t7 kk.test | tail -n3

#
#for i in results/lstm=*; do echo $i; python callSampleMod.py $i/lm_lstm_epoch20* testfile > $i/result.txt; done
