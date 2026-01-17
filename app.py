import os
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
from flask_pymongo import PyMongo
import json
from bson.json_util import dumps
from datetime import datetime
from dotenv import load_dotenv
from threading import Lock

load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config['SECRET_KEY'] = 'secret!'

mongo = PyMongo(app)
socketio = SocketIO(app, cors_allowed_origins="*")

thread = None
thread_lock = Lock()

# Helper to serialize MongoDB documents
def serialize_doc(doc):
    if not doc:
        return None
    return json.loads(dumps(doc))

# Background Thread for Real-time Data
def background_thread():
    """Fetch latest sensor data and emit to clients."""
    while True:
        socketio.sleep(2)
        try:
            # Fetch latest reading
            latest_reading = mongo.db.readings.find_one(sort=[('timestamp', -1)])
            if latest_reading:
                socketio.emit('update_sensor_data', serialize_doc(latest_reading))
        except Exception as e:
            print(f"Error in background thread: {e}")

@socketio.on('connect')
def connect():
    global thread
    print('Client connected')
    
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hardware')
def hardware():
    hardwares = list(mongo.db.hardwares.find())
    return render_template('hardware.html', hardwares=hardwares)

@app.route('/logs')
def logs():
    # Basic pagination implementation
    page = int(request.args.get('page', 1))
    per_page = 20
    skip = (page - 1) * per_page
    
    total = mongo.db.readings.count_documents({})
    readings = list(mongo.db.readings.find().sort('timestamp', -1).skip(skip).limit(per_page))
    
    return render_template('logs.html', readings=readings, page=page, total=total, per_page=per_page)

@app.route('/reports')
def reports():
    return render_template('reports.html')

@app.route('/generate_report')
def generate_report():
    from weasyprint import HTML
    from datetime import timedelta

    # Calculate time range (last 24h)
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=24)

    # Fetch data
    query = {'timestamp': {'$gte': start_time, '$lte': end_time}}
    readings = list(mongo.db.readings.find(query))

    # Calculate Stats
    if not readings:
        return "No data available for report", 404

    co2_values = [r['sensors']['co2'] for r in readings if 'sensors' in r]
    pm25_values = [r['sensors']['pm25'] for r in readings if 'sensors' in r]
    temp_values = [r['sensors']['temp'] for r in readings if 'sensors' in r]
    hum_values = [r['sensors']['hum'] for r in readings if 'sensors' in r]

    stats = {
        'co2': {'min': min(co2_values) if co2_values else 0, 'max': max(co2_values) if co2_values else 0, 'avg': round(sum(co2_values)/len(co2_values), 2) if co2_values else 0},
        'pm25': {'min': min(pm25_values) if pm25_values else 0, 'max': max(pm25_values) if pm25_values else 0, 'avg': round(sum(pm25_values)/len(pm25_values), 2) if pm25_values else 0},
        'temp': {'min': min(temp_values) if temp_values else 0, 'max': max(temp_values) if temp_values else 0, 'avg': round(sum(temp_values)/len(temp_values), 2) if temp_values else 0},
        'hum': {'min': min(hum_values) if hum_values else 0, 'max': max(hum_values) if hum_values else 0, 'avg': round(sum(hum_values)/len(hum_values), 2) if hum_values else 0}
    }

    # Count Ventilation Triggers
    ventilation_count = sum(1 for r in readings if r.get('actuators', {}).get('ventilation') == 'ON')

    # Incidents (Polluted)
    incidents = [r for r in readings if r.get('analysis', {}).get('prediction') == 'Polluted']
    incidents_count = len(incidents)

    # Health Score (Simple logic: 100 - incidents)
    health_score = max(0, 100 - (incidents_count * 2))

    # Render HTML
    html = render_template('report_pdf.html', 
                           generated_at=end_time.strftime('%Y-%m-%d %H:%M:%S'),
                           stats=stats,
                           ventilation_count=ventilation_count,
                           incidents=incidents,
                           incidents_count=incidents_count,
                           health_score=health_score)
    
    # Generate PDF
    pdf = HTML(string=html).write_pdf()

    # Return PDF
    from flask import make_response
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=report.pdf'
    return response

if __name__ == '__main__':
    socketio.start_background_task(background_thread)
    socketio.run(app, debug=True, port=5000)