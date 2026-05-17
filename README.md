# 🚀 DevOpsVaultX - Enterprise System Console & Telemetry Dashboard

DevOpsVaultX is a premium, high-performance, web-based infrastructure observability dashboard built with **Flask** and **Docker**. It provides real-time, non-blocking telemetry data tracking core hardware specs (CPU, RAM, Disk) alongside instant DevOps toolchain environment version mapping.

---

## 💡 Key Upgrades & Features

- **⚡ Zero-Lag Asynchronous Polling:** Replaced full-page hard refreshes with modern JS Fetch API asynchronous background polling every 3 seconds for seamless UI orchestration.
- **🛡️ Intelligent System Health Engine:** Dynamic state processing flags the target node's status instantly between `🟢 HEALTHY`, `🟠 WARNING`, and `🔴 CRITICAL` based on metric resource thresholds.
- **⚙️ Integrated DevOps Toolchain Audit:** Automated native sub-process scanning loops track operational versions of Docker, Kubernetes (kubectl), Terraform, Python, and Git.
- **🪵 Production-Grade Log Rotation:** Integrated Python's `RotatingFileHandler` engine restricting runtime session logging footprints to `5MB` with a maximum 3-file backup fallback to guarantee zero disk exhaustion.
- **🎨 Elite Glassmorphism UI:** Tailored with professional UI responsive grids, localized hardware allocation specifications, and fluid hardware-accelerated animations.

---

## 🛠️ Tech Stack

- **Core Backend:** Python 3.11+, Flask Web Engine
- **Telemetry Processing:** `psutil`, `platform`, `socket` subsystem modules
- **Logging Pipeline:** Python Standard Logging with Automated Log Rotation
- **Advanced UI Front:** Adaptive HTML5, Modern CSS3 Core Variables, Vanilla JS (Async/Await Fetch)
- **Deployment Chain:** Docker, Docker Compose, WSGI Gunicorn Production Servers

---

## 📋 Prerequisites

Ensure you have the following engineering tools set up on your host machine:
- [Docker Engine](https://docs.docker.com/get-docker/) (v20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/)

---

## 🏃 How To Run & Deploy

### 1. Bare-Metal Local Development Setup
```bash
# Clone the system environment
git clone [https://github.com/sachinthokal/Flask_Sys_Info_App.git](https://github.com/sachinthokal/Flask_Sys_Info_App.git)
cd Flask_Sys_Info_App

# Create and trigger virtual workspace environment
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install component dependencies
pip install -r requirements.txt

# Run server with real-time debug variable tracing enabled
DEBUG=True python3 app.py