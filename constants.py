from datetime import timedelta

BLOCK_DURATION = timedelta(minutes=5)  # Timeout for blocking IPs
MAX_COUNT = 3  # Maximum allowed SYN attempts before blocking
LOG_FILE = "honeypot_logs.json"  # Log file path
TAUNT = "GET A LIFE!"  # Taunt for trolling