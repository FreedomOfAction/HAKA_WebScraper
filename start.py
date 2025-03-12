import subprocess
import time
import webbrowser
import os
import psutil

# Define project directory
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

# Function to check if Redis is running
def is_redis_running():
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        if "redis-server" in proc.info['name']:
            return True
    return False

# Start Redis if not running
if not is_redis_running():
    print("Starting Redis...")
    redis_process = subprocess.Popen(["C:\\Program Files\\Redis\\redis-server.exe"])
    time.sleep(3)  # Give Redis time to start

# Start Celery Worker
print("Starting Celery Worker...")
celery_process = subprocess.Popen(["python", "-m", "celery", "-A", "tasks.worker", "worker", "--loglevel=info"], cwd=PROJECT_DIR)

# Wait a bit before starting Flask
time.sleep(5)

# Start Flask App
print("Starting Flask Server...")
flask_process = subprocess.Popen(["python", "app.py"], cwd=PROJECT_DIR)

# Open the web interface in the default browser
time.sleep(2)
webbrowser.open("http://127.0.0.1:5000")

# Keep script running to prevent exit
try:
    flask_process.wait()
except KeyboardInterrupt:
    print("\nStopping everything...")
    celery_process.terminate()
    flask_process.terminate()
