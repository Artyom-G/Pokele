from flask import request, jsonify
from config import app, db
from models import Pokemon
import json
import random
from datetime import datetime
import string

@app.route("/api/v1/ping", methods=["GET"])
def get_ping():
    return jsonify({"message": "pong"}), 200

#@app.route("/api/v1/all", methods=["GET"])
def get_all_pokemon():
    all_pokemon = Pokemon.query.all()
    if not all_pokemon:
        return (jsonify({"message": "All pokemon not found"}), 404)

    pokemon_list = [pokemon.to_json() for pokemon in all_pokemon]
    return jsonify(pokemon_list), 200

@app.route("/api/v1/<name>", methods=["GET"])
def get_pokemon(name):
    pokemon = None
    if(not name.isnumeric()): pokemon = Pokemon.query.get(string.capwords(name.lower()))
    else: pokemon = Pokemon.query.filter_by(id=name.zfill(4)).first()
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
    pokemon = Pokemon.query.filter_by(id=str(id).zfill(4)).first()
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
    if(pokemon_today["name"] == pokemon_guess["name"]): pokemon = pokemon_today
    id = ""
    for i in range(len(pokemon_today["id"])):
        if pokemon_today["id"][i] == pokemon_guess["id"][i]: id += pokemon_today["id"][i]
        else: id += "?"
    pokemon["id"] = id
    abilities = []
    for ability in pokemon_guess["abilities"]:
        if ability in pokemon_today["abilities"]: abilities.append(ability)
    pokemon["abilities"] = abilities
    if(pokemon_today["color"] == pokemon_guess["color"]): 
        pokemon["color"] = pokemon_today["color"]
        pokemon["primary_color"] = pokemon_today["primary_color"]
        pokemon["secondary_color"] = pokemon_today["secondary_color"]
    if(pokemon_today["gen"] == pokemon_guess["gen"]): pokemon["gen"] = pokemon_today["gen"]
    if(pokemon_today["picture"] == pokemon_guess["picture"]): pokemon["picture"] = pokemon_today["picture"]
    types = []
    for type in pokemon_guess["types"]:
        if type in pokemon_today["types"]: types.append(type)
    pokemon["types"] = types

    return jsonify({"response": pokemon}), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run("0.0.0.0", 5000)
    #app.run(debug=False)

