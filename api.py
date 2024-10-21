import json
from flask import Flask,  jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/duplicates', methods=['GET'])
def get_duplicates():
    with open('resultats.json', 'r') as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/api/keepall', methods=['POST'])
def keep_all():
    data = request.get_json()
    update_result_file(data, "keepall")
    return jsonify({"status": "success", "message": "Tag keepall ajouté avec succès"})

@app.route('/api/keepbest', methods=['POST'])
def keep_best():
    data = request.get_json()
    update_result_file(data, "keepbest")
    return jsonify({"status": "success", "message": "Tag keepbest ajouté avec succès"})

def update_result_file(data, tag):
    with open('resultats.json', 'r') as f:
        results = json.load(f)
    for key in data:
        results[key] = {"paths": results[key], "tag": tag}
    with open('resultats.json', 'w') as f:
        json.dump(results, f, indent=4)

if __name__ == '__main__':
    app.run(debug=True)
