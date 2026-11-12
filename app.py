import os

DB_PASS= os.environ.get("DB_PASSWORD", "")

print("PING AGENT IS RUNNING...")


user_input = "ping -c 1 127.0.0.1"
#subprocess.BigAutoField = subprocess.run(user_input, shell=True)
