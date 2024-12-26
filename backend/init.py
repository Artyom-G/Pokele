from config import app, db
from models import Pokemon
from flask import jsonify
from flask_restful import Resource, Api
import requests
import json

# Should be Delete and Post but its expecting a Get for some reason 
@app.route('/api/v1/pokemon/create', methods=["GET", "POST", "DELETE", "PATCH"])
def create_database():
    # Clear the existing Pokémon data
    Pokemon.query.delete()
    db.session.commit()

    # Static number of Pokémon (fetching gives megas and special forms)
    numPokemon = Pokemon.numPokemon

    # Fetching Pokémon data
    r = requests.get(f"https://pokeapi.co/api/v2/pokemon/?limit={numPokemon}")
    if r.status_code != 200:
        return jsonify({"error": f"Failed to fetch Pokémon list: {r.status_code}"}), 500

    pokemonUrls = r.json()["results"]
    i = 1
    for pokemonUrl in pokemonUrls:
        if i % 50 == 0: print(f"Adding Pokemon #{i}")
        try:
            # Fetch Pokémon details
            pokemonReq = requests.get(pokemonUrl["url"]).json()
            pokemonSpeciesReq = requests.get(pokemonReq["species"]["url"]).json()

            # Save to the database
            new_pokemon = Pokemon(
                id=pokemonReq["id"],
                name=pokemonReq["name"],
                abilities=json.dumps(pokemonReq["abilities"]),
                types=json.dumps(pokemonReq["types"]),
                picture=pokemonReq["sprites"]["other"]["official-artwork"]["front_default"],
                gen=pokemonSpeciesReq["generation"]["name"],
                color=pokemonSpeciesReq["color"]["name"],
            )
            db.session.add(new_pokemon)
            if i % 50 == 0: print(f"Added {new_pokemon.name} #{new_pokemon.id}")
            
        except Exception as e:
            print(f"Error processing {pokemonUrl['name']}: {e}")

        i+=1

    try:
        db.session.commit()
    except Exception as e:
        print(str(e))
        return (jsonify({"message": str(e)}), 400)
    print("Created Database!")
    return jsonify({"message": "Successfully created database"}), 200

if __name__ == "__main__":
    print("Init Started")
    with app.app_context():
        db.create_all()
        create_database()

    app.run(debug=True)