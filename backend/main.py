from flask import request, jsonify
from config import app, db
from models import Pokemon
import json
import random
from datetime import datetime

#@app.route("/api/v1/all", methods=["GET"])
def get_all_pokemon():
    all_pokemon = Pokemon.query.all()
    if not all_pokemon:
        return (jsonify({"message": "All pokemon not found"}), 404)

    pokemon_list = [pokemon.to_json() for pokemon in all_pokemon]
    return jsonify(pokemon_list), 200

#@app.route("/api/v1/<name>", methods=["GET"])
def get_pokemon(name):
    pokemon = None
    if(not name.isnumeric()): pokemon = Pokemon.query.get(name)
    else: pokemon = Pokemon.query.filter_by(id=name).first()
    if not pokemon:
        return jsonify({"message": "Pokemon not found"}), 404
    return jsonify({"pokemon": pokemon.to_json()}), 200

#@app.route("/api/v1/today", methods=["GET"])
def get_today_pokemon():
    modulo = Pokemon.numPokemon
    seed = int(datetime.today().strftime('%Y%m%d'))
    random.seed(seed)
    id = random.randint(0, modulo)+1
    print(f"Generating with seed {seed}, returns #{id}")
    pokemon = Pokemon.query.filter_by(id=id).first()
    if not pokemon:
        return jsonify({"message": "Pokemon not found"}), 404

    return jsonify({"pokemon": pokemon.to_json()}), 200
    
@app.route("/api/v1/guess/<name>", methods=["GET"])
def validate_pokemon(name):
    pokemon_today, status_today = get_today_pokemon()
    pokemon_today = json.loads(pokemon_today.data)["pokemon"]
    pokemon_guess, status_guess = get_pokemon(name)
    pokemon_guess = json.loads(pokemon_guess.data)["pokemon"]
    if(status_today != 200 or status_guess != 200): return jsonify({"message": "Error!"}), 404
    
    print("Checking ", pokemon_today["name"], " and ", pokemon_guess["name"])
    
    pokemon = dict()
    if(pokemon_today["id"] == pokemon_guess["id"]): pokemon = pokemon_today
    if(pokemon_today["abilities"] == pokemon_guess["abilities"]): pokemon["abilities"] = pokemon_today["abilities"]
    if(pokemon_today["color"] == pokemon_guess["color"]): pokemon["color"] = pokemon_today["color"]
    if(pokemon_today["gen"] == pokemon_guess["gen"]): pokemon["gen"] = pokemon_today["gen"]
    if(pokemon_today["picture"] == pokemon_guess["picture"]): pokemon["picture"] = pokemon_today["picture"]
    if(pokemon_today["types"] == pokemon_guess["types"]): pokemon["types"] = pokemon_today["types"]

    return jsonify({"response": pokemon}), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)

