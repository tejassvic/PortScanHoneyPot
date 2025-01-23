from datetime import datetime

def auto_unblocking(tasks, ip_handler):
    current_time = datetime.now()
    for task in list(tasks):
        if current_time >= task["unblock_time"]:
            ip_handler.unblock_ip(task["ip"])
            tasks.remove(task)
            print(f"Unblocked IP: {task['ip']} at {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
