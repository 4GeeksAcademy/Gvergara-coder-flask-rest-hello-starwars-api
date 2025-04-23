"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planets, Starships, FavoriteCharacters, FavoritePlanets, FavoriteStarships
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_users():
    users = User.query.all()
    print(users)
    users_serialized = []
    for user in users:
        users_serialized.append(user.serialize())
    print(users_serialized)

    response_body = {
        'data': users_serialized
    }

    return jsonify(response_body), 200

@app.route('/character', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    characters_serialized = []
    for character in characters:
        characters_serialized.append(character.serialize())
    print(characters_serialized)

    response_body = {
        'data': characters_serialized
    }

    return jsonify(response_body), 200

@app.route('/planet', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    planets_serialized = []
    for planet in planets:
        planets_serialized.append(planet.serialize())
    print(planets_serialized)

    response_body = {
        'data': planets_serialized
    }

    return jsonify(response_body), 200

@app.route('/starship', methods=['GET'])
def get_starships():
    starships = Starships.query.all()
    starships_serialized = []
    for starship in starships:
        starships_serialized.append(starship.serialize())
    print(starships_serialized)

    response_body = {
        'data': starships_serialized
    }

    return jsonify(response_body), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    response_body = {
        'data': user.serialize()
    }

    return jsonify(response_body), 200

@app.route('/character/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Character.query.get(character_id)
    if not character:
        return jsonify({'message': 'Character not found'}), 404

    response_body = {
        'data': character.serialize()
    }

    return jsonify(response_body), 200

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planets.query.get(planet_id)
    if not planet:
        return jsonify({'message': 'Planet not found'}), 404

    response_body = {
        'data': planet.serialize()
    }

    return jsonify(response_body), 200

@app.route('/starship/<int:starship_id>', methods=['GET'])
def get_starship(starship_id):
    starship = Starships.query.get(starship_id)
    if not starship:
        return jsonify({'message': 'Starship not found'}), 404

    response_body = {
        'data': starship.serialize()
    }

    return jsonify(response_body), 200

@app.route('/favoritecharacter', methods=['GET'])
def get_favorite_characters():
    favorite_characters = FavoriteCharacters.query.all()
    print(favorite_characters)
    favorite_characters_serialized = []
    for favorite_character in favorite_characters:
        favorite_characters_serialized.append(favorite_character.serialize())
    print(favorite_characters_serialized)

    response_body = {
        'data': favorite_characters_serialized
    }

    return jsonify(response_body), 200

@app.route('/favoriteplanet', methods=['GET'])
def get_favorite_planets():
    favorite_planets = FavoritePlanets.query.all()
    favorite_planets_serialized = []
    print(favorite_planets)
    for favorite_planet in favorite_planets:
        favorite_planets_serialized.append(favorite_planet.serialize())
    print(favorite_planets_serialized)

    response_body = {
        'data': favorite_planets_serialized
    }

    return jsonify(response_body), 200

@app.route('/favoritestarship', methods=['GET'])
def get_favorite_starships():
    favorite_starships = FavoriteStarships.query.all()
    favorite_starships_serialized = []
    print(favorite_starships)
    for favorite_starship in favorite_starships:
        favorite_starships_serialized.append(favorite_starship.serialize())
    print(favorite_starships_serialized)

    response_body = {
        'data': favorite_starships_serialized
    }

    return jsonify(response_body), 200

@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_favorites(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'msg': 'User not found'}), 404
    return jsonify(user.serialize_favorites()), 200

@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()

    if not data or not all(key in data for key in ('email', 'password', 'firstName', 'lastName')):
        return jsonify({'message': 'Missing required fields'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already exists'}), 400

    new_user = User(
        email=data['email'],
        password=data['password'], 
        firstName=data['firstName'],
        lastName=data['lastName'],
        is_active=True
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully', 'user': new_user.serialize()}), 201

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    planet = Planets.query.get(planet_id)
    if not planet:
        return jsonify({'message': 'Planet not found'}), 404

    favorite_planet = FavoritePlanets(planet_id=planet_id)
    db.session.add(favorite_planet)
    db.session.commit()

    return jsonify({'message': f'Planet {planet_id} added to favorites'}), 201

@app.route('/favorite/character/<int:character_id>', methods=['POST'])
def add_favorite_character(character_id):
    character = Character.query.get(character_id)
    if not character:
        return jsonify({'message': 'Character not found'}), 404

    favorite_character = FavoriteCharacters(character_id=character_id)
    db.session.add(favorite_character)
    db.session.commit()

    return jsonify({'message': f'Character {character_id} added to favorites'}), 201

@app.route('/favorite/starship/<int:starship_id>', methods=['POST'])
def add_favorite_starship(starship_id):
    starship = Starships.query.get(starship_id)
    if not starship:
        return jsonify({'message': 'Starship not found'}), 404

    favorite_starship = FavoriteStarships(starship_id=starship_id)
    db.session.add(favorite_starship)
    db.session.commit()

    return jsonify({'message': f'Starship {starship_id} added to favorites'}), 201

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def remove_favorite_planet(planet_id):
    favorite_planet = FavoritePlanets.query.filter_by(planet_id=planet_id).first()
    if not favorite_planet:
        return jsonify({'message': 'Favorite planet not found'}), 404

    db.session.delete(favorite_planet)
    db.session.commit()

    return jsonify({'message': f'Planet {planet_id} removed from favorites'}), 200

@app.route('/favorite/character/<int:character_id>', methods=['DELETE'])
def remove_favorite_character(character_id):
    favorite_character = FavoriteCharacters.query.filter_by(character_id=character_id).first()
    if not favorite_character:
        return jsonify({'message': 'Favorite character not found'}), 404

    db.session.delete(favorite_character)
    db.session.commit()

    return jsonify({'message': f'Character {character_id} removed from favorites'}), 200

@app.route('/favorite/starship/<int:starship_id>', methods=['DELETE'])
def remove_favorite_starship(starship_id):
    favorite_starship = FavoriteStarships.query.filter_by(starship_id=starship_id).first()
    if not favorite_starship:
        return jsonify({'message': 'Favorite starship not found'}), 404

    db.session.delete(favorite_starship)
    db.session.commit()

    return jsonify({'message': f'Starship {starship_id} removed from favorites'}), 200

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': f'User {user_id} deleted successfully'}), 200

@app.route('/character/<int:character_id>', methods=['PUT'])
def update_character(character_id):
    character = Character.query.get(character_id)
    if not character:
        return jsonify({'message': 'Character not found'}), 404

    character.name = request.json.get('name', character.name)
    character.gender = request.json.get('gender', character.gender)
    character.height = request.json.get('height', character.height)

    db.session.commit()
    return jsonify({'message': f'Character {character_id} updated successfully', 'character': character.serialize()}), 200

@app.route('/planet/<int:planet_id>', methods=['PUT'])
def update_planet(planet_id):
    planet = Planets.query.get(planet_id)
    if not planet:
        return jsonify({'message': 'Planet not found'}), 404

    planet.name = request.json.get('name', planet.name)
    planet.weather = request.json.get('weather', planet.weather)

    db.session.commit()
    return jsonify({'message': f'Planet {planet_id} updated successfully', 'planet': planet.serialize()}), 200

@app.route('/starship/<int:starship_id>', methods=['PUT'])
def update_starship(starship_id):
    starship = Starships.query.get(starship_id)
    if not starship:
        return jsonify({'message': 'Starship not found'}), 404

    starship.name = request.json.get('name', starship.name)
    starship.color = request.json.get('color', starship.color)

    db.session.commit()
    return jsonify({'message': f'Starship {starship_id} updated successfully', 'starship': starship.serialize()}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
