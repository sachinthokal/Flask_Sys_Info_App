import os
import socket
import platform
import psutil
import subprocess  # Required to run CLI commands
import logging     # Import standard logging module
from datetime import datetime
from flask import Flask, render_template, jsonify  # Added jsonify for AJAX API endpoint

app = Flask(__name__, static_folder='assets', static_url_path='/assets')

# ==============================================================================
# 🔥 DEBUGGING & LOGGING CONFIGURATION
# ==============================================================================
import logging
from logging.handlers import RotatingFileHandler  # Navin import add kar

logger = logging.getLogger()

if(os.getenv('DEBUG') == 'True'):
    logging.debug("Debug mode enabled. Detailed logs will be recorded.")
    logger.setLevel(logging.DEBUG)
else:
    logging.info("Debug mode disabled. Only warnings and errors will be recorded.")
    logger.setLevel(logging.INFO)   

# Formatter set kar
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

# 1. Rotating File Handler Setup (Max 5MB per file, maximum 3 backup files)
# 5 * 1024 * 1024 bytes = 5 Megabytes
file_handler = RotatingFileHandler("devopsvaultx.log", maxBytes=5*1024*1024, backupCount=3)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Helper function to safely check tool versions (Docker & Terraform)
def get_tool_version(command):
    try:
        logging.info(f"Checking subsystem version for command: {' '.join(command)}")
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        output = result.stdout.strip().split('\n')[0]
        
        if "Docker version" in output:
            return output.replace("Docker version ", "")
            
        return output
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logging.warning(f"Tool check failed for {' '.join(command)}. Exception: {str(e)}")
        return "Not Installed"

# Helper function to auto-convert bytes to GB or TB dynamically
def format_size(bytes_value):
    gb_value = bytes_value / (1024**3)
    if gb_value >= 1024:
        return f"{round(gb_value / 1024, 2)} TB"
    return f"{round(gb_value, 2)} GB"

def get_system_info():
    logging.info("Gathering hardware telemetry and environment specs...")
    
    # Optimized interval for non-blocking asynchronous AJAX polling fetches
    cpu_usage = psutil.cpu_percent(interval=0.1)
    
    # RAM Calculations
    vm = psutil.virtual_memory()
    ram_total = f"{round(vm.total / (1024**3), 2)} GB"
    ram_used = f"{round(vm.used / (1024**3), 2)} GB"
    
    # Disk Calculations
    disk_path = '/' if platform.system() != 'Windows' else 'C:\\'
    try:
        disk = psutil.disk_usage(disk_path)
        disk_percent = disk.percent
        disk_details = f"{format_size(disk.used)} / {format_size(disk.total)}"
    except Exception as e:
        logging.error(f"Failed to fetch disk specs: {str(e)}")
        disk_percent = 0
        disk_details = "N/A"

    hostname = socket.gethostname()
    try:
        ip_address = socket.gethostbyname(hostname)
    except Exception as e:
        logging.warning(f"Hostname resolution failed: {str(e)}")
        ip_address = "127.0.0.1"

    # Fetch Open Listening Ports
    listening_ports = set()
    try:
        for conn in psutil.net_connections(kind='inet'):
            if conn.status == 'LISTEN':
                listening_ports.add(str(conn.laddr.port))
    except Exception as e:
        logging.warning(f"Connections parsing error: {str(e)}")
        pass
    ports_string = ", ".join(sorted(listening_ports)) if listening_ports else "None"

    # 1. Fetch DevOps Tools Versions
    docker_ver = get_tool_version(['docker', '--version'])
    terraform_ver = get_tool_version(['terraform', '--version'])

    # 3. Fetch Kubernetes kubectl Version
    try:
        k8s_res = subprocess.run(['kubectl', 'version', '--client', '--output=yaml'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=2)
        if k8s_res.returncode == 0:
            k8s_ver = "Installed"
            for line in k8s_res.stdout.split('\n'):
                if "gitVersion:" in line:
                    k8s_ver = line.split("gitVersion:")[1].strip().replace('"', '')
                    break
        else:
            k8s_ver = "Not Installed"
    except Exception as e:
        logging.warning(f"Kubectl detection timeout/error: {str(e)}")
        k8s_ver = "Not Installed"

    # 4. Fetch Python Version
    try:
        python_ver = subprocess.run(['python', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        python_ver = python_ver.stdout.strip() if python_ver.stdout else python_ver.stderr.strip()  
    except Exception as e:
        logging.warning(f"Python check failed: {str(e)}")
        python_ver = "Not Installed"

    # 5. Fetch Git Version
    git_ver = get_tool_version(['git', '--version'])

    # Structured Payload for index.html
    info = {
        "CPU Usage": f"{cpu_usage}%",
        "RAM Usage": f"{vm.percent}%",
        "Disk Usage": f"{disk_percent}%",

        "RAM Allocation": f"{ram_used} / {ram_total}",
        "Disk Allocation": disk_details,

        "Hostname": hostname,
        "Private IP": ip_address,
        "Active Listening Ports": ports_string,

        # DevOps Tools
        "Docker Version": docker_ver,
        "Kubernetes CLI": k8s_ver,
        "Terraform Version": terraform_ver,
        "Python Version": python_ver,
        "Git Version": git_ver,

        # System Specs
        "Operating System": f"{platform.system()} {platform.release()}",
        "OS Kernel": platform.version() if platform.system() == 'Windows' else os.uname().release if hasattr(os, 'uname') else platform.release(),
        "Architecture": platform.machine(),
        "Processor Cores": f"{psutil.cpu_count(logical=False)} Physical / {psutil.cpu_count(logical=True)} Threads",
        "System Boot Time": datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S'),
        "Build": datetime.now().strftime('%Y.%m')
    }
    logging.info("Telemetry data successfully compiled.")
    return info

# Route 1: Initial Page Render
@app.route('/')
def home():
    logging.info("--- HTTP GET / Initial Home View Requested ---")
    data = get_system_info()
    return render_template('index.html', info=data)

# Route 2: Real-time Live Metrics Endpoint (Asynchronous Polling target)
@app.route('/api/metrics')
def get_metrics():
    # AJAX call background query logging
    logging.info("Gathering real-time system information...")
    data = get_system_info()
    logging.debug(f"Data fetch initiated for /api/metrics endpoint: {data}")
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=os.getenv('DEBUG', 'False'))