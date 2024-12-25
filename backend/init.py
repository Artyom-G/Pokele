from config import app, db
from models import Pokemon
from flask import jsonify
from flask_restful import Resource, Api
import requests

@app.route('/v1/pokemon/create', methods=["DELETE", "GET", "POST"])
def create_database():
    Pokemon.query.delete()

    # Getting num of pokemon
    numPokemon = 1025 # you cant make the number of pokemon dynamic because they include megas and special forms
    numPokemon = 1
    r = requests.get(f"https://pokeapi.co/api/v2/pokemon/?limit={numPokemon}/")

    if r.status_code == 200:
        data = r.json()
        numPokemon = int(data["count"])
    else:
        print(f"Failed to fetch data (num of pokemon): {r.status_code}, {r.text}")

    # Getting all pokemon
    r = requests.get(f"https://pokeapi.co/api/v2/pokemon/?limit={numPokemon}/")
    if r.status_code == 200:
        # Below gets all pokemon's name and api url
        pokemonUrls = r.json()["results"]
        for pokemonUrl in pokemonUrls:
            pokemonReq = requests.get(pokemonUrl["url"]).json()
            pokemonData = dict()
            pokemonData["abilities"] = pokemonReq["abilities"]
            pokemonData["moves"] = pokemonReq["moves"]
            pokemonData["id"] = pokemonReq["id"]
            pokemonData["name"] = pokemonReq["name"]
            pokemonData["types"] = pokemonReq["types"]
            pokemonData["picture"] = pokemonReq["sprites"]["other"]["official-artwork"]["front_default"]
            print(pokemonData)

    else:
        print(f"Failed to fetch data (all pokemon): {r.status_code}, {r.text}")

    return jsonify({"message": "Database updated!"}), 200

if __name__ == "__main__":
    print("Init Started")
    with app.app_context():
        db.create_all()

    app.run(debug=True)