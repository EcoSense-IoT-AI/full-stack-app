# AirGuard - Premium IoT Dashboard

AirGuard is a professional, production-ready IoT Dashboard application built with Python Flask and a modern, premium frontend. It monitors Air Quality sensors and Actuators in real-time, providing live updates, hardware monitoring, data logs, and PDF reports.

![Dashboard Preview](static/img/dashboard_preview.png) *Note: Add a screenshot here*

## 🚀 Features

*   **Real-time Monitoring**: Live updates of CO2, PM2.5, Temperature, and Humidity using Socket.IO.
*   **Premium UI**: Modern Dark Mode with Glassmorphism, Neon Accents, and smooth animations.
*   **Interactive Charts**: Dynamic Chart.js visualizations for Air Quality and Comfort trends.
*   **Hardware Status**: "Cyberpunk" style status cards for monitoring sensor and actuator health.
*   **Data Logs**: Searchable and sortable history of sensor readings.
*   **PDF Reports**: Generate comprehensive daily reports with statistics and incident logs.
*   **Responsive Design**: Fully responsive layout with a collapsible sidebar.

## 🛠️ Tech Stack

*   **Backend**: Python, Flask, Flask-SocketIO, Flask-PyMongo, WeasyPrint
*   **Database**: MongoDB Atlas
*   **Frontend**: HTML5, CSS3 (Custom Premium Theme), Bootstrap 5, JavaScript, Chart.js, DataTables.js

## 📦 Installation

1.  **Clone the repository**
    ```bash
    git clone <repository-url>
    cd flask-app
    ```

2.  **Create a virtual environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables**
    Create a `.env` file in the root directory and add your MongoDB connection string:
    ```env
    MONGO_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/test?appName=Cluster0
    ```

5.  **Run the Application**
    ```bash
    python app.py
    ```
    The application will be available at `http://localhost:5000`.

## 📂 Project Structure

```
flask-app/
├── app.py              # Main Flask Application & SocketIO Logic
├── requirements.txt    # Python Dependencies
├── .env                # Environment Variables (Not committed)
├── .gitignore          # Git Ignore Rules
├── static/
│   ├── css/
│   │   └── style.css   # Premium Custom Styles
│   └── js/
│       └── main.js     # Global JavaScript
└── templates/
    ├── base.html       # Base Template with Sidebar & Navbar
    ├── index.html      # Real-time Dashboard
    ├── hardware.html   # Hardware Status Monitor
    ├── logs.html       # Data Logs Table
    ├── reports.html    # Report Generation Page
    └── report_pdf.html # PDF Report Template
```

## 📝 License

This project is licensed under the MIT License.
