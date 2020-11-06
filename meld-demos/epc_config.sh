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
cd /home/oaici/openair-cn/scripts
sudo oai_hss -j /usr/local/etc/oai/hss_rel14.json &
sudo ./run_mme --config-file /usr/local/etc/oai/mme.conf --set-virt-if &
sudo spgwc -c /usr/local/etc/oai/spgw_c.conf &
sudo spgwu -c /usr/local/etc/oai/spgw_u.conf &
