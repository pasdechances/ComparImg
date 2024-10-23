import json
import os.path
import subprocess
import threading
from flask import Flask,  jsonify, request, render_template, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='../client', template_folder='../client')
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'data'))
JSON_FILE = os.path.join(DATA_DIR, 'resultats.json')

SCRIPT_RUNNING = False

@app.route('/', methods=['GET'])
def serve_index():
    return render_template('index.html')

@app.route('/<path:filename>', methods=['GET'])
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/api/duplicates', methods=['GET'])
def serve_duplicates():
    global JSON_FILE
    with open(JSON_FILE, 'r') as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/api/detection', methods=['POST'])
def launch_detect():
    global SCRIPT_RUNNING
    lock = threading.Lock()
    if SCRIPT_RUNNING:
        return jsonify({"status": "error", "message": "Script is already running"}), 409
    data = request.get_json()
    script_path = os.path.join(BASE_DIR, 'detect.py')
    command = ['python', script_path]
    if isinstance(data.get('image_dir'), str):
        image_dir = data.get('image_dir')
        if image_dir:
            command.extend(['-i', image_dir])
    if isinstance(data.get('hsize'), int):
        hsize = data.get('hsize')
        if hsize:
            command.extend(['-s', str(hsize)])
    if isinstance(data.get('tolerance'), int):
        tolerance = data.get('tolerance')
        if tolerance:
            command.extend(['-t', str(tolerance)])
    try:
        lock.acquire()
        SCRIPT_RUNNING = True
        thread = threading.Thread(target=run_script, args=(command,lock))
        thread.start()
        return jsonify({"status": "success", "message": "Detect started"}), 202
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/sort', methods=['POST'])
def launch_sorter():
    global SCRIPT_RUNNING
    lock = threading.Lock()
    if SCRIPT_RUNNING:
        return jsonify({"status": "error", "message": "Script is already running"}), 409
    data = request.get_json()
    if isinstance(data.get('trash_folder'), int):
        trash_folder = data.get('trash_folder')
    script_path = os.path.join(BASE_DIR, 'sorter.py')
    command = ['python', script_path]
    if trash_folder:
        command.extend(['-t', str(trash_folder)])
    try:
        lock.acquire()
        SCRIPT_RUNNING = True
        thread = threading.Thread(target=run_script, args=(command,lock))
        thread.start()
        return jsonify({"status": "success", "message": "Sort started"}), 202
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/script-status', methods=['GET'])
def script_status():
    global SCRIPT_RUNNING
    status = "running" if SCRIPT_RUNNING else "idle"
    return jsonify({"status": status}) 

@app.route('/api/img/trow/<group_id>/<image_id>', methods=['DELETE'])
def trowImg(group_id, image_id):
    update_result_file("trash", group_id, image_id)
    return jsonify({"status": "success", "message": "Trash tag added"})

@app.route('/img/<group_id>/<image_id>', methods=['GET'])
def serve_image(group_id, image_id):
    with open(os.path.join(DATA_DIR, 'resultats.json'), 'r') as f:
        data = json.load(f)
    if group_id in data:
        for img in data[group_id]:
            if str(img['image_id']) == image_id:
                img_path = img['image_path']
                return send_from_directory(os.path.dirname(img_path), os.path.basename(img_path))
    return "Image not found", 404 

@app.route('/api/clear', methods=['DELETE'])
def api_clear():
    global JSON_FILE
    csv_file = os.path.join(DATA_DIR, 'image_hashes.csv')
    try:
        with open(JSON_FILE, 'w') as f:
            f.write('{}')
        with open(csv_file, 'w') as f:
            f.truncate(0)
        return jsonify({"status": "success", "message": "Files emptied successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

def update_result_file(tag, group_id, image_id):
    global JSON_FILE
    with open(JSON_FILE, 'r') as f:
        results = json.load(f)
    if group_id in results:
        for img in results[group_id]:
            if str(img['image_id']) == image_id:
                img['tag'] = tag
    with open(JSON_FILE, 'w') as f:
        json.dump(results, f, indent=4)

def run_script(command, script_lock_var):
    global SCRIPT_RUNNING
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print("Script terminé avec succès")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution du script: {str(e)}")
        print(e.output)
        print(e.stderr)
    finally:
        # Libération du verrou à la fin du script
        SCRIPT_RUNNING = False
        script_lock_var.release()


if __name__ == '__main__':
    app.run(debug=True)
