import os
from flask_admin import Admin
from models import db, User, Character, Planets, Starships, FavoriteCharacters, FavoritePlanets, FavoriteStarships
from flask_admin.contrib.sqla import ModelView

class PeopleFavoritesModelView(ModelView):
    column_auto_select_related = True  # Carga automáticamente las relaciones
    # Columnas y relationships de mi tabla PeopleFavorites
    column_list = ['id', 'user', 'people', 'user_id', 'people_id']


class PeopleModelView(ModelView):
    column_auto_select_related = True  # Carga automáticamente las relaciones
    # Columnas y relationships de mi tabla PeopleFavorites
    column_list = ['id', 'name', 'email', 'height', 'favorite_by']


class UserModelView(ModelView):
    column_auto_select_related = True  # Carga automáticamente las relaciones
    # Columnas y relationships de mi tabla PeopleFavorites
    column_list = ['id', 'email', 'password', 'firstName', 'lastName', 'is_active', 'favorites_characters', 'favorites_planets', 'favorites_starships']

class CharacterModelView(ModelView):
    column_auto_select_related = True  # Carga automáticamente las relaciones
    # Columnas y relationships de mi tabla PeopleFavorites
    column_list =['id', 'name', 'gender', 'height', 'favorite_by']

class PlanetsModelView(ModelView):
    column_auto_select_related = True  # Carga automáticamente las relaciones
    # Columnas y relationships de mi tabla PeopleFavorites
    column_list = ['id', 'name', 'weather', 'favorite_by_planet']

class StarshipsModelView(ModelView):
    column_auto_select_related = True  # Carga automáticamente las relaciones
    # Columnas y relationships de mi tabla PeopleFavorites
    column_list = ['id', 'name', 'color', 'favorite_by_starship']

class FavoriteCharactersModelView(ModelView):
    column_auto_select_related = True  # Carga automáticamente las relaciones
    # Columnas y relationships de mi tabla PeopleFavorites
    column_list = ['id', 'user', 'character', 'user_id', 'character_id']

class FavoritePlanetsModelView(ModelView):
    column_auto_select_related = True  # Carga automáticamente las relaciones
    # Columnas y relationships de mi tabla PeopleFavorites
    column_list = ['id', 'user', 'planet', 'user_id', 'planet_id']

class FavoriteStarshipsModelView(ModelView):
    column_auto_select_related = True  # Carga automáticamente las relaciones
    # Columnas y relationships de mi tabla PeopleFavorites
    column_list = ['id', 'user', 'starship', 'user_id', 'starship_id']

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(UserModelView(User, db.session))
    admin.add_view(CharacterModelView(Character, db.session))
    admin.add_view(PlanetsModelView(Planets, db.session))
    admin.add_view(StarshipsModelView(Starships, db.session))
    admin.add_view(FavoriteCharactersModelView(FavoriteCharacters, db.session))
    admin.add_view(FavoritePlanetsModelView(FavoritePlanets, db.session))
    admin.add_view(FavoriteStarshipsModelView(FavoriteStarships, db.session))
    

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))