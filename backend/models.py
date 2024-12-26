from config import db

class Pokemon(db.Model):
    __tablename__ = 'pokemon'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    abilities = db.Column(db.Text, nullable=False)
    types = db.Column(db.Text, nullable=False)
    picture = db.Column(db.String(255), nullable=True)
    gen = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(50), nullable=False)

    def __init__(self, id, name, abilities, types, picture, gen, color):
        self.id = id
        self.name = name
        self.abilities = abilities
        self.types = types
        self.picture = picture
        self.gen = gen
        self.color = color

    def __repr__(self):
        return f"<Pokemon {self.id} - {self.name}>"

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
        }

