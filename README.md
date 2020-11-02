# MELD
MELD (MEC-based Edge Loss Discrimination) is a novel server-side loss discrimination mechanism that leverages recent advancements in Multi-access Edge Computing (MEC) services to discriminate packet losses based on real-time RAN statistics. MELD is built on top of picoquic (https://github.com/private-octopus/picoquic), all the experiments have been performed on r2lab (https://r2lab.inria.fr). Find below the required steps in order to reproduce the results shown in the paper.

# Step 1 : Building OAI and FlexRAN infrastructure
## Launch nodes images on r2lab
From faraday gateway launch the following images
```
$ rload -i flex-epc 17
$ rload -i flex-enb 23
$ rload -i flex-pico-ue 6
$ rload -i flex-pico-server 14
$ rload -i u16.48-gnuradio-3.7.10-uhd-images 13
```
## Configure the server and start FlexRan Controller (fit14)
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
## Starting the EPC (fit17)
```
```
