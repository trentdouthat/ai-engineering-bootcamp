# 1. Define a list of servers (simulated data)
servers = [
    {"hostname": "web-01", "status": "online", "load": 99},
    {"hostname": "db-01",  "status": "online", "load": 92},
    {"hostname": "app-01", "status": "offline", "load": 0},
    {"hostname": "web-02", "status": "online", "load": 15},
    {"hostname": "cache-01","status": "online", "load": 88}
]

print("--- STARTING SYSTEM HEALTH CHECK ---")

# 2. Loop through each server in the list
for server in servers:
    # 3. Check for Offline servers
    if server["status"] == "offline":
        print(f"CRITICAL ALERT: {server['hostname']} is responding offline!")
    
    # 4. Check for High Load (greater than 90%)
    elif server["load"] > 90:
        print(f"WARNING: {server['hostname']} is under heavy load ({server['load']}%)")
    
    # 5. Everything else is fine
    else:
        print(f"OK: {server['hostname']} is healthy.")

print("--- CHECK COMPLETE ---")