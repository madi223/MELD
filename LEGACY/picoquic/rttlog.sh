current=$(pwd)
if [ $# -lt 1 ]
then
   echo "[usage]: ./rttlog.sh <logdir>"
   exit 1
fi

logdir=$1

######## CSV conversion #############
cd $logdir
i=1
for f in *.log; do
	 ../picolog_t -f csv -o "../"$logdir $f;
done

####### RTT in ms ##################
mkdir temp
i=1
for f in *.csv; do
    awk -F , '{print $1/1000000","$8/1000}' $f > "temp/rtt-sec"$i".csv";
    i=$((i+1 ));
done

#### RTT increase at every second ########
cd $current
cp parse-rtt.py $logdir"/temp/"
cd $logdir"/temp/"
i=1;
for f in rtt-sec*.csv; do
    python3 parse-rtt.py -d $f -n $i;
    i=$((i+1 ));
done

#### Combining csv files together #######
i=1
rm -rf rtt-qr.csv
for f in rtt-fin*.csv; do
    cat $f >> rtt-qr.csv;
    i=$((i+1 ));
done

#### Calculate Confidence Interval ######
cd $current
python3 getint.py -d $logdir"/temp/rtt-qr.csv"
