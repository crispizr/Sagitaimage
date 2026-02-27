from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import base64

app = Flask(__name__)
CORS(app)

@app.route('/')
def accueil():
    return jsonify({'status': 'ok', 'message': 'API Sagitaimage en ligne !'})

@app.route('/analyser', methods=['POST'])
def analyser():
    data = request.json
    token = data.get('token')
    modele = data.get('modele')
    image_base64 = data.get('image')

    if not token or not modele or not image_base64:
        return jsonify({'erreur': 'Paramètres manquants'}), 400

    image_bytes = base64.b64decode(image_base64)

    reponse = requests.post(
        f'https://api-inference.huggingface.co/models/{modele}',
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/octet-stream'
        },
        data=image_bytes
    )

    return jsonify(reponse.json()), reponse.status_code

if __name__ == '__main__':
    app.run(debug=True)
