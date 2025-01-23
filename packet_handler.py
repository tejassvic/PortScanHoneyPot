from datetime import datetime
from scapy.all import IP, TCP
from constants import BLOCK_DURATION, MAX_COUNT, TAUNT
from ip_handler import IPHandler
from logger import HoneypotLogger

TRACKER = {}
logger = HoneypotLogger()
ip_handler = IPHandler()

def packet_handler(packet):
    if TCP in packet and packet[TCP].flags == "S":
        source_ip = packet[IP].src
        destination_port = packet[TCP].dport

        print(f"Received SYN from {source_ip} on port {destination_port}")
        current_time = datetime.now()

        if source_ip not in TRACKER:
            TRACKER[source_ip] = {"count": 0, "timestamp": None}

        last_activity = TRACKER[source_ip]["timestamp"]
        if last_activity and current_time - last_activity > BLOCK_DURATION:
            TRACKER[source_ip] = {"count": 0, "timestamp": None}

        TRACKER[source_ip]["count"] += 1
        TRACKER[source_ip]["timestamp"] = current_time

        if TRACKER[source_ip]["count"] > MAX_COUNT:
            ip_handler.block_ip(source_ip)
            logger.log_attack(source_ip, destination_port, current_time, "Blocked for exceeding MAX_COUNT")
            return

        logger.log_attack(source_ip, destination_port, current_time)

        source_port = packet[TCP].sport
        response_packet = (
            IP(dst=source_ip, src=packet[IP].dst) /
            TCP(sport=destination_port, dport=source_port, flags="PA", seq=101, ack=packet[TCP].seq + 1) /
            Raw(load=TAUNT)
        )
        send(response_packet, verbose=0)
        print(f"Sent '{TAUNT}' packet to {source_ip} on port {destination_port}")
