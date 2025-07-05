from flask import Flask, render_template, request, redirect, url_for, session, flash
from scripts.Software import get_services, get_installed_programs
from scripts.Logs import get_system_logs, get_security_logs, get_application_logs
from scripts.Network import get_port_info, get_network_info
from scripts.System import get_cpu_usage, get_gpu_usage, donutChart, get_connected_device, get_system_info
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import os
import threading
import pythoncom
import asyncio
import websockets
import json
import webbrowser
from dotenv import load_dotenv
from sqlalchemy.exc import OperationalError

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db = SQLAlchemy(app)
server_url = os.getenv('SERVER_URL')
port = int(os.getenv('PORT'))

# Initialize COM for WMI usage
pythoncom.CoInitialize()

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_online = db.Column(db.Boolean, default=False)

# WebSocket connection management
active_websockets = {}

def start_websocket_task(user_id):
    def websocket_task():
        pythoncom.CoInitialize()
        asyncio.run(send_data_to_server(user_id))
        pythoncom.CoUninitialize()

    thread = threading.Thread(target=websocket_task, daemon=True)
    thread.start()

async def send_data_to_server(user_id):
    uri = f"ws://{server_url}:{port}"
    try:
        async with websockets.connect(uri) as websocket:
            active_websockets[user_id] = websocket  # Store the websocket connection
            await websocket.send(str(user_id))
            while True:
                data = {
                    "system": {
                        "cpu_usage": get_cpu_usage(),
                        "gpu_usage": get_gpu_usage(),
                        "info_boxes": get_system_info(),
                        "connected_device": get_connected_device(),
                        "donut_chart": donutChart()
                    },
                    "logs": {
                        "system_logs": get_system_logs(),
                        "security_logs": get_security_logs(),
                        "application_logs": get_application_logs()
                    },
                    "network": {
                        "port_info": get_port_info(),
                        "network_info": get_network_info()
                    },
                    "applications": {
                        "programs": get_installed_programs(),
                        "services": get_services()
                    }
                }
                await websocket.send(json.dumps(data))
                await asyncio.sleep(0.1)
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        # Remove the websocket connection when done
        if user_id in active_websockets:
            del active_websockets[user_id]

# Decorator for login required pages
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('You must login to access this page')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Decorator for admin required pages
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('You must login to access this page')
            return redirect(url_for('login'))
        try:
            user = db.session.get(User, session['user_id'])  # Updated to use db.session.get()
        except OperationalError as e:
            db.session.rollback()
            flash('Database connection error. Please try again.')
            return redirect(url_for('login'))
        if not user or not user.is_admin:
            flash('You do not have permission to access this page')
            return redirect(url_for('system', user_id=session['user_id']))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            user.is_online = True
            db.session.commit()
            start_websocket_task(user.id)

            if user.is_admin:
                return redirect(url_for('admin'))
            return redirect(url_for('system', user_id=user.id))

        flash('Invalid email or password')
        return redirect(url_for('login'))

    return render_template("Login.html")

@app.route('/logout')
def logout():
    if 'user_id' in session:
        user_id = session['user_id']
        try:
            user = db.session.get(User, user_id)  # Updated to use db.session.get()
        except OperationalError as e:
            db.session.rollback()
            flash('Database connection error. Please try again.')
            return redirect(url_for('login'))
        if user:
            user.is_online = False
            db.session.commit()
        session.pop('user_id', None)

        # Close the WebSocket connection if it exists
        if user_id in active_websockets:
            websocket = active_websockets[user_id]
            # Use a separate function to close the websocket
            asyncio.run(close_websocket(websocket))  # Close the WebSocket connection

    return redirect(url_for('login'))

async def close_websocket(websocket):
    try:
        await websocket.close()  # Close the WebSocket connection
    except Exception as e:
        print(f"Error closing websocket: {e}")

@app.route('/admin')
@admin_required
def admin():
    users = User.query.all()
    return render_template("Admin.html", users=users)

@app.route("/system/<int:user_id>")
@login_required
def system(user_id):
    if not check_user_access(user_id):
        return redirect(url_for('system', user_id=session['user_id']))
    return render_template("System.html", server_url=server_url, port=port)

@app.route("/software/<int:user_id>")
@login_required
def software(user_id):
    if not check_user_access(user_id):
        return redirect(url_for('software', user_id=session['user_id']))
    return render_template("Software.html",server_url=server_url,port=port)

@app.route("/network/<int:user_id>")
@login_required
def network(user_id):
    if not check_user_access(user_id):
        return redirect(url_for('network', user_id=session['user_id']))
    return render_template("Network.html",server_url=server_url,port=port)

@app.route("/logs/<int:user_id>")
@login_required
def logs(user_id):
    if not check_user_access(user_id):
        return redirect(url_for('logs', user_id=session['user_id']))
    return render_template("Logs.html",server_url=server_url,port=port)

def check_user_access(user_id):
    try:
        user = db.session.get(User, session['user_id'])  # Updated to use db.session.get()
    except OperationalError as e:
        db.session.rollback()
        flash('Database connection error. Please try again.')
        return False
    return user and (user.is_admin or user.id == user_id)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    # Automatically open the default web browser to the login page
    webbrowser.open("http://127.0.0.1:5000/")
    app.run(debug=True, use_reloader=False)