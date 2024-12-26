from config import db
import json

class Pokemon(db.Model):
    __tablename__ = 'pokemon'
    numPokemon = 1025

    id = db.Column(db.String(4), unique=True, nullable=False)
    name = db.Column(db.String(100), primary_key=True)
    abilities = db.Column(db.Text, nullable=False)
    types = db.Column(db.Text, nullable=False)
    picture = db.Column(db.String(255), nullable=False)
    gen = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(50), nullable=False)
    primary_color = db.Column(db.String(10), nullable=False)
    secondary_color = db.Column(db.String(10), nullable=False)

    def __init__(self, id, name, abilities, types, picture, gen, color, primary_color, secondary_color):
        self.id = id
        self.name = name
        self.abilities = json.dumps([ability["ability"]["name"] for ability in json.loads(abilities)])
        self.types = json.dumps([type["type"]["name"] for type in json.loads(types)])
        self.picture = picture
        self.gen = gen
        self.beautify_gen()
        # color is boy-color (color categories) eg. red, blue, green, black
        self.color = color
        # these colors are accurate, hex codes
        self.primary_color = primary_color
        self.secondary_color = secondary_color

    def __repr__(self):
        return f"<Pokemon {self.id} - {self.name}>"

    def beautify_gen(self):
        self.gen = self.gen[11:].upper()

    def to_json(self):
        pokemon = self
        return {
            "id": pokemon.id,
            "name": pokemon.name,
            "abilities": json.loads(pokemon.abilities),
            "types": json.loads(pokemon.types),
            "picture": pokemon.picture,
            "gen": pokemon.gen,
            "color": pokemon.color,
            "primary_color": pokemon.primary_color,
            "secondary_color": pokemon.secondary_color,
        }

