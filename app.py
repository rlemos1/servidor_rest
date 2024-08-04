from flask import Flask, request, jsonify, Response
import requests
from google.protobuf.json_format import MessageToJson
import protobuf.favorite_pb2 as favorite_pb2

app = Flask(__name__)

DOG_API_URL = "https://dog.ceo/api"

# Bancos de dados simulados
breeds_db = []
favorites_db = []

def format_response(data, format):
    if format == 'xml':
        from dicttoxml import dicttoxml
        return Response(dicttoxml(data), mimetype='application/xml')
    elif format == 'protobuf':
        # Assumindo que `data` é um dicionário com 'id' e 'url'
        favorite = favorite_pb2.Favorite()
        favorite.id = data["id"]
        favorite.url = data["url"]
        return Response(favorite.SerializeToString(), mimetype='application/x-protobuf')
    else:
        return jsonify(data)

@app.route('/breeds', methods=['GET', 'POST'])
def manage_breeds():
    format = request.args.get('format', 'json')
    if request.method == 'GET':
        # Consome a API externa para obter informações sobre raças
        response = requests.get(f"{DOG_API_URL}/breeds/list/all")
        if response.status_code == 200:
            breeds = response.json().get('message', {})
            return format_response(breeds, format)
        else:
            return format_response({"error": "Unable to fetch breeds from Dog API"}, format), response.status_code
    elif request.method == 'POST':
        breeds_db  # Declara a variável global
        breed = request.json.get('breed')
        breeds_db.append(breed)
        return format_response({"message": "Breed added", "breed": breed}, format)

@app.route('/breeds/<string:breed_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_breed(breed_id):
    format = request.args.get('format', 'json')
    if request.method == 'GET':
        breed = next((b for b in breeds_db if b.get("id") == breed_id), None)
        if breed:
            return format_response(breed, format)
        else:
            return format_response({"error": "Breed not found"}, format), 404
    elif request.method == 'PUT':
        breeds_db  # Declara a variável global
        breed = next((b for b in breeds_db if b.get("id") == breed_id), None)
        if breed:
            breed.update(request.json)
            return format_response({"message": "Breed updated", "breed": breed}, format)
        else:
            return format_response({"error": "Breed not found"}, format), 404
    elif request.method == 'DELETE':
        breeds_db  # Declara a variável global
        breeds_db[:] = [b for b in breeds_db if b.get("id") != breed_id]
        return format_response({"message": "Breed deleted"}, format)

@app.route('/favorites', methods=['POST', 'GET', 'DELETE'])
def manage_favorites():
    format = request.args.get('format', 'json')
    if request.method == 'POST':
        favorites_db  # Declara a variável global
        favorite = {
            "id": len(favorites_db) + 1,
            "url": request.json.get('url')
        }
        favorites_db.append(favorite)
        return format_response({"message": "Favorite added", "favorite": favorite}, format)
    elif request.method == 'GET':
        return format_response(favorites_db, format)
    elif request.method == 'DELETE':
        favorites_db  # Declara a variável global
        favorite_id = request.json.get('id')
        favorites_db[:] = [f for f in favorites_db if f.get("id") != favorite_id]
        return format_response({"message": "Favorite deleted"}, format)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
