import time
import os

LOG_FILE = "mock_auth.log"

ATTACK_LOGS = [
    "Mar 19 20:23:10 server sshd[12034]: Failed password for invalid user admin from 192.168.1.55 port 45123 ssh2",
    "Mar 19 20:23:11 server sshd[12035]: Failed password for root from 192.168.1.55 port 45124 ssh2",
    "Mar 19 20:23:12 server sshd[12036]: Failed password for root from 192.168.1.55 port 45125 ssh2",
    "Mar 19 20:23:13 server sshd[12037]: Failed password for root from 192.168.1.55 port 45126 ssh2",
    # The 5th log triggers our daemon's rule!
    "Mar 19 20:23:14 server sshd[12038]: Failed password for root from 192.168.1.55 port 45127 ssh2",
]

def simulate():
    print("Initiating simulated SSH brute force in 3 seconds...")
    time.sleep(3)
    
    with open(LOG_FILE, "a") as f:
        for log in ATTACK_LOGS:
            print(f"Injecting: {log}")
            f.write(log + "\n")
            f.flush()
            # 0.5 sec delay makes the "rapid fire" visible in Window 2
            time.sleep(0.5) 

if __name__ == "__main__":
    simulate()
