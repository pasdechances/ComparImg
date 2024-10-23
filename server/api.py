import json
import os.path
from flask import Flask,  jsonify, request, render_template, send_from_directory
from flask_cors import CORS

app = Flask(__name__, template_folder='../client')
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'data'))
JSON_FILE = os.path.join(DATA_DIR, 'resultats.json')

@app.route('/', methods=['GET'])
def serve_index():
    return render_template('index.html')

@app.route('/script.js', methods=['GET'])
def serve_script():
    return render_template('script.js', name='mark')

@app.route('/api/duplicates', methods=['GET'])
def serve_duplicates():
    with open(JSON_FILE, 'r') as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/api/detection', methods=['POST'])
def launch_detect():
    return 0

@app.route('/api/sort', methods=['POST'])
def launch_sorter():
    return 0

@app.route('/api/img/keep/<group_id>/<image_id>', methods=['PUT'])
def keepImg(group_id, image_id):
    update_result_file("keep", group_id, image_id)
    return jsonify({"status": "success", "message": "Tag keepall ajouté avec succès"})

@app.route('/api/img/trow/<group_id>/<image_id>', methods=['DELETE'])
def trowImg(group_id, image_id):
    update_result_file("trash", group_id, image_id)
    return jsonify({"status": "success", "message": "Tag keepall ajouté avec succès"})

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

def update_result_file(tag, group_id, image_id):
    with open(JSON_FILE, 'r') as f:
        results = json.load(f)
    if group_id in results:
        for img in results[group_id]:
            if str(img['image_id']) == image_id:
                img['tag'] = tag
    with open(JSON_FILE, 'w') as f:
        json.dump(results, f, indent=4)

if __name__ == '__main__':
    app.run(debug=True)
