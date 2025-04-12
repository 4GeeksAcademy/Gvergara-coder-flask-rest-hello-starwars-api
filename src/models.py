from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    lastName: Mapped[str] = mapped_column(String(25), nullable=False)
    firstName: Mapped[str] = mapped_column(String(25), nullable=False)
    favorites_characters: Mapped[list['FavoriteCharacters']] = relationship(
        back_populates='user', cascade='all, delete-orphan')
    favorites_planets: Mapped[list['FavoritePlanets']] = relationship(
        back_populates='user', cascade='all, delete-orphan')
    favorites_starships: Mapped[list['FavoriteStarships']] = relationship(
        back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f'Usuario con id {self.id} y email {self.email}'

    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'is_active': self.is_active
        }


class Character(db.Model):
    __tablename__ = 'character'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25), nullable=False)
    gender: Mapped[str] = mapped_column(String(25), nullable=False)
    height: Mapped[int] = mapped_column(Integer(), nullable=False)
    favorite_by: Mapped[list['FavoriteCharacters']] = relationship(
        back_populates='character', cascade='all, delete-orphan')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'height': self.height
        }


class Planets(db.Model):
    __tablename__ = 'planet'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25), nullable=False)
    weather: Mapped[str] = mapped_column(String(25), nullable=False)
    favorite_by_planet: Mapped[list['FavoritePlanets']] = relationship(
        back_populates='planet', cascade='all, delete-orphan')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'weather': self.weather
        }


class Starships(db.Model):
    __tablename__ = 'starship'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25), nullable=False)
    color: Mapped[str] = mapped_column(String(25), nullable=False)
    favorite_by_starship: Mapped[list['FavoriteStarships']] = relationship(
        back_populates='starship', cascade='all, delete-orphan')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'color': self.color
        }


class FavoriteCharacters(db.Model):
    __tablename__ = 'favoritecharacters'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    character_id: Mapped[int] = mapped_column(ForeignKey('character.id'))
    character: Mapped['Character'] = relationship(back_populates='favorite_by')
    user: Mapped['User'] = relationship(back_populates='favorites_characters')

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'character_id': self.character_id
        }


class FavoritePlanets(db.Model):
    __tablename__ = 'favoriteplanets'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    planet_id: Mapped[int] = mapped_column(ForeignKey('planet.id'))
    planet: Mapped['Planets'] = relationship(
        back_populates='favorite_by_planet')
    user: Mapped['User'] = relationship(back_populates='favorites_planets')

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'planet_id': self.planet_id
        }


class FavoriteStarships(db.Model):
    __tablename__ = 'favoritestarships'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    starship_id: Mapped[int] = mapped_column(ForeignKey('starship.id'))
    starship: Mapped['Starships'] = relationship(
        back_populates='favorite_by_starship')
    user: Mapped['User'] = relationship(back_populates='favorites_starships')

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'starship_id': self.starship_id
        }
