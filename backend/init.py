from config import app, db
from models import Pokemon
from flask import jsonify
import requests
import json
import string
from PIL import Image

def get_dominant_colors(pil_img, palette_size=16, num_colors=2):
    # Resize image to speed up processing
    img = pil_img.copy()
    img.thumbnail((100, 100))

    # Reduce colors (uses k-means internally)
    paletted = img.convert('P', palette=Image.ADAPTIVE, colors=palette_size)

    # Find the color that occurs most often
    palette = paletted.getpalette()
    color_counts = sorted(paletted.getcolors(), reverse=True)

    dominant_colors = []
    for i in range(num_colors):
      palette_index = color_counts[i][1]
      hex_color = '#%02x%02x%02x' % tuple(palette[palette_index*3:palette_index*3+3])
      dominant_colors.append(hex_color)

    return dominant_colors

def create_database():
    # Clear the existing Pokémon data
    Pokemon.query.delete()
    db.session.commit()

    # Static number of Pokémon (fetching gives megas and special forms)
    numPokemon = Pokemon.numPokemon
    #numPokemon = 100

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

            img = Image.open(requests.get(pokemonReq["sprites"]["other"]["official-artwork"]["front_default"], stream=True).raw)
            blank, primary_color, secondary_color = get_dominant_colors(img, 16, 3)

            # Save to the database
            new_pokemon = Pokemon(
                id=str(pokemonReq["id"]).zfill(4),
                name=string.capwords(pokemonReq["name"].lower()),
                abilities=json.dumps(pokemonReq["abilities"]),
                types=json.dumps(pokemonReq["types"]),
                picture=pokemonReq["sprites"]["other"]["official-artwork"]["front_default"],
                gen=pokemonSpeciesReq["generation"]["name"],
                color=pokemonSpeciesReq["color"]["name"],
                primary_color=primary_color,
                secondary_color=secondary_color
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
