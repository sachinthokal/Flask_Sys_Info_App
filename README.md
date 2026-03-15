# 🚀 SYS-INSIGHTS DASHBOARD

A simple and premium web-based dashboard built with **Flask** and **Docker** to monitor real-time system metrics like CPU usage, RAM usage, and OS information.

## 🚀 Features

- **Real-time Monitoring:** View CPU and RAM usage without manual refreshing.
- **System Info:** Displays Hostname, IP Address, Boot Time, and Architecture.
- **Dockerized:** Fully containerized for easy deployment.
- **Premium UI:** Modern Dark Mode interface.

## 🛠️ Tech Stack

- **Backend:** Python 3.11, Flask
- **Metrics:** psutils library
- **Frontend:** HTML5, CSS3 (Grid & Flexbox), JavaScript
- **Deployment:** Docker, Docker Compose, Gunicorn

## 📋 Prerequisites

Before running this project, ensure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## 🏃 How to Run

### 1. Clone the repository

```bash
git clone https://github.com/sachinthokal/Flask_Sys_Info_App.git
cd Flask_Sys_Info_App
docker compose up -d --build
```

OR 🐳 Docker Hub Image
> You can also pull the pre-built image directly from Docker Hub:

```bash
docker pull sachinthokal/flask-sys-info-app:v1.0.0
```

## 👤 Author

> Sachin Thokal DevOps Engineer | Pune, India
