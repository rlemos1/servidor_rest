from flask import Flask, request, jsonify, Response
import requests
import json
from google.protobuf.json_format import MessageToJson
import protobuf.favorite_pb2 as favorite_pb2  # Atualização aqui

app = Flask(__name__)

DOG_API_URL = "https://dog.ceo/api"

breeds_db = []
favorites_db = []

# Helper function to format response
def format_response(data, format):
    if format == 'xml':
        # Convert JSON to XML (simplified for brevity)
        from dicttoxml import dicttoxml
        return Response(dicttoxml(data), mimetype='application/xml')
    elif format == 'protobuf':
        # Convert data to Protocol Buffers
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
        response = requests.get(f"{DOG_API_URL}/breeds/list/all")
        breeds = response.json().get('message', {})
        return format_response(breeds, format)
    elif request.method == 'POST':
        breed = request.json.get('breed')
        breeds_db.append(breed)
        return format_response({"message": "Breed added", "breed": breed}, format)

@app.route('/breeds/<string:breed_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_breed(breed_id):
    format = request.args.get('format', 'json')
    if request.method == 'GET':
        breed = next((b for b in breeds_db if b["id"] == breed_id), None)
        if breed:
            return format_response(breed, format)
        else:
            return format_response({"error": "Breed not found"}, format), 404
    elif request.method == 'PUT':
        breed = next((b for b in breeds_db if b["id"] == breed_id), None)
        if breed:
            breed.update(request.json)
            return format_response({"message": "Breed updated", "breed": breed}, format)
        else:
            return format_response({"error": "Breed not found"}, format), 404
    elif request.method == 'DELETE':
        global breeds_db
        breeds_db = [b for b in breeds_db if b["id"] != breed_id]
        return format_response({"message": "Breed deleted"}, format)

@app.route('/favorites', methods=['POST', 'GET', 'DELETE'])
def manage_favorites():
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
        global favorites_db
        favorites_db = [f for f in favorites_db if f["id"] != favorite_id]
        return format_response({"message": "Favorite deleted"}, format)

if __name__ == '__main__':
    app.run(debug=True)
