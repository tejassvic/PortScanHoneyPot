from scapy.all import *
from datetime import datetime, timedelta
from collections import defaultdict
import subprocess

TRACKER = defaultdict(lambda: {"count": 0, "timestamp": None})
BLOCK_DURATION = timedelta(minutes=5) # Timeout for dropping all SYN on all ports
MAX_COUNT = 3 # Attemps count


class ipHandler:
    def __init__(self):
        pass

    def isBlocked(self, ip):
        resp = subprocess.run(["sudo", "iptables", "-L", "-n"], stdout=subprocess.PIPE, text=True)
        return ip in resp.stdout

    def blockIp(self, ip):
        print(f"Blocking IP: {ip}")

        if self.isBlocked(ip):
            return True

        try:
            subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"], check=True)
        except Exception as e:
            print(f"Error Blocking IP {ip}: {e}")

    def unblockIp(self, ip):
        print(f"Unblocking IP: {ip}")

        if not self.isBlocked(ip):
            return True

        try:
            subprocess.run(["sudo", "iptables", "-D", "INPUT", "-s", ip, "-j", "DROP"], check=True)
        except Exception as e:
            print(f"Error unblocking IP {ip}: {e}")


class snifferHandler:
    def __init__(self):
        self.tasks = []

    def start(self):
        print(f"Started Sniffing")
        sniff(filter="tcp", prn=packetHandler)


ip_handler = ipHandler()
sniffer = snifferHandler()


def packetHandler(packet):
    if TCP in packet and packet[TCP].flags == "S":
        sourceIp = packet[IP].src
        port = packet[TCP].dport
        sourcePort = packet[TCP].sport

        print(f"Received Packet with IP: {sourceIp}")

        currentTime = datetime.now()
        if TRACKER[sourceIp]["timestamp"] and currentTime - TRACKER[sourceIp]["timestamp"] > BLOCK_DURATION:
            TRACKER[sourceIp] = {"count": 0, "timestamp": None}

        TRACKER[sourceIp]["count"] += 1
        TRACKER[sourceIp]["timestamp"] = currentTime

        if TRACKER[sourceIp]["count"] > MAX_COUNT:
            ip_handler.blockIp(sourceIp)
            unblock_time = datetime.now() + BLOCK_DURATION
            print(f"IP {sourceIp} will be unblocked at {unblock_time.strftime('%Y-%m-%d %H:%M:%S')}")
            sniffer.tasks.append({"ip": sourceIp, "unblock_time": unblock_time})
            return

        syn_ack = (
            IP(dst=sourceIp, src=packet[IP].dst) /
            TCP(sport=port, dport=sourcePort, flags="SA", seq=100, ack=packet[TCP].seq + 1)
        )
        send(syn_ack, verbose=0)
        print(f"Sent SYN-ACK to {sourceIp} on port {port}")

        data_packet = (
            IP(dst=sourceIp, src=packet[IP].dst) /
            TCP(sport=port, dport=sourcePort, flags="PA", seq=101, ack=packet[TCP].seq + 1) /
            Raw(load="GET A LIFE!") # Taunt
        )
        send(data_packet, verbose=0)
        print(f"Sent data packet with message 'GET A LIFE!' to {sourceIp} on port {port}")


def autoUnblocking():
    currentTime = datetime.now()
    for task in list(sniffer.tasks):
        if currentTime >= task["unblock_time"]:
            ip_handler.unblockIp(task["ip"])
            sniffer.tasks.remove(task)


if __name__ == "__main__":
    import threading

    sniffer = snifferHandler()
    sniffer_thread = threading.Thread(target=sniffer.start, daemon=True)
    sniffer_thread.start()

    while True:
        autoUnblocking()
