import json
from datetime import datetime

class HoneypotLogger:
    def __init__(self, log_file="honeypot_logs.json"):
        self.log_file = log_file

    def log_attack(self, source_ip, destination_port, timestamp, additional_info=None):
        log_entry = {
            "source_ip": source_ip,
            "destination_port": destination_port,
            "timestamp": timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            "additional_info": additional_info,
        }
        with open(self.log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
        print(f"Logged attack from {source_ip} on port {destination_port}")
