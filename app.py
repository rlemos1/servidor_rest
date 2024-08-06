from flask import Flask, request, jsonify, Response
import requests
from google.protobuf.json_format import MessageToJson
import protobuf.favorite_pb2 as favorite_pb2

app = Flask(__name__)

DOG_API_URL = "https://dog.ceo/api"

# Bancos de dados simulados
breeds_db = [{"id": 1, "name": "Golden Retriever"}, {"id": 2, "name": "Labrador"}]
favorites_db = []

def format_response(data, format):
    if format == 'xml':
        from dicttoxml import dicttoxml
        return Response(dicttoxml(data), mimetype='application/xml')
    elif format == 'protobuf':
        if isinstance(data, list):
            # Convertendo uma lista de dicionários em uma mensagem protobuf
            response = [favorite_pb2.Favorite(id=item['id'], url=item['url']) for item in data]
            serialized = b"".join(fav.SerializeToString() for fav in response)
            return Response(serialized, mimetype='application/x-protobuf')
        elif isinstance(data, dict):
            favorite = favorite_pb2.Favorite(id=data["id"], url=data["url"])
            return Response(favorite.SerializeToString(), mimetype='application/x-protobuf')
    else:
        return jsonify(data)

@app.route('/breeds', methods=['GET', 'POST'])
def manage_breeds():
    global breeds_db  # Declara a variável global no início da função

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
        breed = request.json
        breed['id'] = len(breeds_db) + 1  # Gera um novo ID para a raça
        breeds_db.append(breed)
        return format_response({"message": "Breed added", "breed": breed}, format)

@app.route('/breeds/<int:breed_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_breed(breed_id):
    global breeds_db  # Declara a variável global no início da função

    format = request.args.get('format', 'json')
    if request.method == 'GET':
        breed = next((b for b in breeds_db if b.get("id") == breed_id), None)
        if breed:
            return format_response(breed, format)
        else:
            return format_response({"error": "Breed not found"}, format), 404
    elif request.method == 'PUT':
        breed = next((b for b in breeds_db if b.get("id") == breed_id), None)
        if breed:
            breed.update(request.json)
            return format_response({"message": "Breed updated", "breed": breed}, format)
        else:
            return format_response({"error": "Breed not found"}, format), 404
    elif request.method == 'DELETE':
        breeds_db[:] = [b for b in breeds_db if b.get("id") != breed_id]
        return format_response({"message": "Breed deleted"}, format)

@app.route('/favorites', methods=['POST', 'GET', 'DELETE'])
def manage_favorites():
    global favorites_db  # Declara a variável global no início da função

    format = request.args.get('format', 'json')
    if request.method == 'POST':
        favorite = {
            "id": len(favorites_db) + 1,
            "url": request.json.get('url')
        }
        favorites_db.append(favorite)
        return format_response({"message": "Favorite added", "favorite": favorite}, format)
    elif request.method == 'GET':
        return format_response(favorites_db, format)
    elif request.method == 'DELETE':
        favorite_id = request.json.get('id')
        favorites_db[:] = [f for f in favorites_db if f.get("id") != favorite_id]
        return format_response({"message": "Favorite deleted"}, format)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
