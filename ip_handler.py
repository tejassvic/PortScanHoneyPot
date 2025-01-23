import subprocess

class IPHandler:
    def is_blocked(self, ip):
        resp = subprocess.run(["sudo", "iptables", "-L", "-n"], stdout=subprocess.PIPE, text=True)
        return ip in resp.stdout

    def block_ip(self, ip):
        print(f"Blocking IP: {ip}")
        if self.is_blocked(ip):
            return True

        try:
            subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"], check=True)
        except Exception as e:
            print(f"Error blocking IP {ip}: {e}")

    def unblock_ip(self, ip):
        print(f"Unblocking IP: {ip}")
        if not self.is_blocked(ip):
            return True

        try:
            subprocess.run(["sudo", "iptables", "-D", "INPUT", "-s", ip, "-j", "DROP"], check=True)
        except Exception as e:
            print(f"Error unblocking IP {ip}: {e}")
