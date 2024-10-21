import json
import os.path
from flask import Flask,  jsonify, request, render_template
from flask_cors import CORS

app = Flask(__name__, static_folder='../data/img', template_folder='../client')
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '../data')
JSON_FILE = os.path.join(DATA_DIR, 'resultats.json')

@app.route('/', methods=['GET'])
def get_index():
    return render_template('index.html')

@app.route('/script.js')
def get_script():
    return render_template('script.js', name='mark')

@app.route('/api/duplicates', methods=['GET'])
def get_duplicates():
    with open(JSON_FILE, 'r') as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/api/keep', methods=['POST'])
def keep_all():
    data = request.get_json()
    update_result_file(data, "keepall")
    return jsonify({"status": "success", "message": "Tag keepall ajouté avec succès"})


def update_result_file(data, tag):
    with open(JSON_FILE, 'r') as f:
        results = json.load(f)
    for key in data:
        results[key] = {"paths": results[key], "tag": tag}
    with open(JSON_FILE, 'w') as f:
        json.dump(results, f, indent=4)

if __name__ == '__main__':
    app.run(debug=True)
