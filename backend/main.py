from flask import request, jsonify
from config import app, db
from models import Pokemon

@app.route("/pokemon", methods=["GET"])
def get_pokemon():
    pokemon = Pokemon.query.all()
    json_contacts = list(map(lambda x: x.to_json(), pokemon))
    return (jsonify({"pokemon": json_contacts}), 200)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)

