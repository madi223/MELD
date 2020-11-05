import csv
import argparse
#import csv
parser = argparse.ArgumentParser()
parser.add_argument("--data","-d",help="absolute path of dataset.csv",required=True)
parser.add_argument("--num","-n",help="absolute path of dataset.csv",required=True)
args = parser.parse_args()
data = args.data
num = args.num
f = open("rtt-fin"+str(num)+".csv","w")
with open(data) as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    tmp = 0
    count = 0
    sm = 0
    tot = 0
    for row in csv_reader:
        if count == 0:
            print("line 0\n")
            count += 1
        else:
            hook = tmp+1
            if (hook > int(float(row[0]))):
                print("{}".format(row[0]))
                sm = sm+float(row[1])
                tot +=1
                #tmp = int(row[1])
            else:
                mean = sm/tot
                f.write("{},{}\n".format(tmp,mean))
                tmp +=1
                sm = float(row[1])
                tot = 1
            count += 1
f.close()
