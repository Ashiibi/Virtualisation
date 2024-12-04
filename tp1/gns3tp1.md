
🌞 **Déterminer l'adresse MAC de vos deux machines**

~~~
pc1> show ip all

NAME   IP/MASK              GATEWAY           MAC                DNS
pc1    10.1.1.1/24          0.0.0.0           00:50:79:66:68:01


pc2> show ip all

NAME   IP/MASK              GATEWAY           MAC                DNS
pc2    10.1.1.2/24          0.0.0.0           00:50:79:66:68:00
~~~

🌞 **Définir une IP statique sur les deux machines**
~~~
pc1> ip 10.1.1.1/24
Checking for duplicate address...
pc1 : 10.1.1.1 255.255.255.0


pc1> show ip all

NAME   IP/MASK              GATEWAY           MAC                DNS
pc1    10.1.1.1/24          0.0.0.0           00:50:79:66:68:01


pc2> ip 10.1.1.2/24
Checking for duplicate address...
pc2 : 10.1.1.2 255.255.255.0


pc2> show ip all

NAME   IP/MASK              GATEWAY           MAC                DNS
pc2    10.1.1.2/24          0.0.0.0           00:50:79:66:68:00
~~~
🌞 **Effectuer un `ping` d'une machine à l'autre**
~~~
pc1> ping 10.1.1.2

84 bytes from 10.1.1.2 icmp_seq=1 ttl=64 time=0.676 ms


pc2> ping 10.1.1.1

84 bytes from 10.1.1.1 icmp_seq=1 ttl=64 time=0.243 ms
~~~


🌞 **Wireshark !**

cf gnsw1.pcapng, Protocol ICMP

🌞 **ARP**

~~~
pc1> ping 10.1.1.2

84 bytes from 10.1.1.2 icmp_seq=1 ttl=64 time=0.168 ms


pc1> show arp

00:50:79:66:68:00  10.1.1.2 expires in 114 seconds
~~~

🌞 **Déterminer l'adresse MAC de vos trois machines**
~~~
pc1> show ip all

NAME   IP/MASK              GATEWAY           MAC                DNS
pc1    10.1.1.1/24          0.0.0.0           00:50:79:66:68:01


pc2> show ip all

NAME   IP/MASK              GATEWAY           MAC                DNS
pc2    10.1.1.2/24          0.0.0.0           00:50:79:66:68:00


pc3> show ip all

NAME   IP/MASK              GATEWAY           MAC                DNS
pc3    10.1.1.3/24          0.0.0.0           00:50:79:66:68:02
~~~

🌞 **Définir une IP statique sur les trois machines**
~~~
pc1> ip 10.1.1.1/24
Checking for duplicate address...
pc1 : 10.1.1.1 255.255.255.0

pc2> ip 10.1.1.2/24
Checking for duplicate address...
pc2 : 10.1.1.2 255.255.255.0

pc3> ip 10.1.1.3/24
Checking for duplicate address...
pc3 : 10.1.1.3 255.255.255.0
~~~

🌞 **Effectuer des `ping` d'une machine à l'autre**
~~~
pc1> ping 10.1.1.2

84 bytes from 10.1.1.2 icmp_seq=1 ttl=64 time=0.895 ms


pc2> ping 10.1.1.3

84 bytes from 10.1.1.3 icmp_seq=1 ttl=64 time=0.288 ms


pc1> ping 10.1.1.3

84 bytes from 10.1.1.3 icmp_seq=1 ttl=64 time=0.871 ms
~~~


🌞 **Donner un accès Internet à la machine `dhcp.tp1.efrei`**
~~~
[root@localhost ~]# ping 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=116 time=24.5 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=116 time=37.0 ms

dnf install dhcp-server
~~~
🌞 **Installer et configurer un serveur DHCP**

~~~

[root@localhost dhcp]# sudo vi /etc/sysconfig/network-scripts/ifcfg-enp0s3
[root@localhost dhcp]# sudo nmcli connection reload
[root@localhost dhcp]# sudo nmcli connection up lan
Connection successfully activated (D-Bus active path: /org/freedesktop/NetworkManager/ActiveConnection/29)
[root@localhost dhcp]# sudo nmcli connection down lan
Connection 'lan' successfully deactivated (D-Bus active path: /org/freedesktop/NetworkManager/ActiveConnection/29)
[root@localhost dhcp]# sudo nmcli connection up lan
Connection successfully activated (D-Bus active path: /org/freedesktop/NetworkManager/ActiveConnection/31)
[root@localhost dhcp]# ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:3f:61:2b brd ff:ff:ff:ff:ff:ff
    inet 10.1.1.10/24 brd 10.1.1.255 scope global noprefixroute enp0s3
       valid_lft forever preferred_lft forever
    inet6 fe80::a00:27ff:fe3f:612b/64 scope link
       valid_lft forever preferred_lft forever
[root@localhost dhcp]# cat /etc/sysconfig/network-scripts/ifcfg-enp0s3
DEVICE=enp0s3
NAME=lan

ONBOOT=yes
BOOTPROTO=static

IPADDR=10.1.1.10
NETMASK=255.255.255.0

[root@localhost ~]# vi /etc/dhcp/dhcpd.conf
subnet 10.1.1.0
netmask 255.255.255.0 {
    range 10.1.1.10 10.1.1.50;
    option broadcast-address 10.1.1.1;
    option routers 10.1.1.1;
    option subnet-mask 255.255.255.0;
}
[root@localhost ~]# sudo systemctl restart dhcpd
~~~
🌞 Récupérer une IP automatiquement depuis les 3 nodes
~~~
Pc1> dhcp
Pc1> show ip

NAME        : VPCS[1]
IP/MASK     : 10.1.1.11/24
GATEWAY     : 10.1.1.1
DNS         :
DHCP SERVER : 10.1.1.10
DHCP LEASE  : 43007, 43200/21600/37800
MAC         : 00:50:79:66:68:02
LPORT       : 20011
RHOST:PORT  : 127.0.0.1:20012
MTU         : 1500

Pc2> dhcp
Pc2> show ip

NAME        : VPCS[1]
IP/MASK     : 10.1.1.12/24
GATEWAY     : 10.1.1.1
DNS         :
DHCP SERVER : 10.1.1.10
DHCP LEASE  : 42986, 43200/21600/37800
MAC         : 00:50:79:66:68:00
LPORT       : 20007
RHOST:PORT  : 127.0.0.1:20008
MTU         : 1500

Pc3> dhcp
pc3> show ip

NAME        : pc2[1]
IP/MASK     : 10.1.1.13/24
GATEWAY     : 10.1.1.1
DNS         :
DHCP SERVER : 10.1.1.10
DHCP LEASE  : 42939, 43200/21600/37800
MAC         : 00:50:79:66:68:01
LPORT       : 20009
RHOST:PORT  : 127.0.0.1:20010
MTU         : 1500
~~~
🌞 **Wireshark !**
cf gnsws2.pcapng

🌞 **Configurez dnsmasq**
~~~
  dnf install -y dnsmasq
~~~
~~~
port=0
dhcp-range=10.1.1.210,10.1.1.250,255.255.255.0,12h
dhcp-authoritative
interface=enp0s3
~~~
~~~
sudo systemctl restart dnsmasq
~~~
🌞 **Test !**

~~~
PC2> dhcp -r
DDORA IP 10.1.1.249/24 GW 10.1.1.14


PC2> show ip all

NAME   IP/MASK              GATEWAY           MAC                DNS
PC2    10.1.1.249/24        10.1.1.14         00:50:79:66:68:04
~~~
🌞 **Now race !**

~~~
sudo systemctl start dhcpd
~~~
~~~
PC2> dhcp -r
DORA IP 10.1.1.16/24 GW 10.1.1.1

PC1> dhcp
DORA IP 10.1.1.16/24 GW 10.1.1.1

PC2> dhcp
DORA IP 10.1.1.249/24 GW 10.1.1.14

PC3> dhcp
DORA IP 10.1.1.15/24 GW 10.1.1.1
(Loser un peu le Rogue)
~~~
🌞 **Wireshark !**

cf race.pcapng

## 3. BONUS : DHCP starvation

Une attaque très débile et simple à mettre en place pour **DOS l'accès à un LAN** s'il n'y a pas de protections particulières. **C'est naze, mais c'est là** :d

Le principe est simple : **faire de multiples échanges DORA avec le serveur DHCP pour récupérer toutes les IP disponibles dans le réseau.**

On usurpe une adresse MAC (qu'elle existe ou non), on demande une adresse IP, on la récupère (merci). On répète l'opération avec une nouvelle fake adresse MAC, une nouvelle IP (merci). Etc. Jusqu'à épuiser toutes les adresses de la range.

Il existe des tools pour faire ça, vous pouvez aussi essayer (recommandé) de le **coder vous-mêmes avec Scapy** (une dinguerie cette lib) : on peut forger à peu près tout et n'importe quoi comme trame, et très facilement, avec Scapy.