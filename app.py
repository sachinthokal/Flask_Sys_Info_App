import os
import socket
import platform
import psutil
from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__)

def get_system_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    
    hostname = socket.gethostname()
    try:
        ip_address = socket.gethostbyname(hostname)
    except:
        ip_address = "127.0.0.1"

    info = {
        "User": "Sachin Thokal",
        "System Status": "🟢 Healthy",
        "CPU Usage": f"{cpu_usage}%",
        "RAM Usage": f"{psutil.virtual_memory().percent}%",
        "Disk Used": f"{psutil.disk_usage('/').percent}%",
        "Boot Time": f"{datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')}",
        "Hostname": hostname,
        "IP Address": ip_address,
        "Architecture": platform.machine(),
        "Python": platform.python_version(),
        "Docker": "Yes" if os.path.exists('/.dockerenv') else "No"
    }
    return info

@app.route('/')
def home():
    data = get_system_info()
    return render_template('index.html', info=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)