from flask import request, jsonify
from config import app, db
from models import Pokemon
import json
import random
from datetime import datetime

@app.route("/api/v1/all", methods=["GET"])
def get_all_pokemon():
    all_pokemon = Pokemon.query.all()
    if not all_pokemon:
        return (jsonify({"message": "All pokemon not found"}), 404)

    pokemon_list = [pokemon.to_json() for pokemon in all_pokemon]
    return jsonify(pokemon_list), 200

@app.route("/api/v1/<int:id>", methods=["GET"])
def get_pokemon(id):
    pokemon = Pokemon.query.get(id)
    if not pokemon:
        return jsonify({"message": "Pokemon not found"}), 404
    return jsonify({"pokemon": pokemon.to_json()}), 200

@app.route("/api/v1/today", methods=["GET"])
def get_today_pokemon():
    modulo = Pokemon.numPokemon
    seed = int(datetime.today().strftime('%Y%m%d'))
    random.seed(seed)
    id = random.randint(0, modulo)+1
    print(f"Generating with seed {seed}, returns #{id}")
    return get_pokemon(id)

@app.route("/api/v1/validate/<int:id>", methods=["GET"])
def validate_pokemon(id):
    pokemon_today, status_today = get_today_pokemon()
    pokemon_id, status_id = get_pokemon(id)
    if(status_today != 200 or status_id != 200): return jsonify({"message": "Error!"}), 404
    print("Checking ", json.loads(pokemon_today.data)["pokemon"]["name"], " and ", json.loads(pokemon_id.data)["pokemon"]["name"])
    return jsonify({"response": json.loads(pokemon_today.data)["pokemon"]["name"] == json.loads(pokemon_id.data)["pokemon"]["name"]}), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)

