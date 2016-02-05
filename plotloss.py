import sys
import matplotlib.pyplot as plt
#http://matplotlib.org/users/pyplot_tutorial.html
#http://matplotlib.org/1.3.0/examples/pylab_examples/legend_demo.html
#th train.lua -seq_length 54 -batch_size 10 -print_every 20 -eval_val_every 100

f=open(sys.argv[1])
png=sys.argv[2]

l=[line.rstrip().split(" ") for line in f]
f.close()
epochs=[i[0] for i in l]
train_losses=[i[1] for i in l]
val_losses=[i[2] for i in l]
plt.plot(epochs, train_losses, 'r', label="Train loss")
plt.plot(epochs, val_losses, 'b', label="Validation loss")
plt.legend(loc='upper right', shadow=True)
if (png=='yes'):
    plt.savefig(sys.argv[1].split(".")[0]+".png")
else:
    plt.show()

