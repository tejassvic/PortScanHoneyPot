from scapy.all import sniff

class SnifferHandler:
    def __init__(self):
        self.tasks = []

    def start_sniffing(self, packet_handler):
        print("Started sniffing...")
        sniff(filter="tcp", prn=packet_handler)
