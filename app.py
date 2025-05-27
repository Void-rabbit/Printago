print("INFO: app.py was imported") # Added print statement

print("INFO: app.py was imported") # Added print statement

print("INFO: app.py was imported") # Added print statement

print("INFO: app.py was imported") # Added print statement

print("INFO: app.py was imported") # Added print statement

print("INFO: app.py was imported") # Added print statement

print("INFO: app.py was imported") # Added print statement

print("INFO: app.py was imported") # Added print statement

print("INFO: app.py was imported") # Added print statement

print("INFO: app.py was imported") # Added print statement

print("INFO: app.py was imported") # Added print statement

print("INFO: app.py was imported") # Added print statement

print("INFO: app.py was imported") # Added print statement

print("INFO: app.py was imported") # Added print statement

print("INFO: app.py was imported") # Added print statement

print("INFO: app.py was imported") # Added print statement

print("INFO: app.py was imported") # Added print statement

print("INFO: app.py was imported") # Added print statement

print("INFO: app.py was imported") # Added print statement

print("INFO: app.py was imported") # Added print statement

print("INFO: app.py was imported") # Added print statement

print("INFO: app.py was imported") # Added print statement

print("INFO: app.py was imported") # Added print statement

print("INFO: app.py was imported") # Added print statement

print("INFO: app.py was imported") # Added print statement

print("INFO: app.py was imported") # Added print statement

print("INFO: app.py was imported") # Added print statement

print("INFO: app.py was imported") # Added print statement

print("INFO: app.py was imported") # Added print statement

print("INFO: app.py was imported") # Added print statement

print("INFO: app.py was imported") # Added print statement

print("INFO: app.py was imported") # Added print statement

print("INFO: app.py was imported") # Added print statement

print("INFO: app.py was imported") # Added print statement

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from functools import wraps
import json
import bcrypt
import uuid
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'super secret key'  # Needed for flashing messages

USERS_FILE = 'users.json'
PARTS_FILE = 'parts.json'
PRINT_JOBS_FILE = 'print_jobs.json'
PRINTERS_FILE = 'printers.json'

CONFIG_API_KEY = "your_secret_api_key" # TODO: Move to config file or env var

# API Key Decorator
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.headers.get('X-API-Key') and request.headers.get('X-API-Key') == CONFIG_API_KEY:
            return f(*args, **kwargs)
        else:
            return jsonify({"error": "Unauthorized. Invalid or missing API Key."}), 401
    return decorated_function

# Data Structures
# Part: part_id, name, filename, material, print_settings
# PrintJob: job_id, part_id, printer_id, status, created_at, started_at, completed_at, priority
# Printer: printer_id, name, model, status, ip_address, serial_number, access_code

def load_data(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return [] # Return empty list for parts, jobs, printers if file not found

def save_data(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)


def load_users():
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {} # Return empty dict for users if file not found

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

@app.route('/')
def hello_world():
    # Could also redirect to login or dashboard if user session is implemented
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()

        if username in users:
            flash('Username already exists!')
            return redirect(url_for('signup'))

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        users[username] = hashed_password.decode('utf-8')
        save_users(users)
        flash('Signup successful! Please login.')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()

        if username not in users or not bcrypt.checkpw(password.encode('utf-8'), users[username].encode('utf-8')):
            flash('Invalid username or password!')
            return redirect(url_for('login'))

        flash('Login successful!')
        # In a real application, you would set up a session here
        return redirect(url_for('hello_world'))  # Or a dashboard page
    return render_template('login.html')

# Part Management Routes
@app.route('/parts')
def list_parts():
    parts = load_data(PARTS_FILE)
    return render_template('parts.html', parts=parts)

@app.route('/parts/add', methods=['GET', 'POST'])
def add_part():
    if request.method == 'POST':
        parts = load_data(PARTS_FILE)
        new_part = {
            'part_id': str(uuid.uuid4()),
            'name': request.form['name'],
            'material': request.form['material'],
            'print_settings': request.form['print_settings'],
            'filename': '' # Placeholder for now, will handle file upload later
        }
        # Handle file upload (basic)
        if 'part_file' in request.files:
            part_file = request.files['part_file']
            if part_file.filename != '':
                # In a real app, save to a secure location and store path
                new_part['filename'] = part_file.filename
                # For simplicity, we are not saving the file itself in this example
                # You would typically save it using part_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        parts.append(new_part)
        save_data(parts, PARTS_FILE)
        flash('Part added successfully!')
        return redirect(url_for('list_parts'))
    return render_template('add_part.html')

@app.route('/parts/<part_id>')
def view_part(part_id):
    parts = load_data(PARTS_FILE)
    part = next((p for p in parts if p['part_id'] == part_id), None)
    if part:
        return render_template('view_part.html', part=part)
    flash('Part not found!')
    return redirect(url_for('list_parts'))

# Printer Management Routes
@app.route('/printers')
def list_printers():
    printers = load_data(PRINTERS_FILE)
    return render_template('printers.html', printers=printers)

@app.route('/printers/add', methods=['GET', 'POST'])
def add_printer():
    if request.method == 'POST':
        printers = load_data(PRINTERS_FILE)
        new_printer = {
            'printer_id': str(uuid.uuid4()),
            'name': request.form['name'],
            'model': request.form['model'],
            'status': request.form['status'],
            'ip_address': request.form.get('ip_address'),
            'serial_number': request.form.get('serial_number'), # Added
            'access_code': request.form.get('access_code')      # Added
        }
        printers.append(new_printer)
        save_data(printers, PRINTERS_FILE)
        flash('Printer added successfully!')
        return redirect(url_for('list_printers'))
    return render_template('add_printer.html')

@app.route('/printers/<printer_id>')
def view_printer(printer_id):
    printers = load_data(PRINTERS_FILE)
    printer = next((p for p in printers if p['printer_id'] == printer_id), None)
    if printer:
        # Mocked printer status for now
        # In a real implementation, this would come from an API call using printer.ip_address, printer.serial_number, printer.access_code
        mock_status = {
            'state': 'idle',
            'nozzle_temp': 25,
            'nozzle_target_temp': 0,
            'bed_temp': 25,
            'bed_target_temp': 0,
            'progress': 0,
            'remaining_time': 0
        }
        
        # Placeholder for camera feed logic:
        # The camera feed could be an MJPEG stream or RTSP.
        # For MJPEG, an <img> tag could point to a Flask route that proxies the stream:
        # e.g., <img src="{{ url_for('camera_feed', printer_id=printer.printer_id) }}">
        # The /camera_feed/<printer_id> route in Flask would then use printer.ip_address 
        # and potentially printer.access_code to fetch and stream the camera data.
        # For RTSP, a JavaScript player might be needed, or a backend process to convert RTSP to a web-friendly format.
        # Camera URL often looks like rtsp://<printer_ip>/live or http://<printer_ip>/camera_stream
        # Access might require the printer's access code.

        return render_template('view_printer.html', printer=printer, printer_status=mock_status)
    flash('Printer not found!')
    return redirect(url_for('list_printers'))

# Print Queue Management Routes
@app.route('/print_queue')
def list_print_jobs():
    print_jobs_data = load_data(PRINT_JOBS_FILE)
    parts = load_data(PARTS_FILE)
    printers = load_data(PRINTERS_FILE)

    # Augment job data with part and printer names for easier display
    # Sort jobs by priority (lower number is higher priority), then by creation time for tie-breaking
    sorted_print_jobs_data = sorted(print_jobs_data, key=lambda j: (j.get('priority', 0), j.get('created_at', '')))
    
    display_jobs = []
    for job in sorted_print_jobs_data: # Use sorted data
        part = next((p for p in parts if p['part_id'] == job['part_id']), None)
        printer = next((pr for pr in printers if pr['printer_id'] == job['printer_id']), None)
        display_jobs.append({
            **job,
            'part_name': part['name'] if part else 'N/A',
            'printer_name': printer['name'] if printer else 'N/A'
        })
    return render_template('print_queue.html', print_jobs=display_jobs)

@app.route('/print_queue/add', methods=['GET', 'POST'])
def add_print_job():
    parts = load_data(PARTS_FILE)
    printers = load_data(PRINTERS_FILE)
    selected_part_id = request.args.get('part_id') # For pre-selection from view_part page

    if request.method == 'POST':
        print_jobs = load_data(PRINT_JOBS_FILE)
        new_job = {
            'job_id': str(uuid.uuid4()),
            'part_id': request.form['part_id'],
            'printer_id': request.form['printer_id'],
            'status': 'pending', # Initial status
            'created_at': datetime.utcnow().isoformat(),
            'started_at': None,
            'completed_at': None,
            'priority': int(request.form.get('priority', 0)) # Added priority
        }
        print_jobs.append(new_job)
        save_data(print_jobs, PRINT_JOBS_FILE)
        flash('Print job added to queue successfully!')
        return redirect(url_for('list_print_jobs'))
    
    return render_template('add_print_job.html', parts=parts, printers=printers, selected_part_id=selected_part_id)

@app.route('/print_queue/<job_id>')
def view_print_job(job_id):
    print_jobs = load_data(PRINT_JOBS_FILE)
    job = next((j for j in print_jobs if j['job_id'] == job_id), None)
    
    if not job:
        flash('Print job not found!')
        return redirect(url_for('list_print_jobs'))

    parts = load_data(PARTS_FILE)
    printers = load_data(PRINTERS_FILE)
    part = next((p for p in parts if p['part_id'] == job['part_id']), None)
    printer = next((pr for pr in printers if pr['printer_id'] == job['printer_id']), None)

    display_job = {
        **job,
        'part_name': part['name'] if part else 'N/A',
        'printer_name': printer['name'] if printer else 'N/A'
    }
    return render_template('view_print_job.html', job=display_job)

# Print Farm Dashboard
@app.route('/farm_dashboard')
def farm_dashboard():
    printers_data = load_data(PRINTERS_FILE)
    print_jobs_data = load_data(PRINT_JOBS_FILE)

    # Augment printer data with mocked live status for the dashboard
    # In a real scenario, this live status would be fetched via the API for each printer
    display_printers = []
    for printer in printers_data:
        # Mocked status logic similar to view_printer route
        mock_status = {
            'state': 'idle', # Default or fetched status
            'current_job_id': None # Placeholder, could be linked to print_jobs
        }
        # Example: if a job is running on this printer, update status
        for job in print_jobs_data:
            if job['printer_id'] == printer['printer_id'] and job['status'] == 'printing':
                mock_status['state'] = 'printing'
                mock_status['current_job_id'] = job['job_id']
                break
        
        display_printers.append({**printer, 'live_status': mock_status})

    # Print queue summary
    queue_summary = {
        'total_jobs': len(print_jobs_data),
        'jobs_pending': len([job for job in print_jobs_data if job['status'] == 'pending']),
        'jobs_printing': len([job for job in print_jobs_data if job['status'] == 'printing']),
        'jobs_completed': len([job for job in print_jobs_data if job['status'] == 'completed']),
        'jobs_error': len([job for job in print_jobs_data if job['status'] == 'error'])
    }

    return render_template('farm_dashboard.html', printers=display_printers, queue_summary=queue_summary)

# API Endpoints Start

# GET /api/parts - Returns a list of all parts.
@app.route('/api/parts', methods=['GET'])
@require_api_key
def api_list_parts():
    parts = load_data(PARTS_FILE)
    return jsonify(parts)

# GET /api/parts/<part_id> - Returns details of a specific part.
@app.route('/api/parts/<part_id>', methods=['GET'])
@require_api_key
def api_get_part(part_id):
    parts = load_data(PARTS_FILE)
    part = next((p for p in parts if p['part_id'] == part_id), None)
    if part:
        return jsonify(part)
    return jsonify({'error': 'Part not found'}), 404

# POST /api/parts - Creates a new part.
@app.route('/api/parts', methods=['POST'])
@require_api_key
def api_create_part():
    if not request.json:
        return jsonify({'error': 'Invalid input, JSON expected'}), 400
    
    data = request.json
    required_fields = ['name', 'material'] # 'filename' could be optional or handled differently
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields (name, material)'}), 400

    parts = load_data(PARTS_FILE)
    new_part = {
        'part_id': str(uuid.uuid4()),
        'name': data['name'],
        'material': data['material'],
        'print_settings': data.get('print_settings', ''),
        'filename': data.get('filename', '') # Filename might be just metadata here
    }
    parts.append(new_part)
    save_data(parts, PARTS_FILE)
    return jsonify(new_part), 201

# PUT /api/parts/<part_id> - Updates an existing part.
@app.route('/api/parts/<part_id>', methods=['PUT'])
@require_api_key
def api_update_part(part_id):
    if not request.json:
        return jsonify({'error': 'Invalid input, JSON expected'}), 400

    parts = load_data(PARTS_FILE)
    part_index = next((index for (index, p) in enumerate(parts) if p['part_id'] == part_id), None)

    if part_index is None:
        return jsonify({'error': 'Part not found'}), 404

    data = request.json
    # Update fields present in the request
    parts[part_index]['name'] = data.get('name', parts[part_index]['name'])
    parts[part_index]['material'] = data.get('material', parts[part_index]['material'])
    parts[part_index]['print_settings'] = data.get('print_settings', parts[part_index]['print_settings'])
    parts[part_index]['filename'] = data.get('filename', parts[part_index]['filename'])
    
    save_data(parts, PARTS_FILE)
    return jsonify(parts[part_index])

# DELETE /api/parts/<part_id> - Deletes a part.
@app.route('/api/parts/<part_id>', methods=['DELETE'])
@require_api_key
def api_delete_part(part_id):
    parts = load_data(PARTS_FILE)
    original_length = len(parts)
    parts = [p for p in parts if p['part_id'] != part_id]

    if len(parts) == original_length:
        return jsonify({'error': 'Part not found'}), 404
        
    save_data(parts, PARTS_FILE)
    return jsonify({'message': 'Part deleted successfully'})

# GET /api/printers - Returns a list of all printers.
@app.route('/api/printers', methods=['GET'])
@require_api_key
def api_list_printers():
    printers = load_data(PRINTERS_FILE)
    return jsonify(printers)

# GET /api/printers/<printer_id> - Returns details of a specific printer (including mocked live status).
@app.route('/api/printers/<printer_id>', methods=['GET'])
@require_api_key
def api_get_printer(printer_id):
    printers = load_data(PRINTERS_FILE)
    printer = next((p for p in printers if p['printer_id'] == printer_id), None)
    if printer:
        # Mocked status, similar to the web view
        mock_status = {
            'state': 'idle',
            'nozzle_temp': 25,
            'nozzle_target_temp': 0,
            'bed_temp': 25,
            'bed_target_temp': 0,
            'progress': 0,
            'remaining_time': 0
        }
        # Check if this printer is actually printing a job
        print_jobs_data = load_data(PRINT_JOBS_FILE)
        for job in print_jobs_data:
            if job['printer_id'] == printer['printer_id'] and job['status'] == 'printing':
                # Update mock_status if actually printing.
                # This is still simplified; a real system would query the printer.
                part_being_printed = next((p for p in load_data(PARTS_FILE) if p['part_id'] == job['part_id']), None)
                mock_status.update({
                    'state': 'printing',
                    'current_job_id': job['job_id'],
                    'current_part_name': part_being_printed['name'] if part_being_printed else 'N/A',
                    # Actual temps/progress would come from live API call in a real scenario
                })
                break
        return jsonify({**printer, 'live_status': mock_status})
    return jsonify({'error': 'Printer not found'}), 404

# GET /api/print_jobs - Returns a list of all print jobs.
@app.route('/api/print_jobs', methods=['GET'])
@require_api_key
def api_list_print_jobs():
    print_jobs = load_data(PRINT_JOBS_FILE)
    # Optionally sort or augment data as done in the web view
    sorted_print_jobs_data = sorted(print_jobs, key=lambda j: (j.get('priority', 0), j.get('created_at', '')))
    return jsonify(sorted_print_jobs_data)

# GET /api/print_jobs/<job_id> - Returns details of a specific print job.
@app.route('/api/print_jobs/<job_id>', methods=['GET'])
@require_api_key
def api_get_print_job(job_id):
    print_jobs = load_data(PRINT_JOBS_FILE)
    job = next((j for j in print_jobs if j['job_id'] == job_id), None)
    if job:
        # Augment with part and printer names, similar to web view
        parts = load_data(PARTS_FILE)
        printers = load_data(PRINTERS_FILE)
        part = next((p for p in parts if p['part_id'] == job['part_id']), None)
        printer = next((pr for pr in printers if pr['printer_id'] == job['printer_id']), None)
        display_job = {
            **job,
            'part_name': part['name'] if part else 'N/A',
            'printer_name': printer['name'] if printer else 'N/A'
        }
        return jsonify(display_job)
    return jsonify({'error': 'Print job not found'}), 404

# API Endpoints End

# API Documentation Route
@app.route('/api/docs')
def api_docs():
    return render_template('api_docs.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True) # Changed port and added host
