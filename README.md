
<div align="center">
  <h1>⚙️ QuickDash — Real-Time Windows Monitoring Dashboard</h1>
</div>

<p align="center">
  <em>A real-time system monitoring dashboard for Windows, built with Flask, WebSocket, and system-level data collectors.</em>
</p>

---

## 📌 Overview

**QuickDash** is a comprehensive real-time system monitoring application developed in Python using **Flask**, **WebSocket**, and system libraries like `psutil`, `wmi`, and `GPUtil`. It offers a web-based dashboard to monitor CPU, GPU, services, installed applications, logs, ports, and more.

Key features include:

- 🖥️ Real-time system statistics (CPU, GPU, memory, devices)  
- 🔌 WebSocket-powered live updates  
- 📡 Network and port info monitoring  
- 🛠️ Installed programs and running services  
- 📝 Windows Event Log integration (system, security, application logs)  
- 👥 User authentication system with admin panel  
- 🌐 Responsive Flask web interface with session-based login  

---

## 🧰 Requirements

- Python 3.x  
- Windows OS  
- PostgreSQL database  
- Tesseract (optional, if OCR is required)

To install required Python packages:

```bash
pip install -r requirements.txt
```

---

## 🛠️ Environment Setup

Before running the application, create a `.env` file in the root directory and add the following keys with **your own values**:

```env
DATABASE_URL='your_postgresql_connection_string_here'
SERVER_URL='your_websocket_server_ip_here'
PORT='your_websocket_port_here'
```

> 🔐 **Important:** Do not upload your `.env` file to version control (GitHub). Ensure your `.gitignore` file includes `.env`.

---

## 🚀 Installation & Run

1. **Clone the repository**:

```bash
git clone https://github.com/your-username/quickdash.git
cd quickdash
```

2. **(Optional)** Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate   # On Windows
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

4. **Run the application**:

```bash
python app.py
```

---

## 📁 Project Structure

```
quickdash/
│
├── scripts/                    # System, logs, network-related modules
├── static/                     # CSS, JS, icons
├── templates/                  # HTML templates (Login, Admin, Dashboard)
├── app.py                      # Main Flask app
├── server.py                   # WebSocket server (optional)
├── quickdash.ico               # Application icon
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (NOT COMMITTED)
├── .gitignore                  # Git ignored files
└── README.md                   # Documentation
```

---

## 🔐 User Roles

- **Admin users** can view all dashboards and manage users via the admin panel.  
- **Regular users** can only access their own system dashboard.  

---

## ✨ Features

- ✅ Real-time system updates via WebSocket  
- ✅ CPU, GPU, RAM, disk, device and service monitoring  
- ✅ Event log integration (System, Security, Application)  
- ✅ PostgreSQL-backed authentication  
- ✅ Admin panel  
- ✅ Simple and functional web interface  

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 🙋‍♂️ Contributing

Pull requests and suggestions are welcome! Fork the repository and feel free to submit improvements.

---

## 📬 Contact

| Platform | Info |
|----------|------|
| 📧 Email | [batuhanisiklar0@gmail.com](mailto:batuhanisiklar0@gmail.com) |
| 💼 LinkedIn | [Batuhan Işıklar](https://www.linkedin.com/in/batuhanisiklar/) |

---

> Made with ⚙️ and 💻 by Batuhan Işıklar
