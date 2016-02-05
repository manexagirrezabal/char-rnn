for i in ~/Dropbox/poetryCorpora/trainTestSet2/train/*.xml; do python ~/train/corpusReader2.py $i; done >dpbx2-train.nn
./mapPatts.sh dpbx2-train.nn > dpbx2-train.nn.patt.nonl
rm dpbx2-train.nn
rm data/tinyshakespeare/input.txt
ln -s ~/char-rnn/dpbx2-train.nn.patt.nonl data/tinyshakespeare/input.txt
th train.lua -seq_length 27 -batch_size 10 -print_every 40 -eval_val_every 100

th train.lua -print_every 40 -eval_val_every 100 -losslog logs/dpbx2-default.txt
th train.lua -seq_length 27 -batch_size 10 -print_every 40 -eval_val_every 100 -losslog logs/dpbx2-seq_len27-batch_size10.txt
th train.lua -seq_length 27 -batch_size 20 -print_every 40 -eval_val_every 100 -losslog logs/dpbx2-seq_len27-batch_size20.txt
th train.lua -seq_length 27 -batch_size 30 -print_every 40 -eval_val_every 100 -losslog logs/dpbx2-seq_len27-batch_size30.txt
