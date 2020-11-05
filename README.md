# MELD
MELD (MEC-based Edge Loss Discrimination) is a novel server-side loss discrimination mechanism that leverages recent advancements in Multi-access Edge Computing (MEC) services to discriminate packet losses based on real-time RAN statistics. MELD is built on top of picoquic (https://github.com/private-octopus/picoquic), all the experiments have been performed on r2lab (https://r2lab.inria.fr). Find below the required steps in order to reproduce the results shown in the paper.

# Step 1 : Building OAI and FlexRAN infrastructure
## 1.1 Launch nodes images on r2lab
From faraday gateway launch the following images
```
$ rload -i flex-epc 17
$ rload -i flex-enb 23
$ rload -i flex-pico-ue 6
$ rload -i flex-pico-server 14
$ rload -i u16.48-gnuradio-3.7.10-uhd-images 13
```
## 1.2 Configure the server and start FlexRan Controller (fit14)
Connect to the server and set the routes using the commands below:
```
$ ssh oaici@fit14 (passwor=linux)
$ sudo ip route add 12.0.0.0/24 via 192.168.3.17 dev control
$ sudo ip route add 12.1.1.0/24 via 192.168.3.17 dev control
$ sudo ifconfig data 192.168.2.14/24 up
```
Launch rabbitmq and FlexRan controller
```
$ sudo docker container start rabbitmq
$ cd flexran-rtc/
$ ./run_flexran_rtc.sh
```
## 1.3 Start the EPC (fit17)
```
ssh oaici@fit17 (password=linux)
sudo ifconfig control:m11 172.16.1.102 up
sudo ifconfig control:m10 192.168.10.110 up
sudo ifconfig control:sxu 172.55.55.102 up
sudo ifconfig control:sxc 172.55.55.101 up
sudo ifconfig control:s5c 172.58.58.102 up
sudo ifconfig control:p5c 172.58.58.101 up
sudo ifconfig control:s11 172.16.1.104 up
sudo ip route add default via 192.168.3.100 dev control table lte
sudo ip rule add from 12.0.0.0/8 table lte
sudo ip rule add from 12.1.1.0/8 table lte
cd ~/openair-cn/scripts
sudo oai_hss -j /usr/local/etc/oai/hss_rel14.json &
sudo ./run_mme --config-file /usr/local/etc/oai/mme.conf --set-virt-if &
sudo spgwc -c /usr/local/etc/oai/spgw_c.conf &
sudo spgwu -c /usr/local/etc/oai/spgw_u.conf &
```
## 1.4 Start the eNodeB (fit23)
```
ssh oaici@fit23 (password=linux)
sudo ifconfig data 192.168.2.23/24 up
cd ~/openairinterface5g
source oaienv
cd cmake_targets
sudo -E ./lte_build_oai/build/lte-softmodem -O ~/openairinterface5g/ci-scripts/conf_files/ci-enb.band7.tm1.25PRB.usrpb210.conf --eNBs.[0].rrc_inactivity_threshold 0 --RUs.[0].max_rxgain 120 --eNBs.[0].component_carriers.[0].pusch_p0_Nominal -90 --eNBs.[0].component_carriers.[0].pucch_p0_Nominal -96 --eNBs.[0].tracking_area_code 600 --eNBs.[0].plmn_list.[0].mnc 95 --THREAD_STRUCT.[0].parallel_config PARALLEL_RU_L1_TRX_SPLIT
```
## 1.5 Start the UE (fit06)
```
ssh oaici@fit06
cd ~/openairinterface5g
source oaienv
cd cmake_targets/lte_build_oai/build
echo -e "s#93#95#\ns#0100001111#0000000012#\ns#e734f8734007d6c5ce7a0508809e7e9c#8e27b6af0e692e750f32667a3b14605d#\ns#33611123456#001011234561010#" > adapt_usim_parameters.sed
sed -f adapt_usim_parameters.sed ../../../openair3/NAS/TOOLS/ue_eurecom_test_sfr.conf > ../../../openair3/NAS/TOOLS/ci-ue_eurecom_test_sfr.conf
../../../targets/bin/conf2uedata -c ../../../openair3/NAS/TOOLS/ci-ue_eurecom_test_sfr.conf -o .
sudo ./lte-uesoftmodem -C 2660000000 -r 25 --ue-rxgain 125 --ue-txgain 0 --ue-max-power -6 --ue-scan-carrier --nokrnmod 1
```
## 1.6 Start the AWGN (Additive White Gaussian Noise) generator (fit13) 
```
ssh root@fit13
enable-usrp-ethernet
uhd_siggen --gaussian -f 2425M -g -10
```
# Step 2 : Testing MELD
You can test Legacy picoquic, MELD-DE and MELD-ME by launching picoquicdemo in the correspondign directory, for instance, in order to test MELD-DE, you need to follow the steps below:
## Launch the publish process
Open a new terminal on the server (fit14) and copy the RNTI of the UE from FlexRAN controller:
```
ssh oaici@fit14
cd rnis_dev/
python3 rnis_pub.py -r <RNTI>
```
## Launch picoquic server with Cubic or NewReno
In another terminal, connect to the server and launch the following commands:
```NewReno
cd MELD/MELD-DE/picoquic/
mkdir reno-log
./picoquicdemo -p 4443 -w . -G reno -L -b reno-log
```
or
```Cubic
cd MELD/MELD-DE/picoquic/
mkdir cubic-log
./picoquicdemo -p 4443 -w . -G cubic -L -b cubic-log
```
## Download 20MB file from the UE
Connect to the UE and add the following route:
```
ssh oaici@fit06
sudo ip route add 192.168.3.14/32 dev oaitun_ue1
```
Stop and relaunch the publish process (make sure it is still running while downloading).
```
```
From the UE start the download:
```
oaici@fit06~: cd rnis_dev/picoquic/
oaici@fit06~: ./picoquicdemo -D 192.168.3.14 4443 8:/20MB
```
# Step 4 : Analysing and Interpreting log results in csv
After running the desired number of tests, stop picoquicdemo at the server and launch the following script
```
./rttlog.sh reno-log
```
or
```
./rttlog.sh cubic-log
```
rttlog.sh generate a csv file (rtt-<timestamp>.csv) the mean RTT and confidence interval at each second
```
time,mean,error  
1,247.8873545821989,282.06587808664585
2,238.97878824767338,244.03404046253155
3,252.68859432726705,325.54888976613205
4,257.12052580774645,241.32091918536278
5,256.76023007035195,236.52503657900186
6,259.97328753428053,320.8926477570124
7,263.1348330754019,216.4134579022659
8,259.5439771741548,261.270701678302
9,265.88118376922165,267.0920855984539
10,265.8011558973408,247.45082362359005
```
You can plot the content of this csv file with your favorite vizualization tool (python seaborn, gnuplot, tikz etc.) For instance, with seaborn got the following graphs for MELD-DE, MELD-ME and Legacy picoquic
