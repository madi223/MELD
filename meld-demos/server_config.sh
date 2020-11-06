cd /home/oaici/openairinterface5g
git fetch --all --prune --quiet
git checkout --quiet develop_inria_ci_deployment
git pull --quiet origin develop_inria_ci_deployment
sudo ip route add 12.0.0.0/24 via 192.168.3.17 dev control
sudo ip route add 12.1.1.0/24 via 192.168.3.17 dev control
sudo ifconfig data 192.168.2.14/24 up
sudo docker container start rabbitmq
