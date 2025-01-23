import threading
from sniffer_handler import SnifferHandler
from packet_handler import packet_handler
from auto_unblocker import auto_unblocking
from ip_handler import IPHandler

if __name__ == "__main__":
    sniffer = SnifferHandler()
    ip_handler = IPHandler()

    sniffer_thread = threading.Thread(target=sniffer.start_sniffing, args=(packet_handler,), daemon=True)
    sniffer_thread.start()

    print("Honeypot is running...")
    while True:
        auto_unblocking(sniffer.tasks, ip_handler)
