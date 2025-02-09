from flask import Flask, request, jsonify
from flask_cors import CORS
from app import rps_body

app = Flask(__name__)
CORS(app)

entities_used = set('Rock')

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    userEntity = data.get('userEntity')
    systemEntity = data.get('systemEntity')
    func_output = rps_body(userEntity, systemEntity, entities_used)
    return jsonify(func_output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
