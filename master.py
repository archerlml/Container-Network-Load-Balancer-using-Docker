import docker
import queue
import os
import time
import threading
from flask import Flask, jsonify

# Number of containers in the beginning.
initial_num = 3

# Number of containers that we have at most in the system.
upper_limit = 100

# Time interval which the daemon thread will use to check the idle queue 
# and perform the automatic scale down. 
sleep_time = 10

# Using the synchronize queue to include the busy and idle containers.
busy_queue = queue.Queue(maxsize = upper_limit)
idle_queue = queue.Queue(maxsize = upper_limit)

# Using the docker-py to communicate with docker
client = docker.from_env()

# Using the Flask framework to start the client-server architecture
app = Flask(__name__)

# For the testing purpose
@app.route('/')
def Welcome():
    return 'Welcome to our CMPE 283 project!'

# For the testing purpose
@app.route('/myapp')
def WelcomeToMyapp():
    return 'Welcome to our CMPE 283 project again!'

# To handle the GET HTTP request
@app.route('/api/training', methods=['GET'])
def GetTraining():
    if idle_queue.empty() and busy_queue.qsize() < upper_limit:
        ctr = client.create_container(
            image='model-training', command='python3 slave.py a.txt b.txt c.txt')
    else:
        ctr = idle_queue.get()
    busy_queue.put(ctr)
    client.start(ctr)
    return "True"

# To get the result in the MySQL database which is the future work.
@app.route('/api/result')
def GetResult():
    return "This part is left for furture work."

# Daemon thread, always runing
def auto_scale_down():
    while True:
        time.sleep(sleep_time)
        while busy_queue.qsize() > 0:
            ctr = busy_queue.get()
            state = client.wait(ctr)
            if state == -1:
                continue
            log = client.logs(ctr)
            log_str = bytes.decode(log)
            print(log_str)
            if idle_queue.qsize() < initial_num:
                idle_queue.put(ctr)
            else:
                flag = True
                count = 0
                while flag:
                    try:
                        client.remove_container(ctr)
                        flag = False
                    except:
                        if count > 3:
                            break
                        time.sleep(1)
                        count += 1      

# Set the listening port
port = os.getenv('PORT', '5000')

# Main function
if __name__ == "__main__":
    for x in range(0, initial_num):
        idle_queue.put(client.create_container(
            image='model-training', command='python3 slave.py a.txt b.txt c.txt'))
    t = threading.Thread(target = auto_scale_down)
    t.start()
    app.run(host='0.0.0.0', port = int(port))